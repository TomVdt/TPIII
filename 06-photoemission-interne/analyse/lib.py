from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import elementary_charge, k
from glob import glob


@dataclass
class Data:
    filename: str
    I: np.ndarray[float]
    V: np.ndarray[float]
    temperature: float

def load(path: str) -> list[Data]:
    data_files = glob(f'../data/{path}/*.tsv')
    data_files.sort()
    data = []
    for i, file in enumerate(data_files):
        # V [V], I [mA]
        V, I = np.loadtxt(file, delimiter='\t', unpack=True,converters=lambda s: s.replace(',', '.'))
        data.append(
            Data(
                filename=file,
                I=I[V>0],
                V=V[V>0],
                temperature=300
            )
        )
    return data

def plot_IV(data: Data):
    plt.plot(data.V, data.I)
    plt.xlabel('Tension [V]')
    plt.ylabel('Current [mA]')


def curve_IV(I: np.ndarray[float], T, I_s, n, R) -> np.ndarray[float]:
    return (n*k*T / elementary_charge) * np.log(I/I_s + 1) + R*I