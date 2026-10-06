import numpy as np
import pypulseq as pp
import uuid
import shutil
from pathlib import Path

slice_thickness = 4e-3
n_slices = 4
num_pts = 128
fov = 108e-3
slice_spacing = 9e-3
t_echo = 10e-3
num_echoes = 10
recovery_time = 5

exc_pulse_duration = 3e-3
refoc_pulse_duration = 2e-3
grad_rise_time = 110e-6
delta_k = 1/fov

system = pp.Opts(
    max_grad=28,
    grad_unit='mT/m',
    max_slew=150,
    slew_unit='T/m/s',
    rf_ringdown_time=20e-6,
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
    delay=max(grad_rise_time, system.rf_dead_time),
    use='excitation'
)

bandwidth = time_bw_product / exc_pulse_duration   # Hz
amplitude = bandwidth / slice_thickness     # Hz/m (pulseq internal units)

g_ss = pp.make_trapezoid(
    channel='z',
    amplitude=amplitude,
    rise_time=grad_rise_time,
    flat_time=exc_pulse_duration,
    system=system
)

g_ro_dur = t_echo - refoc_pulse_duration - 2*system.rf_dead_time
reph_grad_duration = (t_echo-exc_pulse_duration-refoc_pulse_duration)/2-grad_rise_time-system.rf_dead_time
g_ro = pp.make_trapezoid(channel='x', area=num_pts*delta_k, duration=g_ro_dur, rise_time=grad_rise_time, system=system)
g_ro_prewind = pp.make_trapezoid(channel='x', area=g_ro.area / 2, duration=reph_grad_duration,rise_time=grad_rise_time, system=system)
g_ss_reph = pp.make_trapezoid(channel='z', area=-g_ss.area / 2, duration=reph_grad_duration,rise_time=grad_rise_time, system=system)

rf180 = pp.make_block_pulse(
    flip_angle=np.pi,
    duration=refoc_pulse_duration,
    system=system,
    delay=system.rf_dead_time,
    phase_offset = np.pi/2
)

adc_raster = system.adc_raster_time

dwell = round(g_ro.flat_time / num_pts / adc_raster) * adc_raster

duration = dwell * num_pts

adc = pp.make_adc(
    num_samples=num_pts,
    duration=duration,
    delay=grad_rise_time,   # start sampling when gradient is flat
    system=system
)

for s in range(n_slices):
    rf.freq_offset = g_ss.amplitude*slice_spacing*(s-(n_slices-1)/2)
    print(rf.freq_offset)
    rf180.phase_offset = np.pi/2
    seq.add_block(rf, g_ss)
    seq.add_block(g_ss_reph, g_ro_prewind)

    for i in range(num_echoes):
        seq.add_block(rf180)
        seq.add_block(pp.make_delay(system.rf_dead_time - system.rf_ringdown_time))
        seq.add_block(g_ro, adc)

    
    seq.add_block(pp.make_delay(recovery_time))
    rf180.phase_offset = -np.pi/2

    seq.add_block(rf, g_ss)
    seq.add_block(g_ss_reph, g_ro_prewind)

    for i in range(num_echoes):
        seq.add_block(rf180)
        seq.add_block(pp.make_delay(system.rf_dead_time - system.rf_ringdown_time))
        seq.add_block(g_ro, adc)

    seq.add_block(pp.make_delay(recovery_time))

seq.set_definition(key='FOV', value=[fov, 20e-3, 150e-3])
seq.set_definition(key='Name', value='cpmg_multislice')

seq.check_timing()
seq_uuid = str(uuid.uuid4())[-8:]
print(f'Unique ID: {seq_uuid}')
src = Path(__file__).resolve()

seq.write(f'{str(src.parent)}/Sequences/{n_slices}s_{slice_thickness*1000}mm_{num_echoes}e_{t_echo*1000}te_{seq_uuid}'+'.seq')

dst = src.parent  / Path(f"Sequences/Source/{seq_uuid}.py.bak")
shutil.copy2(src, dst)

# plot_loop(seq, 5,7, "$N_e$", save=True)
seq.plot()