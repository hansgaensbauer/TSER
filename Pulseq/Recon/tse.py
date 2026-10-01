import warnings

import numpy as np

import pypulseq as pp
import matplotlib.pyplot as plt

def main(
    plot: bool = False,
    test_report: bool = False,
    write_seq: bool = False,
    seq_filename: str = 'tse_pypulseq.seq',
    *,
    fov: float | tuple[float, float] = 256e-3,
    n_x: int = 64,
    n_y: int = 64,
    n_echo: int = 16,
    n_slices: int = 1,
    rf_flip_deg: int = 180,
    slice_thickness: float = 5e-3,
    te: float = 12e-3,
    tr: float = 2000e-3,
):
    """Create a turbo spin-echo (TSE) sequence.

    Parameters
    ----------
    plot : bool, optional
        Plot the sequence diagram. Default is False.
    test_report : bool, optional
        Print a test report. Default is False.
    write_seq : bool, optional
        Write the sequence to a .seq file. Default is False.
    seq_filename : str, optional
        Output filename for the .seq file. Default is 'tse_pypulseq.seq'.
    fov : float or tuple of float, optional
        Field of view in meters. If a single value, it is used for both x and y.
        If a tuple, it is (fov_x, fov_y). Default is 256e-3.
    n_x : int, optional
        Number of readout samples. Default is 64.
    n_y : int, optional
        Number of phase encoding steps. Default is 64.
    n_echo : int, optional
        Number of echoes per excitation. Default is 16.
    n_slices : int, optional
        Number of slices. Default is 1.
    rf_flip_deg : int, optional
        Refocusing flip angle in degrees. Default is 180.
    slice_thickness : float, optional
        Slice thickness in meters. Default is 5e-3.
    te : float, optional
        Echo time in seconds. Default is 12e-3.
    tr : float, optional
        Repetition time in seconds. Default is 2000e-3.

    Returns
    -------
    seq : pypulseq.Sequence
        The TSE sequence object.
    """
    fov_x, fov_y = (fov, fov) if isinstance(fov, (int, float)) else fov
    dG = 250e-6

    # Set system limits
    system = pp.Opts(
        max_grad=32,
        grad_unit='mT/m',
        max_slew=130,
        slew_unit='T/m/s',
        rf_ringdown_time=100e-6,
        rf_dead_time=100e-6,
        adc_dead_time=10e-6,
    )

    seq = pp.Sequence(system)

    if isinstance(rf_flip_deg, int):
        rf_flip_deg = np.zeros(n_echo) + rf_flip_deg

    sampling_time = 6.4e-3
    readout_time = sampling_time + 2 * system.adc_dead_time
    t_ex = 2.5e-3
    t_exwd = t_ex + system.rf_ringdown_time + system.rf_dead_time
    t_ref = 2e-3
    t_refwd = t_ref + system.rf_ringdown_time + system.rf_dead_time
    t_sp = 0.5 * (te - readout_time - t_refwd)
    t_spex = 0.5 * (te - t_exwd - t_refwd)
    fsp_r = 1
    fsp_s = 0.5

    rf_ex_phase = np.pi / 2
    rf_ref_phase = 0

    # Create excitation pulse and gradient
    flip_ex = np.deg2rad(90)
    rf_ex, gz, _ = pp.make_sinc_pulse(
        flip_angle=flip_ex,
        system=system,
        duration=t_ex,
        slice_thickness=slice_thickness,
        apodization=0.5,
        time_bw_product=4,
        phase_offset=rf_ex_phase,
        return_gz=True,
        delay=system.rf_dead_time,
        use='excitation',
    )
    gs_ex = pp.make_trapezoid(
        channel='z',
        system=system,
        amplitude=gz.amplitude,
        flat_time=t_exwd,
        rise_time=dG,
    )

    flip_ref = np.deg2rad(rf_flip_deg[0])
    rf_ref, gz, _ = pp.make_sinc_pulse(
        flip_angle=flip_ref,
        system=system,
        duration=t_ref,
        slice_thickness=slice_thickness,
        apodization=0.5,
        time_bw_product=4,
        phase_offset=rf_ref_phase,
        use='refocusing',
        return_gz=True,
        delay=system.rf_dead_time,
    )
    gs_ref = pp.make_trapezoid(
        channel='z',
        system=system,
        amplitude=gs_ex.amplitude,
        flat_time=t_refwd,
        rise_time=dG,
    )

    ags_ex = gs_ex.area / 2
    gs_spr = pp.make_trapezoid(
        channel='z',
        system=system,
        area=ags_ex * (1 + fsp_s),
        duration=t_sp,
        rise_time=dG,
    )
    gs_spex = pp.make_trapezoid(channel='z', system=system, area=ags_ex * fsp_s, duration=t_spex, rise_time=dG)

    delta_kx = 1 / fov_x
    delta_ky = 1 / fov_y
    k_width = n_x * delta_kx

    gr_acq = pp.make_trapezoid(
        channel='x',
        system=system,
        flat_area=k_width,
        flat_time=readout_time,
        rise_time=dG,
    )
    adc = pp.make_adc(num_samples=n_x, duration=sampling_time, delay=system.adc_dead_time, system=system)
    gr_spr = pp.make_trapezoid(
        channel='x',
        system=system,
        area=gr_acq.area * fsp_r,
        duration=t_sp,
        rise_time=dG,
    )

    agr_spr = gr_spr.area
    agr_preph = gr_acq.area / 2 + agr_spr
    gr_preph = pp.make_trapezoid(channel='x', system=system, area=agr_preph, duration=t_spex, rise_time=dG)

    # Phase-encoding
    n_ex = int(np.floor(n_y / n_echo))
    pe_steps = np.arange(1, n_echo * n_ex + 1) - 0.5 * n_echo * n_ex - 1
    if divmod(n_echo, 2)[1] == 0:
        pe_steps = np.roll(pe_steps, [0, int(-np.round(n_ex / 2))])
    pe_order = pe_steps.reshape((n_ex, n_echo), order='F').T
    phase_areas = pe_order * delta_ky

    # Split gradients and recombine into blocks
    gs1_times = np.array([0, gs_ex.rise_time])
    gs1_amp = np.array([0, gs_ex.amplitude])
    gs1 = pp.make_extended_trapezoid(channel='z', times=gs1_times, amplitudes=gs1_amp)

    gs2_times = np.array([0, gs_ex.flat_time])
    gs2_amp = np.array([gs_ex.amplitude, gs_ex.amplitude])
    gs2 = pp.make_extended_trapezoid(channel='z', times=gs2_times, amplitudes=gs2_amp)

    gs3_times = np.array(
        [
            0,
            gs_spex.rise_time,
            gs_spex.rise_time + gs_spex.flat_time,
            gs_spex.rise_time + gs_spex.flat_time + gs_spex.fall_time,
        ]
    )
    gs3_amp = np.array([gs_ex.amplitude, gs_spex.amplitude, gs_spex.amplitude, gs_ref.amplitude])
    gs3 = pp.make_extended_trapezoid(channel='z', times=gs3_times, amplitudes=gs3_amp)

    gs4_times = np.array([0, gs_ref.flat_time])
    gs4_amp = np.array([gs_ref.amplitude, gs_ref.amplitude])
    gs4 = pp.make_extended_trapezoid(channel='z', times=gs4_times, amplitudes=gs4_amp)

    gs5_times = np.array(
        [
            0,
            gs_spr.rise_time,
            gs_spr.rise_time + gs_spr.flat_time,
            gs_spr.rise_time + gs_spr.flat_time + gs_spr.fall_time,
        ]
    )
    gs5_amp = np.array([gs_ref.amplitude, gs_spr.amplitude, gs_spr.amplitude, 0])
    gs5 = pp.make_extended_trapezoid(channel='z', times=gs5_times, amplitudes=gs5_amp)

    gs7_times = np.array(
        [
            0,
            gs_spr.rise_time,
            gs_spr.rise_time + gs_spr.flat_time,
            gs_spr.rise_time + gs_spr.flat_time + gs_spr.fall_time,
        ]
    )
    gs7_amp = np.array([0, gs_spr.amplitude, gs_spr.amplitude, gs_ref.amplitude])
    gs7 = pp.make_extended_trapezoid(channel='z', times=gs7_times, amplitudes=gs7_amp)

    # Readout gradient
    gr3 = gr_preph

    gr5_times = np.array(
        [
            0,
            gr_spr.rise_time,
            gr_spr.rise_time + gr_spr.flat_time,
            gr_spr.rise_time + gr_spr.flat_time + gr_spr.fall_time,
        ]
    )
    gr5_amp = np.array([0, gr_spr.amplitude, gr_spr.amplitude, gr_acq.amplitude])
    gr5 = pp.make_extended_trapezoid(channel='x', times=gr5_times, amplitudes=gr5_amp)

    gr6_times = np.array([0, readout_time])
    gr6_amp = np.array([gr_acq.amplitude, gr_acq.amplitude])
    gr6 = pp.make_extended_trapezoid(channel='x', times=gr6_times, amplitudes=gr6_amp)

    gr7_times = np.array(
        [
            0,
            gr_spr.rise_time,
            gr_spr.rise_time + gr_spr.flat_time,
            gr_spr.rise_time + gr_spr.flat_time + gr_spr.fall_time,
        ]
    )
    gr7_amp = np.array([gr_acq.amplitude, gr_spr.amplitude, gr_spr.amplitude, 0])
    gr7 = pp.make_extended_trapezoid(channel='x', times=gr7_times, amplitudes=gr7_amp)

    # Fill-times
    t_ex = pp.calc_duration(gs1) + pp.calc_duration(gs2) + pp.calc_duration(gs3)
    t_ref = pp.calc_duration(gs4) + pp.calc_duration(gs5) + pp.calc_duration(gs7) + readout_time
    t_end = pp.calc_duration(gs4) + pp.calc_duration(gs5)

    te_train = t_ex + n_echo * t_ref + t_end
    tr_delay = (tr - n_slices * te_train) / n_slices
    # Round to gradient raster
    tr_delay = system.grad_raster_time * np.round(tr_delay / system.grad_raster_time)
    if tr_delay < 0:
        tr_delay = 1e-3
        warnings.warn(f'TR too short, adapted to include all slices to: {1000 * n_slices * (te_train + tr_delay)} ms')
    else:
        print(f'TR delay: {1000 * tr_delay} ms')

    for i_excitation in range(n_ex + 1):
        for i_slice in range(n_slices):
            rf_ex.freq_offset = gs_ex.amplitude * slice_thickness * (i_slice - (n_slices - 1) / 2)
            rf_ref.freq_offset = gs_ref.amplitude * slice_thickness * (i_slice - (n_slices - 1) / 2)
            rf_ex.phase_offset = rf_ex_phase - 2 * np.pi * rf_ex.freq_offset * pp.calc_rf_center(rf_ex)[0]
            rf_ref.phase_offset = rf_ref_phase - 2 * np.pi * rf_ref.freq_offset * pp.calc_rf_center(rf_ref)[0]

            seq.add_block(gs1)
            seq.add_block(rf_ex, gs2)
            seq.add_block(gs3, gr3)

            for i_echo in range(n_echo):
                if i_excitation > 0:
                    phase_area = phase_areas[i_echo, i_excitation - 1]
                else:
                    phase_area = 0.0  # 0.0 and not 0 because -phase_area should successfully result in negative zero

                gp_pre = pp.make_trapezoid(
                    channel='y',
                    system=system,
                    area=phase_area,
                    duration=t_sp,
                    rise_time=dG,
                )
                gp_rew = pp.make_trapezoid(
                    channel='y',
                    system=system,
                    area=-phase_area,
                    duration=t_sp,
                    rise_time=dG,
                )
                seq.add_block(rf_ref, gs4)
                seq.add_block(gr5, gp_pre, gs5)
                if i_excitation > 0:
                    seq.add_block(gr6, adc)
                else:
                    seq.add_block(gr6)

                seq.add_block(gr7, gp_rew, gs7)

            seq.add_block(gs4)
            seq.add_block(gs5)
            seq.add_block(pp.make_delay(tr_delay))

    ok, error_report = seq.check_timing()
    if ok:
        print('Timing check passed successfully')
    else:
        print('Timing check failed. Error listing follows:')
        [print(e) for e in error_report]

    if test_report:
        print(seq.test_report())

    if plot:
        seq.plot()

    seq.set_definition(key='FOV', value=[fov_x, fov_y, slice_thickness * n_slices])
    seq.set_definition(key='Name', value='tse')

    eps = 1e-9
    def calculate_kspace(seq,trajectory_delay = 0, gradient_offset = 0.0):
        """
        Calculates the k-space trajectory of the entire pulse sequence.

        Parameters
        ----------
        trajectory_delay : float or list or numpy.ndarray, default=0
            Compensation factor in seconds (s) to align ADC and gradients in the reconstruction.
            If trajectory_delay is a single value, this value will be used for all gradient channels.
            If trajectory_delay is a list or array, it is expected to have the same length as the number of gradient
            channels and the first element is applied to the first gradient channel, the second to the second, and so on.
        gradient_offset : float or list or numpy.ndarray, default=0
            Simulates background gradients (specified in Hz/m)
            If gradient_offset is a single value, this value will be used for all gradient channels.
            If gradient_offset is a list or array, it is expected to have the same length as the number of gradient
            channels and the first element is applied to the first gradient channel, the second to the second, and so on.

        Returns
        -------
        k_traj_adc : numpy.array
            K-space trajectory sampled at `t_adc` timepoints.
        k_traj : numpy.array
            K-space trajectory of the entire pulse sequence.
        t_excitation : List[float]
            Excitation timepoints.
        t_refocusing : List[float]
            Refocusing timepoints.
        t_adc : numpy.array
            Sampling timepoints.
        """
        if np.any(np.abs(trajectory_delay) > 100e-6):
            raise Warning(f'Trajectory delay of {trajectory_delay * 1e6} us is suspiciously high')

        total_duration = sum(seq.block_durations.values())

        t_excitation, fp_excitation, t_refocusing, _ = seq.rf_times()
        t_adc, _ = seq.adc_times()

        # Convert data to piecewise polynomials
        gw_pp = seq.get_gradients(trajectory_delay, gradient_offset)
        ng = len(gw_pp)

        # Calculate slice positions.
        # For now we entirely rely on the excitation -- ignoring complicated interleaved refocused sequences
        if len(t_excitation) > 0:
            # Position in x, y, z
            slice_pos = np.zeros((ng, len(t_excitation)))
            for j in range(ng):
                if gw_pp[j] is None:
                    slice_pos[j] = np.nan
                else:
                    # Check for divisions by zero to avoid numpy warning
                    divisor = np.array(gw_pp[j](t_excitation))
                    slice_pos[j, divisor != 0.0] = fp_excitation[0, divisor != 0.0] / divisor[divisor != 0.0]
                    slice_pos[j, divisor == 0.0] = np.nan

            slice_pos[~np.isfinite(slice_pos)] = 0  # Reset undefined to 0
        else:
            slice_pos = []

        # Integrate waveforms as PPs to produce gradient moments
        gm_pp = []
        tc = []
        for i in range(ng):
            if gw_pp[i] is None:
                gm_pp.append(None)
                continue

            gm_pp.append(gw_pp[i].antiderivative())
            tc.append(gm_pp[i].x)
            # "Sample" ramps for display purposes.  Otherwise piecewise-linear display (plot) fails
            ii = np.flatnonzero(np.abs(gm_pp[i].c[0, :]) > 1e-7 * seq.system.max_slew)

            # Do nothing if there are no ramps
            if ii.shape[0] == 0:
                continue

            starts = np.int64(np.floor((gm_pp[i].x[ii] + eps) / seq.grad_raster_time))
            ends = np.int64(np.ceil((gm_pp[i].x[ii + 1] - eps) / seq.grad_raster_time))

            # Create all ranges starts[0]:ends[0], starts[1]:ends[1], etc.
            lengths = ends - starts + 1
            inds = np.ones((lengths).sum())
            # Calculate output index where each range will start
            start_inds = np.cumsum(np.concatenate(([0], lengths[:-1])))
            # Create element-wise differences that will cumsum into
            # the final indices: [starts[0], 1, 1, starts[1]-starts[0]-lengths[0]+1, 1, etc.]
            inds[start_inds] = np.concatenate(([starts[0]], np.diff(starts) - lengths[:-1] + 1))

            tc.append(np.cumsum(inds) * seq.grad_raster_time)
        if tc != []:
            tc = np.concatenate(tc)

        t_acc = 1e-10  # Temporal accuracy
        t_acc_inv = 1 / t_acc
        # tc = seq.__flatten_jagged_arr(tc)
        t_ktraj = t_acc * np.unique(
            np.round(
                t_acc_inv
                * np.array(
                    [
                        *tc,
                        0,
                        *np.asarray(t_excitation) - 2 * seq.rf_raster_time,
                        *np.asarray(t_excitation) - seq.rf_raster_time,
                        *t_excitation,
                        *np.asarray(t_refocusing) - seq.rf_raster_time,
                        *t_refocusing,
                        *t_adc,
                        total_duration,
                    ]
                )
            )
        )

        i_excitation = np.searchsorted(t_ktraj, t_acc * np.round(t_acc_inv * np.asarray(t_excitation)))
        i_refocusing = np.searchsorted(t_ktraj, t_acc * np.round(t_acc_inv * np.asarray(t_refocusing)))
        i_adc = np.searchsorted(t_ktraj, t_acc * np.round(t_acc_inv * np.asarray(t_adc)))

        i_periods = np.unique([0, *i_excitation, *i_refocusing, len(t_ktraj) - 1])
        if len(i_excitation) > 0:
            ii_next_excitation = 0
        else:
            ii_next_excitation = -1
        if len(i_refocusing) > 0:
            ii_next_refocusing = 0
        else:
            ii_next_refocusing = -1

        k_traj = np.zeros((ng, len(t_ktraj)))
        for i in range(ng):
            if gw_pp[i] is None:
                continue

            it = np.where(
                np.logical_and(
                    t_ktraj >= t_acc * round(t_acc_inv * gm_pp[i].x[0]),
                    t_ktraj <= t_acc * round(t_acc_inv * gm_pp[i].x[-1]),
                )
            )[0]
            k_traj[i, it] = gm_pp[i](t_ktraj[it])
            if t_ktraj[it[-1]] < t_ktraj[-1]:
                k_traj[i, it[-1] + 1 :] = k_traj[i, it[-1]]

        # Convert gradient moments to k-space positions
        dk = -k_traj[:, 0]
        for i in range(len(i_periods) - 1):
            i_period = i_periods[i]
            i_period_end = i_periods[i + 1]
            if ii_next_excitation >= 0 and i_excitation[ii_next_excitation] == i_period:
                if abs(t_ktraj[i_period] - t_excitation[ii_next_excitation]) > t_acc:
                    raise Warning(
                        f'abs(t_ktraj[i_period]-t_excitation[ii_next_excitation]) < {t_acc} failed for ii_next_excitation={ii_next_excitation} error={t_ktraj(i_period) - t_excitation(ii_next_excitation)}'
                    )
                dk = -k_traj[:, i_period]
                if i_period > 0:
                    # Use nans to mark the excitation points since they interrupt the plots
                    k_traj[:, i_period - 1] = np.nan
                # -1 on len(i_excitation) for 0-based indexing
                ii_next_excitation = min(len(i_excitation) - 1, ii_next_excitation + 1)
            elif ii_next_refocusing >= 0 and i_refocusing[ii_next_refocusing] == i_period:
                # dk = -k_traj[:, i_period]
                dk = -2 * k_traj[:, i_period] - dk
                # -1 on len(i_excitation) for 0-based indexing
                ii_next_refocusing = min(len(i_refocusing) - 1, ii_next_refocusing + 1)

            k_traj[:, i_period:i_period_end] = k_traj[:, i_period:i_period_end] + dk[:, None]

        k_traj[:, i_period_end] = k_traj[:, i_period_end] + dk
        k_traj_adc = k_traj[:, i_adc]

        return k_traj_adc, k_traj, t_excitation, t_refocusing, t_adc, t_ktraj

    [k_traj_adc, k_traj, t_excitation, t_refocusing, t_adc, t_ktraj] = calculate_kspace(seq)

    plt.figure()
    plt.plot(t_ktraj, k_traj[0])
    plt.plot(t_ktraj, k_traj[1])
    plt.plot(t_ktraj, k_traj[2])
    plt.show()

    if write_seq:
        seq.write(seq_filename)

    return seq


if __name__ == '__main__':
    main(plot=True, write_seq=True)