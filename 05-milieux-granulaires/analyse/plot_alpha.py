import numpy as np
import scipy as sc
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

from uncertainties import unumpy as unp
from uncertainties import ufloat, umath

from options import *
from lib import *
from constants import *

nom_vals = unp.nominal_values
std_devs = unp.std_devs

mpl.rcParams.update(rcParams)

# mpl.rcParams['savefig.bbox'] = 'standard'
mpl.rcParams["figure.figsize"] = (12*INCH_PER_CM, 12*INCH_PER_CM)
# mpl.rcParams["figure.subplot.left"]   = 0.21
# mpl.rcParams['figure.subplot.right']  = 0.75
# mpl.rcParams['figure.subplot.top']    = 0.97
# mpl.rcParams['figure.subplot.bottom'] = 0.2

# params
dir = "../data/"
c_glass = 'C0'
c_plastic = 'C3'
c_sand = 'C1'

# Data loading      # TODO: DESSINER FITS
glass_im = np.load(f"{dir}glass_alpha_im.npz", allow_pickle=True)
glass_im_amplitude, glass_im_alpha = glass_im["arr_0"], glass_im["arr_1"]
plastic_im = np.load(f"{dir}plastic_alpha_im.npz", allow_pickle=True)
plastic_im_amplitude, plastic_im_alpha = plastic_im["arr_0"], plastic_im["arr_1"]
sand_im = np.load(f"{dir}sand_alpha_im.npz", allow_pickle=True)
sand_im_amplitude, sand_im_alpha = sand_im["arr_0"], sand_im["arr_1"]


# Plot
fig, ax = plt.subplots(1,1)

plt.errorbar(glass_im_amplitude, nom_vals(glass_im_alpha),
             yerr=std_devs(glass_im_alpha),
             ls='', c=c_glass,
             label='Glass'
             )
plt.errorbar(plastic_im_amplitude, nom_vals(plastic_im_alpha),
             yerr=std_devs(plastic_im_alpha),
             ls='', c=c_plastic,
             label='Plastic'
             )
plt.errorbar(sand_im_amplitude, nom_vals(sand_im_alpha),
             yerr=std_devs(sand_im_alpha),
             ls='', c=c_sand,
             label='Sand'
             )

plt.yscale('log')
plt.xscale('log')
plt.xlabel(r'Oscillation amplitude [V]')
plt.ylabel(r'Friction coefficient $\alpha$')

ax.legend(bbox_to_anchor=(1.02,1))

plt.savefig('../figures/alpha_together.png', bbox_inches='tight')

# plt.show()