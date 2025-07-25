from uncertainties import ufloat
from numpy import pi, log10
from scipy.constants import lambda2nu, hbar
# Real constants
CM_PER_INCH = 2.54  # cm/inch
INCH_PER_CM = 1/2.54 # inch/cm
EV_PER_JOULE = 6.241509e+18  # eV / J

# Calibration
RESISTANCE_73K = 18.49
RESISTANCE_303K = 111.67
RESISTANCE_SLOPE = (303 - 73) / (RESISTANCE_303K - RESISTANCE_73K)  # dT/dR
RESISTANCE_OFFSET = 303 - RESISTANCE_SLOPE * RESISTANCE_303K

# Actual constant

A_G = 1.12e6  # A / m² / K² [notice]
A = ufloat(0.9e-4,6.726812023536856e-05)   # m² [aire de la diode] 0.0009+/-6.726812023536856e-05