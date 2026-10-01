import numpy as np
import pypulseq as pp

# from Pulseq.Python.plot_loop import plot_loop

#wells running along z, slice select in x, readout in z

slice_thickness = 4e-3
n_slices = 1
slice_gap         = 9e-3
num_pts = 32
fov = 50e-3
recovery_time = 5
delta_k = 1/fov
t_echo = 50e-3
num_echoes = 80
exc_pulse_duration = 2.5e-3
refoc_pulse_duration = 3e-3
grad_rise_time = 110e-6

system = pp.Opts(
    max_grad=20,
    grad_unit='mT/m',
    max_slew=100,
    slew_unit='T/m/s',
    rf_ringdown_time=30e-6,
    rf_dead_time=100e-6,
    adc_dead_time=20e-6
)

seq = pp.Sequence(system)

time_bw_product = 4
rf = pp.make_sinc_pulse(
    flip_angle=np.pi/2,
    duration=exc_pulse_duration,
    slice_thickness=slice_thickness,
    apodization=0.42,
    time_bw_product=time_bw_product,
    system=system,
    return_gz=False,
    delay=max(grad_rise_time, system.rf_dead_time)
)

bandwidth = time_bw_product / exc_pulse_duration   # Hz
amplitude = bandwidth / slice_thickness     # Hz/m (pulseq internal units)

gx = pp.make_trapezoid(
    channel='x',
    amplitude=amplitude,
    rise_time=grad_rise_time,
    flat_time=exc_pulse_duration,
    system=system
)

gz_dur = t_echo - refoc_pulse_duration - 2*system.rf_dead_time
reph_grad_duration = (t_echo-exc_pulse_duration-refoc_pulse_duration)/2-grad_rise_time-system.rf_dead_time
gz = pp.make_trapezoid(channel='z', area=num_pts*delta_k, duration=gz_dur, rise_time=grad_rise_time, system=system)
gz_prewind = pp.make_trapezoid(channel='z', area=gz.area / 2, duration=reph_grad_duration,rise_time=grad_rise_time, system=system)
gx_reph = pp.make_trapezoid(channel='x', area=-gx.area / 2, duration=reph_grad_duration,rise_time=grad_rise_time, system=system)

rf180 = pp.make_block_pulse(
    flip_angle=np.pi,
    duration=refoc_pulse_duration,
    system=system,
    delay=system.rf_dead_time,
    phase_offset = np.pi/2,
    use='refocusing'
)

adc_raster = system.adc_raster_time

dwell = round(gz.flat_time / num_pts / adc_raster) * adc_raster

duration = dwell * num_pts

adc = pp.make_adc(
    num_samples=num_pts,
    duration=duration,
    delay=grad_rise_time,   # start sampling when gradient is flat
    system=system
)

for s in range(n_slices):
    rf.freqOffset=gx.amplitude*slice_gap*(s-(n_slices-1)/2)
    rf180.phase_offset = np.pi/2
    seq.add_block(rf, gx)
    seq.add_block(gx_reph, gz_prewind)

    for i in range(num_echoes):
        seq.add_block(rf180)
        seq.add_block(pp.make_delay(system.rf_dead_time - system.rf_ringdown_time))
        seq.add_block(gz, adc)

    
    seq.add_block(pp.make_delay(recovery_time))
    rf180.phase_offset = -np.pi/2

    seq.add_block(rf, gx)
    seq.add_block(gx_reph, gz_prewind)

    for i in range(num_echoes):
        seq.add_block(rf180)
        seq.add_block(pp.make_delay(system.rf_dead_time - system.rf_ringdown_time))
        seq.add_block(gz, adc)

    if(s < n_slices - 1):
        seq.add_block(pp.make_delay(recovery_time))

# seq.check_timing()
# seq.write('cpmg_1s_80e_50te.seq')

import matplotlib.pyplot as plt
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
plt.plot(t_ktraj, k_traj[2])
plt.plot(t_ktraj, k_traj[0])
# plot_loop(seq, 5,7, "$N_e$", save=True)
seq.plot()