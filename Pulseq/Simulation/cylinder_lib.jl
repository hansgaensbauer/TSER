# =============================================================================
# cylinder_lib.jl  --  shared code: Cylinder type, phantom builder, Skyra
# scanner, and the browser-based plot helper. Included by the other scripts.
# =============================================================================

using KomaMRI
using LinearAlgebra
using PlotlyJS          # backend for KomaMRI plots

# -----------------------------------------------------------------------------
# Plot helper: `display(plot)` needs an Electron/Blink window, which fails in
# plain scripts / headless sessions (ECONNREFUSED). Instead, write each plot to
# an HTML file and open it in the default browser.
# -----------------------------------------------------------------------------
const OPEN_IN_BROWSER = true            # set false to only write the files
const PLOT_DIR = joinpath(pwd(), "plots")

function show_plot(p, name::AbstractString)
    mkpath(PLOT_DIR)
    path = joinpath(PLOT_DIR, name * ".html")
    try
        PlotlyJS.savefig(p, path)
    catch
        open(path, "w") do io
            PlotlyJS.to_html(io, p; include_plotlyjs = "cdn")
        end
    end
    println("Saved plot: ", path)
    if OPEN_IN_BROWSER
        try
            if Sys.isapple()
                run(`open $path`)
            elseif Sys.iswindows()
                run(`cmd /c start "" $path`)
            else
                run(`xdg-open $path`)
            end
        catch
            @info "Couldn't launch a browser automatically; open the file manually."
        end
    end
    return path
end

# -----------------------------------------------------------------------------
# 1. Cylinder description
# -----------------------------------------------------------------------------
"""
    Cylinder(; center, radius, length, axis, ρ, T1, T2, Δf, label)

A uniform solid cylinder.
- `center` : (x, y, z) of the cylinder centre [m]
- `radius` : radius [m]
- `length` : full length along its axis [m]
- `axis`   : direction vector of the long axis (any length, normalised internally)
- `ρ`      : proton density (relative)
- `T1, T2` : relaxation times [s]
- `Δf`     : off-resonance [Hz]
"""
Base.@kwdef struct Cylinder
    center::NTuple{3,Float64} = (0.0, 0.0, 0.0)
    radius::Float64           = 5e-3
    length::Float64           = 50e-3
    axis::NTuple{3,Float64}   = (0.0, 0.0, 1.0)
    ρ::Float64                = 1.0
    T1::Float64               = 1.0
    T2::Float64               = 0.1
    Δf::Float64               = 0.0
    label::String             = "cyl"
end

unit_axis(c::Cylinder) = collect(c.axis) ./ norm(collect(c.axis))

"Half-extent of the cylinder's bounding box along each world axis [m]."
function half_extents(c::Cylinder)
    u = unit_axis(c)
    return [(c.length / 2) * abs(u[i]) + c.radius * sqrt(max(0.0, 1 - u[i]^2)) for i in 1:3]
end

"Boolean mask: which points (3×N matrix) lie inside the cylinder."
function inside(c::Cylinder, P::AbstractMatrix)
    u = unit_axis(c)
    d = P .- collect(c.center)            # 3×N offsets from centre
    a = vec(u' * d)                       # component along the axis
    perp = d .- u * a'                    # component perpendicular to the axis
    r = vec(sqrt.(sum(abs2, perp; dims = 1)))
    return (abs.(a) .<= c.length / 2) .& (r .<= c.radius)
end

# -----------------------------------------------------------------------------
# 2. Convenience: lay out a regular grid of cylinders
# -----------------------------------------------------------------------------
"""
    cylinder_grid(; nrows, ncols, pitch, radius, length, axis, center, T1s, T2s, ρs, Δf)

Create `nrows × ncols` cylinders on a regular grid in the plane perpendicular
to `axis` (all sharing the same axis), centred on `center`.
`pitch` is the centre-to-centre spacing (m), either a scalar or (row, col).
`T1s`, `T2s`, `ρs` may be scalars or vectors of length nrows*ncols (row-major),
so every tube can have different contrast.
Per-cylinder overrides afterwards are easy: just edit the returned vector.
"""
function cylinder_grid(; nrows = 3, ncols = 3, pitch = 25e-3,
                         radius = 8e-3, length = 60e-3,
                         axis = (0.0, 0.0, 1.0), center = (0.0, 0.0, 0.0),
                         T1s = 1.0, T2s = 0.1, ρs = 1.0, Δf = 0.0)
    n = nrows * ncols
    expand(v) = v isa AbstractVector ? v : fill(v, n)
    T1v, T2v, ρv = expand(T1s), expand(T2s), expand(ρs)
    @assert all(Base.length.((T1v, T2v, ρv)) .== n) "T1s/T2s/ρs must be scalars or length nrows*ncols"
    prow, pcol = pitch isa Tuple ? pitch : (pitch, pitch)

    # Orthonormal basis (e1, e2) spanning the plane perpendicular to `axis`
    u  = collect(axis) ./ norm(collect(axis))
    ref = abs(u[3]) < 0.9 ? [0.0, 0.0, 1.0] : [1.0, 0.0, 0.0]
    e1 = normalize(cross(u, ref))
    e2 = cross(u, e1)

    cyls = Cylinder[]
    k = 0
    for i in 1:nrows, j in 1:ncols
        k += 1
        off = ((i - (nrows + 1) / 2) * prow) .* e2 .+ ((j - (ncols + 1) / 2) * pcol) .* e1
        c = collect(center) .+ off
        push!(cyls, Cylinder(center = Tuple(c), radius = radius, length = length,
                             axis = axis, ρ = ρv[k], T1 = T1v[k], T2 = T2v[k],
                             Δf = Δf, label = "r$(i)c$(j)"))
    end
    return cyls
end

# -----------------------------------------------------------------------------
# 3. Build a KomaMRI Phantom from a list of cylinders
# -----------------------------------------------------------------------------
"""
    build_phantom(cylinders; Δ = (1e-3, 1e-3, 1e-3), jitter = 0.0, name = "cylinders")

Sample each cylinder on a regular lattice with spacing `Δ = (dx, dy, dz)` [m]
and return a `Phantom` with one spin per lattice point inside a cylinder.
Later cylinders overwrite earlier ones where they overlap.
`jitter` (0–1) randomly displaces spins by that fraction of Δ, which reduces
aliasing/ringing artefacts from a perfectly regular lattice.

Rule of thumb: choose Δ ≲ half of your simulated voxel size, and keep the
total spin count in the 1e4–1e6 range for reasonable run times.
"""
function build_phantom(cylinders::Vector{Cylinder};
                       Δ = (1e-3, 1e-3, 1e-3), jitter = 0.0, name = "cylinders")
    Δv = collect(Float64.(Δ))
    # A global lattice anchored at the origin, so neighbouring cylinders share
    # lattice sites (makes overlap handling clean).
    owner = Dict{NTuple{3,Int},Int}()          # lattice index -> cylinder index
    for (ci, c) in enumerate(cylinders)
        h  = half_extents(c)
        lo = floor.(Int, (collect(c.center) .- h) ./ Δv)
        hi = ceil.(Int,  (collect(c.center) .+ h) ./ Δv)
        idx = [(i, j, k) for i in lo[1]:hi[1], j in lo[2]:hi[2], k in lo[3]:hi[3]]
        isempty(idx) && continue
        P = Float64[idx[n][d] * Δv[d] for d in 1:3, n in eachindex(idx)]
        for n in findall(inside(c, P))
            owner[idx[n]] = ci
        end
    end
    isempty(owner) && error("No spins fall inside any cylinder; check size vs. Δ.")

    keys_ = collect(keys(owner))
    N = length(keys_)
    x = zeros(N); y = zeros(N); z = zeros(N)
    ρ = zeros(N); T1 = zeros(N); T2 = zeros(N); Δw = zeros(N)
    for (n, key) in enumerate(keys_)
        c = cylinders[owner[key]]
        x[n], y[n], z[n] = key[1] * Δv[1], key[2] * Δv[2], key[3] * Δv[3]
        ρ[n], T1[n], T2[n] = c.ρ, c.T1, c.T2
        Δw[n] = 2π * c.Δf                      # rad/s
    end
    if jitter > 0
        x .+= (rand(N) .- 0.5) .* jitter * Δv[1]
        y .+= (rand(N) .- 0.5) .* jitter * Δv[2]
        z .+= (rand(N) .- 0.5) .* jitter * Δv[3]
    end
    return Phantom(; name = name, x = x, y = y, z = z, ρ = ρ,
                     T1 = T1, T2 = T2, T2s = copy(T2), Δw = Δw)
end

# -----------------------------------------------------------------------------
# 4. Scanner: approximate Siemens MAGNETOM Skyra
# -----------------------------------------------------------------------------
function skyra_scanner()
    return Scanner(
        B0     = 3.0,       # T
        B1     = 20e-6,     # T   (peak B1+ capability, ~20 µT; adjust to taste)
        Gmax   = 45e-3,     # T/m (Skyra: 45 mT/m)
        Smax   = 200.0,     # T/m/s (Skyra: 200 T/m/ms... i.e. 200 T/m/s slew)
        ADC_Δt = 2e-6,      # s   (minimum ADC dwell used for simulation grid)
        RF_Δt  = 1e-6,      # s
        GR_Δt  = 10e-6,     # s   (Siemens gradient raster)
    )
end

