import numpy as np
import scipy as sc
from matplotlib import mlab

import os
import json
from glob import glob

from options import *
from constants import *


def load(dataset: str):
    raw_data = np.fromfile(dataset, np.complex64)
    with open(dataset.replace("raw.dat", "params.json"), "r") as file:
        params = json.load(file)
    
    spectrum, frequencies = mlab.psd(raw_data, NFFT=NFFT, Fs=SAMPLE_RATE)
    frequencies += params['frequency']

    return raw_data, (spectrum, frequencies), params

# data = []
freq = None

files = sorted(glob("../data/h_*.dat"))
files.sort(key=os.path.getmtime)

for file in files:
    _, (spectrum, freq), params = load(file)
    # params['l'] = ufloat(file.split('data/h_')[1].split('_')[0], 1)
    # data.append((spectrum, params))
    print(f"Saving {file}")
    np.save(file.replace(".dat", ""), spectrum)
