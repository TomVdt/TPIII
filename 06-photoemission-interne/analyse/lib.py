from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import elementary_charge, k, h, c
from constants import *
from glob import glob


@dataclass
class Data:
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

def load(path: str) -> list[Data]:
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
            Data(
                filename=file,
                I=I[V>0],
                V=V[V>0],
                temperature=ufloat(T,err_T)
            )
        )
    return data

def resistance_to_temperature(ohm: float) -> float:
    return ohm * RESISTANCE_SLOPE + RESISTANCE_OFFSET

def wavelength_nm_to_energy(wavelength: float) -> float:
    return h * c / (wavelength * 1e-9) * EV_PER_JOULE

def curve_IV(I: np.ndarray[float], T, I_s, n, R) -> np.ndarray[float]:
    return (n*k*T / elementary_charge) * np.log(I/I_s + 1) + R*I

if __name__ == '__main__':
    print(resistance_to_temperature(109) - 273.15)