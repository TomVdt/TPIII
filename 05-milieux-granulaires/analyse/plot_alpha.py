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

# params
dir = "../data/"

# Data loading
glass_im = np.load(f"{dir}glass_alpha_im.npz", allow_pickle=True)
glass_im_amplitude, glass_im_alpha = glass_im["arr_0"], glass_im["arr_1"]


# Plot
plt.errorbar(glass_im_amplitude, nom_vals(glass_im_alpha),
             yerr=std_devs(glass_im_alpha),
             ls=''
             )

plt.yscale('log')
plt.xscale('log')
plt.xlabel(r'Oscillation amplitude [V]')
plt.ylabel(r'Friction coefficient $\alpha$')

plt.tight_layout()
plt.savefig('../figures/alpha_together.png')

plt.show()