# TSER
Turbo Spin Echo Relaxometry for Multi-Well Plates

## Background
MRI imaging sequences typically do not support the fast echo times required for high sensitivity CPMG $T_2$ measurements. This protocol uses a slice selective excitation followed by a standard CPMG echo train, with a readout gradient between each echo. These sequences can measure every sample in a 96 well plate in under two minutes, with an iron limit of detection better than 1uM. 

## Pulseq
### Generating a .seq File
1. Create a folder called `Sequences` in `Pulseq/Python`.
2. Create a folder within that folder called `Source`.
3. Create a virtual environment, then activate it.
4. `pip install -r Pulseq/Python/requirements.txt`
5. Run `Pulseq/Python/cpmg_1d_multislice.py` to generate a `.seq` file with the parameters defined at the top of `cpmg_1d_multislice.py`. A copy of the contents of `cpmg_1d_multislice.py` is saved in `Pulseq/Python/Sequences/Source/`, tagged with the same unique ID that is appended to the `.seq` filename.

### Reconstruction
1. Set up a virtual environment as above.
2. Create a folder called `Data` in `Pulseq/Recon`. Save the `.dat` files from the scanner here.
3. Run the reconstruction/analysis examples in `Pulseq/Recon/Recon.ipynb`.

## ParaVision

### Reconstruction
1. Make a folder inside the `ParaVision` directory called `Data`.
2. Inside that folder, create another folder called `Output`.
3. Copy the data folder from the scanner into the `Data` folder.
4. Create and activate a virtual environment.
5. `pip install -r ParaVision/Recon/requirements.txt`
6. `cpmg_recon.py` can be run from the command line. Run `python ParaVision/Recon/cpmg_recon.py --help` to get the list of arguments. 
7. For example: `python Recon/cpmg_recon.py --datafolder "Data/[Experiment Directory]" -e 3 -j 'localizer' -o Data/Output` runs the job 'localizer' on experiment 3 and saves the output image into the Data/Output folder.
8. `python Recon/cpmg_recon.py --datafolder "Data/[Experiment Directory]" -e 4 -j 'plotslice' -s 0 -o Data/Output` plots decays and a cross sections for the given slice.
9. To change the indices used for extracting decays, edit line 65 in `cpmg_recon.py`. To change the number of wells, edit line 34/35.
10. Once the decays look good, a command like `
`python Recon/cpmg_recon.py --datafolder "Data/[Experiment Directory]" -e 4 -j 't2s' -s 0 -o Data/Output` will compute T2 for each well in each slice and save the output to a .csv file. 
