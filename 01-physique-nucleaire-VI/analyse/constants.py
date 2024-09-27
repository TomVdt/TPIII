from uncertainties import ufloat
from numpy import pi, mean

# Real constants
CM_PER_INCH = 2.54  # cm/inch
INCH_PER_CM = 1/2.54 # inch/cm

GAMMA_CS137 = 662  # keV
GAMMA_PB210 = 46.5  # keV
GAMMA_CO57 = 136.4  # keV
GAMMA_HF181 = 482 - 136  # keV

# Uncertainties
ERROR_ATTENUATION_COUNT = 0.01  # %
ERROR_TIME = 0.1  # s
ERROR_THICC = 1e-3  # mm