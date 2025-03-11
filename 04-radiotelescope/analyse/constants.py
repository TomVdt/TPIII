from uncertainties import ufloat
from numpy import pi, log10

# Real constants
CM_PER_INCH = 2.54  # cm/inch
INCH_PER_CM = 1/2.54 # inch/cm

# FFT
NFFT = 1024
SAMPLE_RATE = 2_048_000

# Galactic
H21 = 1.420405751768e9  # Hz
METERS_PER_PARSEC = 3.0857e16
R0 = 8.5  # kpc, IAU
V0 = 220e3  # m/s, source: IAU apparently, unable to find
OORT_A = ufloat(15.3e3, 0.4e3)  # m s−1 kpc−1

# Using dB scale
# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.psd.html
# dB = 10 * log10(amplitude)
def to_dB(x):
    return 10 * log10(x)

def deg2rad(deg: float) -> float:
    return pi * deg / 180