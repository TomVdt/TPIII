from uncertainties import ufloat
import numpy as np
from matplotlib import colors

# Real constants
CM_PER_INCH = 2.54  # cm/inch
INCH_PER_CM = 1/2.54 # inch/cm

BOLTZMANN_CONSTANT_JOULE = 1.380_649e-23  # J/K


# https://stackoverflow.com/questions/18926031/how-to-extract-a-subset-of-a-colormap-as-a-new-colormap-in-matplotlib
def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap
