from uncertainties import ufloat
from numpy import pi, mean

# Real constants
CM_PER_INCH = 2.54  # cm/inch

GAMMA_CS137 = 0.662  # MeV
GAMMA_PB210 = 0.0465  # MeV
GAMMA_CO57 = 0.1364  # MeV
GAMMA_NA22 = 1.275  # MeV
GAMMA_HF181 = 0.482 - 0.136  # MeV

# Uncertainties
ERROR_ATTENUATION_COUNT = 0.01  # %
ERROR_TIME = 0.1  # s
ERROR_THICC = 1e-3  # mm