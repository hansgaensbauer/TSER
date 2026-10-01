import numpy as np
import pypulseq as pp

# from Pulseq.Python.plot_loop import plot_loop

#wells running along z, slice select in x, readout in z

slice_thickness = 4e-3
n_slices = 8
num_pts = 32
fov = 50e-3
delta_k = 1/fov
t_echo = 10e-3
num_echoes = 3
exc_pulse_duration = 2.5e-3
refoc_pulse_duration = 2e-3
grad_rise_time = 110e-6

system = pp.Opts(
    max_grad=32,
    grad_unit='mT/m',
    max_slew=130,
    slew_unit='T/m/s',
    rf_ringdown_time=30e-6,
    rf_dead_time=100e-6,
    adc_dead_time=10e-6
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
    phase_offset = np.pi/2
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

seq.add_block(rf, gx)
seq.add_block(gx_reph, gz_prewind)

for i in range(num_echoes):
    seq.add_block(rf180)
    seq.add_block(pp.make_delay(system.rf_dead_time - system.rf_ringdown_time))
    seq.add_block(gz, adc)

seq.check_timing()
# seq.write('cpmg_1d.seq')

# plot_loop(seq, 5,7, "$N_e$", save=True)
seq.plot()