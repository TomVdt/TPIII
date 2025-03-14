import numpy as np
from matplotlib import mlab

import os
import json
import sys
from glob import glob
from pathlib import Path

NFFT = 1024
SAMPLE_RATE = 2_048_000

def load(dataset: Path):
    raw_data = np.fromfile(dataset, np.complex64)
    json_path = dataset.parent/dataset.name.replace("raw.dat", "params.json")
    with open(json_path, "r") as file:
        params = json.load(file)
    
    spectrum, frequencies = mlab.psd(raw_data, NFFT=NFFT, Fs=SAMPLE_RATE)
    frequencies += params['frequency']

    data = np.stack((frequencies, spectrum))

    return data


def main(argv):
    if len(argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_files_glob> <output_dir>")
        return

    outdir = Path(argv[2])
    if not outdir.is_dir():
        outdir = Path(outdir.parent)

    files = glob(argv[1])
    files.sort(key=os.path.getmtime)
    files = list(map(Path, files))

    for file in files:
        data = load(file)
        print(f"Saving {file} to {outdir/file.stem}")
        np.save(outdir/file.stem, data)


if __name__ == '__main__':
    main(sys.argv)
