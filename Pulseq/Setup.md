# Pulseq Setup

## Python

1. Install `numpy`, `matplotlib`, `pymapvbvd`, and `pypulseq`.
2. In the `Python` subdirectory, create the subdirectory `Sequences` and `Sequences\Source`.
3. In the `Recon` subdirectory, create a the subdirectory `Data`.
4. Change the parameters in `cpmg_1d_multislice.py` to define the experiment you want
5. Run `cpmg_1d_multislice.py`. This will generate a .seq file in `Sequences`, and a copy of the source code in `Sequences\Source` with a matching unique id. 
6. An example reconstruction is provided in `Recon`. Place .data files from the scanner in the `Data` subdirectory, which is gitignored.