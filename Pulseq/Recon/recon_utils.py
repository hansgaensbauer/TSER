import mapvbvd
import numpy as np 
import scipy.signal as sg
import scipy.optimize as opt

def load_TSER(file, points, echoes, channels = 15):
    twixObj = mapvbvd.mapVBVD(file)
    twixObj[1].image.squeeze = True #remove extra dimensions
    twixObj[1].image.flagRemoveOS = False #no readout oversampling
    data = twixObj[1].image[''].reshape(points,channels,-1, 2, echoes) # arrange data into (points, channels, slices, phase cycle, echoes)
    data_pc = data[:,:,:,0] + data[:,:,:,1] # add phase cycle steps to remove ringing

    # data_pc is phase cycled data with shape (points, channels, slices, echoes)
    return data_pc

def transform_and_scale(data):
    data_ft = np.fft.fftshift(np.fft.fft(np.fft.fftshift(data[3:-3,:,:,:], axes=(0)), axis=0), axes=(0))
    ## Sensitivity adjustment: add all coil signals together, scaled by the 5th echo amplitude for each coil
    # data_sa = data_ft[:,0,:,:]
    data_sa = np.einsum('jkhi,jkh->jhi', data_ft, np.conj(data_ft[:, :, :, 5]))
    return data_sa

def get_t2(echo_data, te):
    def _decay(x, a, b, c):
        return a * np.exp(-b * x)+c
    popt, _ = opt.curve_fit(_decay, np.arange(len(echo_data))*te, echo_data/np.max(echo_data))
    return 1/popt[1]

def get_peaks_t2s(data_sa, te=10e-3):
    n_slices = np.shape(data_sa)[1]
    slice_peaks = {}
    slice_t2s = {}
    ## full plate processing
    for slice_idx in range(n_slices):
        model = np.concatenate((np.zeros(2), np.ones(5), np.zeros(2)))
        target = np.convolve(np.abs(data_sa[:,slice_idx,5]), model)
        peaks, _ = sg.find_peaks(target, prominence=0.5*np.std(data_sa[:,0,5]))
        slice_peaks[slice_idx] = peaks - 4
        slice_t2s[slice_idx] = []
        for peak in slice_peaks[slice_idx]:
            slice_t2s[slice_idx].append(get_t2(np.abs(data_sa[peak,slice_idx,:]), te))

    return slice_peaks, slice_t2s

def find_first_row(slice_peaks_dict):
    #estimate first row position
    first_row_idx = np.inf
    for i in range(len(slice_peaks_dict.keys())):
        for peak in slice_peaks_dict[i]:
            if(peak < first_row_idx):
                first_row_idx = peak
    return first_row_idx

def assign_wells(data_sa, slice_peaks, slice_t2s, n_wells):
    n_slices = np.shape(data_sa)[1]
    first_row = find_first_row(slice_peaks)
    points = np.shape(data_sa)[0]
    points_per_well = points/n_wells

    #assign to wells
    well_t2s = np.full((n_slices, n_wells), np.nan)

    for i in range(n_slices):
        for peak_idx, peak in enumerate(slice_peaks[i]):
            points = peak - first_row
            well = int((points + points_per_well/2)/points_per_well)
            if(np.isnan(well_t2s[i, well])):
                well_t2s[i, well] = slice_t2s[i][peak_idx]
            else:
                print('two points fall in same well')
    return well_t2s

def process_to_array(data_sa, te=10e-3, n_wells=12, save=False, filename=None):
    peaks, peak_t2s = get_peaks_t2s(data_sa, te)
    well_t2s = assign_wells(data_sa, peaks, peak_t2s, n_wells)
    if(save):
        if(filename is None):
            filename = 'slicedata.csv'
        with open(filename, 'w+') as f:
            f.write('-,1,2,3,4,5,6,7,8,9,10,11,12\n')
            for i in range(len(well_t2s)):
                f.write(chr(65+i) + ',')
                for j in range(len(well_t2s[0])):
                    if(np.isnan(well_t2s[i,j])):
                        f.write('NA,')
                    else:
                        f.write("%.4f," % well_t2s[i,j])
                f.seek(f.tell() - 1)
                f.write('\n')
        # np.savetxt(filename, well_t2s, delimiter=',')
    return np.flipud(np.fliplr(well_t2s))
