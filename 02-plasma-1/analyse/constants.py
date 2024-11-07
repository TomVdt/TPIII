from uncertainties import ufloat
from numpy import pi, mean

# Real constants
INCH_PER_CM = 2.54  # cm/inch
CM_PER_INCH = 1/2.54 # inch/cm

ELEMENTARY_CHARGE = 1.602_176_634e-19  # C
BOLTZMANN_CONSTANT_JOULE = 1.380_649e-23  # J/K
BOLTZMANN_CONSTANT_ELECTRONVOLT = 8.617333262e-5  # eV/K
ELECTRON_MASS = ufloat(9.109_383_7139e-31, 0.000_000_0028e-31)  # kg

SURFACE_PROBE = 1.26e-5  # m^2