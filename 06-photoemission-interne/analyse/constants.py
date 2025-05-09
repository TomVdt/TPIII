from uncertainties import ufloat
from numpy import pi, log10

# Real constants
CM_PER_INCH = 2.54  # cm/inch
INCH_PER_CM = 1/2.54 # inch/cm

# Calibration
RESISTANCE_73K = 18.49
RESISTANCE_303K = 111.67
RESISTANCE_SLOPE = (303 - 73) / (RESISTANCE_303K - RESISTANCE_73K)  # dT/dR
RESISTANCE_OFFSET = 303 - RESISTANCE_SLOPE * RESISTANCE_303K
