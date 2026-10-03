# =============================================================================
# make_phantom.jl
#
# Define the cylinder phantom, preview it, and save it to disk.
#   julia make_phantom.jl [output.phantom]
# Output is a KomaMRI .phantom file (HDF5; readable in Julia via read_phantom
# and in Python via h5py).
# =============================================================================
include(joinpath(@__DIR__, "cylinder_lib.jl"))

OUT_PATH = length(ARGS) >= 1 ? ARGS[1] : "cylinders.phantom"

# -----------------------------------------------------------------------------
# 5. Configure the phantom here
# -----------------------------------------------------------------------------
# Option A: a regular 3×3 grid of tubes, all along z, with varying T1/T2
# (loosely inspired by a relaxometry phantom at 3 T).
# T1_vals = [0.30, 0.45, 0.60, 0.80, 1.00, 1.20, 1.50, 1.80, 2.20]   # s
# T2_vals = [0.03, 0.05, 0.07, 0.09, 0.12, 0.16, 0.20, 0.30, 0.45]   # s

cylinders = cylinder_grid(
    nrows  = 5, ncols = 8,
    pitch  = 9e-3,                 # centre-to-centre spacing [m]
    radius = 2e-3,                 # [m]
    length = 4e-3,                 # [m]
    axis   = (0.0, 1.0, 0.0),       # long axis of every tube
    center = (0.0, 0.0, 0.0),       # centre of the whole grid [m]
    T1s = 0.3, T2s = 0.05, ρs = 1.0,
)

deleteat!(cylinders, [2, 5, 9, 12, 13, 18, 19, 20, 21, 35, 38])

# Option B: tweak individual cylinders after the fact, or add extra ones.
# e.g. tilt the centre tube by 20° towards x, and make it thinner:
# cylinders[5] = Cylinder(center = (0.0, 0.0, 0.0), radius = 6e-3, length = 80e-3,
#                         axis = (sin(deg2rad(20)), 0.0, cos(deg2rad(20))),
#                         T1 = 1.0, T2 = 0.12, label = "tilted")
# push!(cylinders, Cylinder(center = (0.0, 60e-3, 0.0), radius = 12e-3, length = 50e-3,
#                           axis = (1.0, 0.0, 0.0), T1 = 0.8, T2 = 0.08, label = "extra"))

# Spin lattice spacing [m]. Use a coarser dz for 2D slice-selective sequences if
# you only care about a thin slab; use a fine dz if the slice is thick.
spin_spacing = (1e-3, 1e-3, 1.0e-3)

# -----------------------------------------------------------------------------
# 6. Build + preview
# -----------------------------------------------------------------------------
obj = build_phantom(cylinders; Δ = spin_spacing, jitter = 0.0)
println("Phantom has $(length(obj.x)) spins in $(length(cylinders)) cylinders.")

# Interactive phantom view (colour by proton density; try :T1, :T2, :Δw too).
p_rho = plot_phantom_map(obj, :ρ; height = 600, width = 700)
show_plot(p_rho, "phantom_rho")
p_t1  = plot_phantom_map(obj, :T1; height = 600, width = 700)
show_plot(p_t1, "phantom_T1")

# -----------------------------------------------------------------------------
# Save
# -----------------------------------------------------------------------------
write_phantom(obj, OUT_PATH)
println("Saved phantom to ", OUT_PATH)
