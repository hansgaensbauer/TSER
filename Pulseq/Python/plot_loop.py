
import matplotlib.pyplot as plt
import matplotlib as mpl
import itertools
import math
import numpy as np
import pypulseq as pp
from pypulseq.utils.cumsum import cumsum
from pypulseq.Sequence import block, parula
from pypulseq.calc_rf_center import calc_rf_center
from pypulseq.supported_labels_rf_use import get_supported_labels


from matplotlib.path import Path
from matplotlib.patches import PathPatch



def plot_loop(
    seq: pp.Sequence = pp.Sequence(),
    loopstart_block: int = None,
    loopend_block: int = None,
    loopiters: str = str(),
    label: str = str(),
    show_blocks: bool = False,
    save: bool = False,
    time_range=(0, np.inf),
    time_disp: str = 's',
    grad_disp: str = 'kHz/m',
    plot_now: bool = True,
) -> None:
    """
    Plot `Sequence`.

    Parameters
    ----------
    label : str, default=str()
        Plot label values for ADC events: in this example for LIN and REP labels; other valid labes are accepted as
        a comma-separated list.
    save : bool, default=False
        Boolean flag indicating if plots should be saved. The two figures will be saved as JPG with numerical
        suffixes to the filename 'seq_plot'.
    show_blocks : bool, default=False
        Boolean flag to indicate if grid and tick labels at the block boundaries are to be plotted.
    time_range : iterable, default=(0, np.inf)
        Time range (x-axis limits) for plotting the sequence. Default is 0 to infinity (entire sequence).
    time_disp : str, default='s'
        Time display type, must be one of `s`, `ms` or `us`.
    grad_disp : str, default='s'
        Gradient display unit, must be one of `kHz/m` or `mT/m`.
    plot_now : bool, default=True
        If true, function immediately shows the plots, blocking the rest of the code until plots are exited.
        If false, plots are shown when plt.show() is called. Useful if plots are to be modified.
    plot_type : str, default='Gradient'
        Gradients display type, must be one of either 'Gradient' or 'Kspace'.
    """
    mpl.rcParams['lines.linewidth'] = 0.75  # Set default Matplotlib linewidth

    valid_time_units = ['s', 'ms', 'us']
    valid_grad_units = ['kHz/m', 'mT/m']
    valid_labels = get_supported_labels()
    if not all(isinstance(x, (int, float)) for x in time_range) or len(time_range) != 2:
        raise ValueError('Invalid time range')
    if time_disp not in valid_time_units:
        raise ValueError('Unsupported time unit')

    if grad_disp not in valid_grad_units:
        raise ValueError('Unsupported gradient unit. Supported gradient units are: ' + str(valid_grad_units))

    fig2, fig2_subplots = plt.subplots(4,1, sharex=True)

    t_factor_list = [1, 1e3, 1e6]
    t_factor = t_factor_list[valid_time_units.index(time_disp)]

    g_factor_list = [1e-3, 1e3 / seq.system.gamma]
    g_factor = g_factor_list[valid_grad_units.index(grad_disp)]

    t0 = 0
    label_defined = False
    label_idx_to_plot = []
    label_legend_to_plot = []
    label_store = {}
    for i in range(len(valid_labels)):
        label_store[valid_labels[i]] = 0
        if valid_labels[i] in label.upper():
            label_idx_to_plot.append(i)
            label_legend_to_plot.append(valid_labels[i])

    # Block timings
    block_edges = np.cumsum([0] + [x[1] for x in sorted(seq.block_durations.items())])
    block_edges_in_range = block_edges[(block_edges >= time_range[0]) * (block_edges <= time_range[1])]
    if show_blocks:
        for sp in [*fig2_subplots]:
            sp.set_xticks(t_factor * block_edges_in_range)
            sp.set_xticklabels(sp.get_xticklabels(), rotation=90)

    print(block_edges)
    for block_counter in seq.block_events:
        block = seq.get_block(block_counter)
        is_valid = time_range[0] <= t0 + seq.block_durations[block_counter] and t0 <= time_range[1]
        if is_valid:
            if getattr(block, 'label', None) is not None:
                for i in range(len(block.label)):
                    if block.label[i].type == 'labelinc':
                        label_store[block.label[i].label] += block.label[i].value
                    else:
                        label_store[block.label[i].label] = block.label[i].value
                label_defined = True

            if getattr(block, 'rf', None) is not None:  # RF
                rf = block.rf
                tc, ic = calc_rf_center(rf)
                time = rf.t
                signal = rf.signal
                if abs(signal[0]) != 0:
                    signal = np.concatenate(([0], signal))
                    time = np.concatenate(([time[0]], time))
                    ic += 1

                if abs(signal[-1]) != 0:
                    signal = np.concatenate((signal, [0]))
                    time = np.concatenate((time, [time[-1]]))

                time_orig = (t0 + time + rf.delay)
                loop_dur = block_edges[loopend_block] - block_edges[loopstart_block]
                # print(loop_dur)
                time_folded = (time_orig - block_edges[loopstart_block]) % loop_dur + block_edges[loopstart_block]
                time_folded[time_orig < block_edges[loopstart_block]] = time_orig[time_orig < block_edges[loopstart_block]]

                breaks = np.diff(time_folded) < 0
                x_plot = time_folded.astype(float).copy()
                y_plot = signal * np.exp(1j * rf.phase_offset) * np.exp(1j * 2 * math.pi * time * rf.freq_offset)

                x_plot[1:][breaks] = np.nan
                y_plot[1:][breaks] = np.nan
                fig2_subplots[0].plot(t_factor * x_plot, np.real(y_plot), 'k', linewidth = 1)
                fig2_subplots[0].plot(t_factor * x_plot, np.imag(y_plot), '--', color='grey', linewidth = 1)

            fig2_subplots[0].legend(["Real", "Imag"], ncols=2, loc='upper left')

            grad_channels = ['gx', 'gy', 'gz']
            for x in range(len(grad_channels)):  # Gradients
                if getattr(block, grad_channels[x], None) is not None:
                    grad = getattr(block, grad_channels[x])
                    if grad.type == 'grad':
                        # We extend the shape by adding the first and the last points in an effort of making the
                        # display a bit less confusing...
                        time = grad.delay + np.array([0, *grad.tt, grad.shape_dur])
                        waveform = g_factor * np.array((grad.first, *grad.waveform, grad.last))
                    else:
                        time = np.array(
                            cumsum(
                                0,
                                grad.delay,
                                grad.rise_time,
                                grad.flat_time,
                                grad.fall_time,
                            )
                        )
                        waveform = g_factor * grad.amplitude * np.array([0, 0, 1, 1, 0])
                    time_orig = (t0 + time)
                    loop_dur = block_edges[loopend_block] - block_edges[loopstart_block]
                    time_folded = time_orig
                    if(time_orig[0] >= block_edges[loopstart_block]):
                        time_folded = (time_orig - block_edges[loopstart_block]) % loop_dur + block_edges[loopstart_block]

                    breaks = np.diff(time_folded) < 0
                    x_plot = time_folded.astype(float).copy()
                    y_plot = waveform.astype(float).copy()

                    x_plot[1:][breaks] = np.nan
                    y_plot[1:][breaks] = np.nan
                    fig2_subplots[x+1].plot(t_factor * x_plot, y_plot, 'k', linewidth = 1)
        t0 += seq.block_durations[block_counter]

    grad_plot_labels = ['rf','x', 'y', 'z']

    for x in range(1,4):
        _label = grad_plot_labels[x]
        fig2_subplots[x].set_ylabel(f'G{_label} ({grad_disp})')
        fig2_subplots[x].axhline(0,color='k', linewidth=1.5)

    fig2_subplots[0].set_ylabel("RF (Hz)")
    fig2_subplots[0].axhline(0,color='k', linewidth=1)
    fig2_subplots[-1].set_xlabel(f't ({time_disp})')

    

    # Grid on
    for sp in [*fig2_subplots]:
        sp.grid()

    fig2.tight_layout()

    loopheight = 0.5
    loopbracket_start = fig2.transFigure.inverted().transform(
            fig2_subplots[0].transData.transform((t_factor * block_edges[loopstart_block], 0))
        )
    
    loopbracket_end = fig2.transFigure.inverted().transform(
        fig2_subplots[0].transData.transform((t_factor * block_edges[loopend_block], 0))
    )

    def bracket(fig, x, y, size=0.03, width=0.01, left=True, **kwargs):
        """
        Draw a scalable bracket in figure coordinates.

        x, y   : bracket center (figure coords)
        size   : vertical size (figure fraction)
        width  : horizontal depth (figure fraction)
        left   : left or right bracket
        """
        s = size / 2
        w = width if left else -width

        verts = [
            (x + w, y + s),
            (x,     y + s),
            (x,     y - s),
            (x + w, y - s),
        ]

        codes = [
            Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.LINETO,
        ]

        patch = PathPatch(
            Path(verts, codes),
            transform=fig.transFigure,
            fill=False,
            **kwargs
        )

        fig.add_artist(patch)


    bracket(fig2, loopbracket_start[0] - 0.01, 0.55, size=0.85, width=0.02, left=True,  lw=2, color='r')
    bracket(fig2, loopbracket_end[0] + 0.01, 0.55, size=0.85, width=0.02, left=False,  lw=2, color='r')

    fig2.text(loopbracket_end[0] - 0.012, 0.55-0.85/2-0.05, "x" + loopiters, fontsize=15, color='r', ha='right')

    if save:
        fig2.savefig('seq_plot.jpg')

    if plot_now:
        plt.show()