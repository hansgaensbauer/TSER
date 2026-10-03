# =============================================================================
# run_sim.jl
#
# Load a saved phantom, simulate a Pulseq sequence on a Skyra-like scanner, and
# save the raw ADC signal to an HDF5 file that is easy to read from Python.
#
#   julia -t auto run_sim.jl cylinders.phantom my_sequence.seq [out.h5]
#
# Extra setup (once):  julia> ] add HDF5
# =============================================================================
include(joinpath(@__DIR__, "cylinder_lib.jl"))
using HDF5

length(ARGS) >= 2 || error("Usage: julia -t auto run_sim.jl phantom.phantom sequence.seq [out.h5]")
PHANTOM_PATH, SEQ_PATH = ARGS[1], ARGS[2]
OUT_PATH = length(ARGS) >= 3 ? ARGS[3] : "sim_output.h5"

# ---- load inputs ------------------------------------------------------------
obj = read_phantom(PHANTOM_PATH)
seq = read_seq(SEQ_PATH)
sys = skyra_scanner()
println("Phantom: $(length(obj.x)) spins;  sequence: $SEQ_PATH")

show_plot(plot_seq(seq; height = 500), "sequence")   # quick sanity check

# ---- simulate ---------------------------------------------------------------
sim_params = KomaMRICore.default_sim_params()
sim_params["return_type"] = "mat"                    # plain complex matrix (Nsamples × Ncoils)
sim_params["Nthreads"]    = Threads.nthreads()
sim_params["gpu"]         = false                    # true if a GPU backend is set up

sig = simulate(obj, seq, sys; sim_params = sim_params)
println("Raw signal size returned by simulate: ", size(sig))
# Depending on the KomaMRI version the matrix can come back as (samples,),
# (samples, coils) or (samples, coils, extra). Drop trailing singleton dims
# beyond 2 and make sure we have at least 2 dims: (samples, coils[, ...]).
function normalize_signal(A)
    A = ndims(A) == 1 ? reshape(A, :, 1) : A
    while ndims(A) > 2 && size(A, ndims(A)) == 1
        A = dropdims(A; dims = ndims(A))
    end
    return A
end
sig = normalize_signal(sig)
println("Saving signal with size ", size(sig), " (samples × coils[ × extra])")

# Julia is column-major, h5py row-major: reversing the dimension order on write
# means Python sees the array with the same axis order as printed above.
rev(A) = permutedims(A, ndims(A):-1:1)

# ---- sampling times and k-space (best-effort; depends on KomaMRI version) ----
t_adc = try
    Float64.(vec(get_adc_sampling_times(seq)))
catch err
    @warn "Could not get ADC sampling times" exception = err
    nothing
end
kadc = try
    _, k_adc = get_kspace(seq)
    Float64.(Array(k_adc))                           # N × (≥3): kx, ky, kz in 1/m
catch err
    @warn "Could not get k-space trajectory" exception = err
    nothing
end

# ---- save to HDF5 -----------------------------------------------------------
# Arrays are written with reversed dimension order so h5py sees them as
# (Nsamples, Ncoils[, extra]) and (Nsamples, 3) -- see load_sim.py.
h5open(OUT_PATH, "w") do f
    write(f, "signal_real", rev(Float64.(real.(sig))))
    write(f, "signal_imag", rev(Float64.(imag.(sig))))
    t_adc === nothing || write(f, "t_adc", t_adc)                       # [s]
    kadc  === nothing || write(f, "kspace_adc", rev(kadc))      # [1/m]

    attrs(f)["phantom_file"] = basename(PHANTOM_PATH)
    attrs(f)["sequence_file"] = basename(SEQ_PATH)
    attrs(f)["n_spins"] = length(obj.x)
    attrs(f)["B0_T"] = sys.B0
    attrs(f)["Gmax_T_per_m"] = sys.Gmax
    attrs(f)["Smax_T_per_m_per_s"] = sys.Smax
    attrs(f)["ADC_dt_s"] = sys.ADC_Δt
end
println("Saved simulation output to ", OUT_PATH)