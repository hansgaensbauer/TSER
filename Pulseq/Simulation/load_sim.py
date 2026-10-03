"""Load KomaMRI simulation output (from run_sim.jl) and the saved phantom.

    pip install h5py numpy
    python load_sim.py sim_output.h5 [cylinders.phantom]
"""
import sys
import h5py
import numpy as np


def load_sim(path):
    with h5py.File(path, "r") as f:
        signal = f["signal_real"][()] + 1j * f["signal_imag"][()]   # (Nsamples, Ncoils)
        out = {
            "signal": signal,
            "t_adc": f["t_adc"][()] if "t_adc" in f else None,           # seconds
            "kspace": f["kspace_adc"][()] if "kspace_adc" in f else None,  # (Nsamples, >=3), 1/m
            "attrs": dict(f.attrs),
        }
    return out


def inspect_phantom(path):
    """Phantom files are HDF5; this just lists what's inside."""
    with h5py.File(path, "r") as f:
        def show(name, obj):
            if isinstance(obj, h5py.Dataset):
                print(f"  {name}: shape={obj.shape}, dtype={obj.dtype}")
        f.visititems(show)


if __name__ == "__main__":
    d = load_sim(sys.argv[1])
    print("signal:", d["signal"].shape, d["signal"].dtype)
    print("t_adc:", None if d["t_adc"] is None else d["t_adc"].shape)
    print("kspace:", None if d["kspace"] is None else d["kspace"].shape)
    print("attrs:", d["attrs"])
    if len(sys.argv) > 2:
        print("phantom contents:")
        inspect_phantom(sys.argv[2])
