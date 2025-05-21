from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import elementary_charge, k, h, c
from constants import *
from glob import glob


@dataclass
class IV:
    filename: str
    I: np.ndarray[float]
    V: np.ndarray[float]
    temperature: ufloat

@dataclass
class Calibration:
    sensor: str
    filter: int
    min_lambda: float
    max_lambda: float
    lambd: np.ndarray[float]
    intensity: np.ndarray[float]

@dataclass
class Photocurrent:
    min_lambda: float
    max_lambda: float
    lambd: np.ndarray[float]
    intensity: np.ndarray[float]
    E: np.ndarray[float]

def load_IV(path: str) -> list[IV]:
    data_files = glob(f'../data/{path}/*.tsv')
    data_files.sort()
    data = []
    for i, file in enumerate(data_files):
        # print(file, i)
        # V [V], I [mA]
        V, I = np.loadtxt(file, delimiter='\t', unpack=True, converters=lambda s: s.replace(',', '.'))
        # Extract temperature (Ohm)
        ohm_lower, ohm_upper, *_ = map(float, file.split("/")[-1][:-4].split('-'))
        T = (resistance_to_temperature(ohm_lower) + resistance_to_temperature(ohm_upper)) / 2
        err_T = abs(resistance_to_temperature(ohm_lower) - resistance_to_temperature(ohm_upper)) / 2
        data.append(
            IV(
                filename=file,
                I=I[V>0],
                V=V[V>0],
                temperature=ufloat(T,err_T)
            )
        )
    return data

def load_calibration(path: str) -> list[Calibration]:
    data_files = glob(f'../data/{path}/*.tsv')
    data_files.sort()
    dataset: list[Calibration] = []
    for i, file in enumerate(data_files):
        _, t, signal, _ = np.loadtxt(file, unpack=True, delimiter="\t", converters=lambda s: s.replace(',', '.'))
        sensor, filterr, lower, upper = file.split('/')[-1][:-4].split('-')
        lower = int(lower)
        upper = int(upper)
        filterr = int(filterr)

        data = Calibration(
            sensor=sensor, filter=filterr, min_lambda=lower, max_lambda=upper,
            lambd=np.linspace(lower, upper, len(t), endpoint=True),
            intensity=signal
        )

        dataset.append(data)
    return dataset

def load_photocurrent(path:str) -> list[Photocurrent]:
    data_files = glob(f'../data/{path}/*.tsv')
    data_files.sort()
    dataset: list[Calibration] = []
    for i, file in enumerate(data_files):
        _, t, signal, _ = np.loadtxt(file, unpack=True, delimiter="\t", converters=lambda s: s.replace(',', '.'))
        test_lower = 200
        test_upper = 2600
        lambd = np.linspace(test_lower, test_upper, len(t), endpoint=True) # [nm]
        E = h * c / (lambd*1e-9) * EV_PER_JOULE # [eV]

        dataset.append(Photocurrent(test_lower, test_upper, lambd, signal, E))
    return dataset
    
def resistance_to_temperature(ohm: float) -> float:
    return ohm * RESISTANCE_SLOPE + RESISTANCE_OFFSET

def wavelength_nm_to_energy(wavelength: float) -> float:
    return h * c / (wavelength * 1e-9) * EV_PER_JOULE

def curve_IV(I: np.ndarray[float], T, I_s, n, R) -> np.ndarray[float]:
    return (n*k*T / elementary_charge) * np.log(I/I_s + 1) + R*I

if __name__ == '__main__':
    print(resistance_to_temperature(109) - 273.15)