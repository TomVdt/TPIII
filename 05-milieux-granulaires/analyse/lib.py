import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from uncertainties import Variable
from uncertainties import unumpy as unp
from dataclasses import dataclass
from glob import glob
import warnings
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
    metadata_file = glob(f'../data/{dataset_name}/*-*.txt')
    metadata_file = min(metadata_file, key=len)
    metadata = np.loadtxt(metadata_file, skiprows=1, delimiter='\t')
    assert metadata.shape[0] < 50

    data_files = glob(f'../data/{dataset_name}/*-*_step*.txt')
    data_files.sort(key=lambda s: int(s.split('step')[-1][:-4]))
    data: list[Step] = []

    prev_freq = None
    for i, file in enumerate(data_files):
        try:
            with warnings.catch_warnings(record=True):
                freq, psd, chi_abs, chi_im = np.loadtxt(file, skiprows=1, delimiter='\t', unpack=True)
        except ValueError:
            print(f"WARNING: data is fucked for {file}")
            continue

        imposed_vibration, _, gamma, step_time, *_ = metadata[i]

        if np.allclose(chi_abs, 0): # Data is corrupted when freq_response contains only zeros
            print(f"WARNING: data is fucked for {file}")
            continue
        if np.allclose(freq, 0):
            print(f"WARNING: data is fucked for {file}, trying to recover freqs... ", end='')
            if prev_freq is not None:
                print("Used previous freqs")
                freq = prev_freq.copy()
            else:
                print("Generated artificial freqs between 5 and 70")
                freq = np.arange(5, 70 + 0.0001, 0.1625)

        data.append(
            Step(
                filename=file,
                imposed_vibration=imposed_vibration, gamma=gamma, step_time=step_time,
                freqs=freq, psd=psd, chi_abs=chi_abs, chi_im=np.abs(chi_im)
            )
        )
        prev_freq = freq
    
    return data

def denoise_dataset(dataset: list[Step], noise: Step) -> None:
    for step in dataset:
        step.psd /= noise.psd

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

# Doing fits
def do_fit_alpha(dataset: list[Step], alpha_with_err: np.ndarray) -> tuple[Variable, Variable]:
    amplitude = np.array([step.imposed_vibration for step in dataset])
    alpha = unp.nominal_values(alpha_with_err)
    alpha_err = unp.std_devs(alpha_with_err)

    plt.errorbar(amplitude, alpha, yerr=alpha_err, ls='none')

    coefs, cov = np.polyfit(np.log(amplitude), np.log(alpha), 1, cov=True)
    xx = np.linspace(min(amplitude), max(amplitude), 50)
    yy = np.exp(np.polyval(coefs, np.log(xx)))
    plt.plot(xx, yy)
    
    coefs_err = unp.uarray(coefs, np.sqrt(np.diag(cov)))
    return coefs_err

# Utils
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
