# In[]:
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
mpl.rcParams["figure.figsize"] = (25*INCH_PER_CM, 8*INCH_PER_CM)
# mpl.rcParams["figure.subplot.left"]   = 0.21
# mpl.rcParams['figure.subplot.right']  = 0.75
# mpl.rcParams['figure.subplot.top']    = 0.97
# mpl.rcParams['figure.subplot.bottom'] = 0.2
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.spines.top'] = False

# params
data = load('250404-plastic6')
noise = data.pop(-1)
fits = np.load('../data/fit_chi_abs.npy')

chosen1 = data[0]
chosen2 = data[4]
chosen3 = data[8]
all_chosen = [chosen1, chosen2, chosen3]
# idx = np.nonzero(np.logical_and(chosen1.freqs > 5, chosen1.freqs < 55))

figax = plt.subplots(nrows=1, ncols=2, sharey='row')
fig = figax[0]
ax: list[mpl.axes.Axes] = figax[1]

cmap = truncate_colormap(plt.cm.Blues, 0.4, 1.0)
max_brrrrrrrr = data[0].imposed_vibration
norm = mpl.colors.Normalize(vmin=data[-1].imposed_vibration, vmax=data[0].imposed_vibration)
for chosen in all_chosen:
    chi_abs = moving_average(chosen.chi_abs, 3)
    ax[0].loglog(chosen.freqs, chi_abs, c=cmap(chosen.imposed_vibration/ max_brrrrrrrr))

for step, (I, omega, alpha) in zip(data, fits):
    x = np.linspace(10, 55, endpoint=True)
    y = modulus_chi(x, I, omega, alpha)
    ax[1].loglog(x, y, c=cmap(step.imposed_vibration/ max_brrrrrrrr))

lims = ax[1].get_xlim()
ax[1].set_xlim(lims[0], 80)
# lims = ax[0].get_ylim()
# ax[0].set_ylim(1e-2, lims[1])
# ax[1].set_ylim(1e-2, lims[1])

ax[1].annotate(
    'Increasing\namplitude', (65, 1e-1), (65, 1),
    horizontalalignment="center", verticalalignment="center",
    arrowprops=dict(
        arrowstyle='<-', color="k",
    ))

arr = ax[1].annotate(
    '',
    xy=(65, 1e-1), xycoords=ax[0].transData,
    xytext=(15, 2e-1), textcoords=ax[1].transData,
    # horizontalalignment="center", verticalalignment="center",
    annotation_clip=False,
    arrowprops=dict(
        arrowstyle='<-', color="k",
        connectionstyle="arc3,rad=-0.2"
    ))
ax[1].annotate("Fits", (.5, .5), xycoords=arr, ha='center', va='bottom')


ax[0].xaxis.minorticks_off()
ax[1].xaxis.minorticks_off()
ax[0].xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
ax[1].xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
ax[0].set_xticks([10,20,30,40,50])
ax[1].set_xticks([10,20,30,40,50])
ax[1].yaxis.set_visible(False)
ax[1].spines['left'].set_visible(False)

ax[0].set_xlabel(r"Frequency [Hz]")
ax[1].set_xlabel(r"Frequency [Hz]")
ax[0].set_ylabel(r"$|\chi|$ [rad$^{2}$ Hz$^{-1}$]")

plt.tight_layout()
plt.savefig('../figures/plastic_chi_abs_with_fit.png')
plt.show()
