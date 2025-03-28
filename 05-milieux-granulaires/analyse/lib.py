import numpy as np
from matplotlib import colors
from dataclasses import dataclass
from glob import glob
from scipy.ndimage import uniform_filter1d

@dataclass
class Step:
    filename: str
    imposed_vibration: float
    gamma: float
    step_time: float
    freqs: np.ndarray
    psd: np.ndarray
    chi_abs: np.ndarray
    chi_im: np.ndarray

# Load data
def load(dataset_name: str) -> list[Step]:
    metadata_file = glob(f'../data/{dataset_name}/*-exp?.txt')
    metadata = np.loadtxt(metadata_file[0], skiprows=1, delimiter='\t')

    data_files = glob(f'../data/{dataset_name}/*-exp?_step*.txt')
    data_files.sort(key=lambda s: int(s.split('step')[-1][:-4]))
    data: list[Step] = []

    for i, file in enumerate(data_files):
        try:
            freq, psd, chi_abs, chi_im = np.loadtxt(file, skiprows=1, delimiter='\t', unpack=True)
        except ValueError:
            print(f"WARNING: data is fucked for {file}")
            continue

        imposed_vibration, _, gamma, step_time, *_ = metadata[i]

        if np.allclose(chi_abs, 0): # Data is corrupted when freq_response contains only zeros
            print(f"WARNING: data is fucked for {file}")
            continue
        if np.allclose(freq, 0):
            print(f"WARNING: data is fucked for {file}, trying to recover freqs...")
            freq = np.arange(5, 70 + 0.0001, 0.1625)

        data.append(
            Step(
                file,
                imposed_vibration, gamma, step_time,
                freq, psd, chi_abs, np.abs(chi_im)
            )
        )
    
    return data

# Functions for fits
def modulus_chi(f: np.ndarray, I: float, w0: float, alpha: float) -> np.ndarray:
    w = 2 * np.pi * f
    return 1 / np.sqrt(
        (I * (w**2 - w0**2))**2 + (alpha * w)**2
    )

def imag_chi(f: np.ndarray, I: float, w0: float, alpha: float) -> np.ndarray:
    w = 2 * np.pi * f
    return alpha * w / (
        (I * (w**2 - w0**2))**2 + (alpha * w)**2
    )

def moving_average(spectrum: np.ndarray, window_size: int) -> np.ndarray:
    """
    Applies a moving average filter to the given spectrum.
    """
    return uniform_filter1d(spectrum, size=window_size, mode='nearest')

# https://stackoverflow.com/questions/18926031/how-to-extract-a-subset-of-a-colormap-as-a-new-colormap-in-matplotlib
def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap
