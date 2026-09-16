import argparse
import numpy as np
from scipy.optimize import curve_fit
import brkraw
import matplotlib.pyplot as plt

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--expno', '-e', type=int, help='Experiment number')
    parser.add_argument('--datafolder', type=str, help='Data directory')
    parser.add_argument('--job', '-j', help='Output type. \'all\', \'localizer\', \'plotslice\', \'info\'')
    parser.add_argument('--slice', '-s', type=int, help='Slice for plotting/recon')
    parser.add_argument('--out', '-o', help='Output directory', default='Output')

    args = parser.parse_args()

    def fit_t2(y, et):
        # Define decay function
        def decay_fn(TE, a, b):
            return a * np.exp(-b * TE)

        try:
            p0 = [y.max() - y.min(), 0.01]
            params, _ = curve_fit(decay_fn, et, y, p0=p0, maxfev=5000)
            return 1/params[1]
        except RuntimeError:
            return(np.nan)
        
    #TODO: get echoes, points, etc from acqpars file
    echo_time = -1
    npts = -1
    nechoes = -1
    nslices = -1
    nwells = 4
    # nwells = 3
    fov=-1

    if args.job != "localizer":
        method_file = args.datafolder + '/' + str(args.expno) + '/method'
        with open(method_file, 'r') as mf:
            for line in mf:
                if("##$PVM_EchoTime" in line):
                    echo_time = int(line.split("=")[-1])/1000.0
                    print(f'Echo Time: {(echo_time*1000):.2f}ms')
                elif("##$NPts" in line):
                    npts = int(line.split("=")[-1])
                    print(f'NPts: {npts}')
                elif("##$NEchoes" in line):
                    nechoes = int(line.split("=")[-1])
                    print(f'NEchoes: {nechoes}')
                elif("##$PVM_Fov=(" in line):
                    fov = int(next(mf))
                    print(f'FOV: {fov}')
        acqp_file = args.datafolder + '/' + str(args.expno) + '/acqp'
        with open(acqp_file, 'r') as pf:
            for line in pf:
                if("##$NSLICES" in line):
                    nslices = int(line.split("=")[-1])
                    print(f'NSlices: {nslices}')

        t = np.arange(nechoes)*echo_time

        #TODO: automatically detect well center indices
        well_centerindices = [3,12,20,26]
        # well_centerindices = [7,15,26]

        raw = np.fromfile(args.datafolder + '/' + str(args.expno) + '/rawdata.job0', dtype=np.int32)
        raw_phased = (raw[0::2] + 1j * raw[1::2]).reshape(2, nslices,nechoes,2,npts)
        data = raw_phased[0] + raw_phased[1]
        data_ft = np.fft.fftshift(np.fft.fft(np.fft.fftshift(data, axes=-1), axis=-1), axes=-1)

    if(args.job == 'all' or args.job == 'localizer'):
        pvdset = brkraw.load(args.datafolder)
        niiobj1 = pvdset.convert(args.expno, reco_id=1)
        slices = niiobj1[1].dataobj.shape[2]
        index = slices // 2

        fig, ax = plt.subplots(1, 1)
        img = ax.imshow(niiobj1[2].dataobj[:, :, index].T, cmap="gray", origin="lower")
        plt.savefig(args.out + '/localizer.png')

    if(args.job == 'all' or args.job == 't2s'):
        tf = plt.figure()

        t2s = np.empty((nslices, nwells))
        for slice in range(nslices):
            for well in range(nwells):
                t2s[slice, well] = fit_t2(np.abs(data_ft[slice,30:,0,well_centerindices[well]]), t[30:])
        
        with open(args.out + '/t2data.csv', 'w+') as f:
            f.write('Slice,')
            for well in range(nwells):
                if(well < nwells - 1):
                        f.write(f"{str(well + 1)}" + ',')
                else:
                    f.write(f"{str(well + 1)}" + '\n')   
            for slice in range(nslices):
                f.write(str(slice) + ', ')
                for well in range(nwells):
                    if(well < nwells - 1):
                        f.write(f"{t2s[slice, well]:.4f}" + ',')
                else:
                    f.write(f"{t2s[slice, well]:.4f}" + '\n')

    if(args.job == 'plotslice'):
        tn, ax = plt.subplots(1,2, figsize=(9,5))
        for well in range(nwells):
            ax[0].plot(t[30:], 
                       (np.abs(data_ft[args.slice,30:,0,well_centerindices[well]])),
                        label=str(well + 1))
        dim = np.linspace(-fov/2, fov/2, npts)
        ax[1].plot(dim, np.abs(data_ft[args.slice,0,0,:]), '.')
        ax[1].plot(dim, np.abs(data_ft[args.slice,0,0,:]))
        ax[1].set_xlabel("RO (mm)")
        ax[1].set_title("Slice Cross Section")
        ax[0].set_title("Well Decays")
        ax[0].set_xlabel("Time (s)")
        ax[0].legend()
        plt.savefig(args.out + f'/slice{args.slice}.png')