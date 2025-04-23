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
mpl.rcParams["figure.figsize"] = (14*INCH_PER_CM, 12*INCH_PER_CM)
# mpl.rcParams["figure.subplot.left"]   = 0.21
# mpl.rcParams['figure.subplot.right']  = 0.75
# mpl.rcParams['figure.subplot.top']    = 0.97
# mpl.rcParams['figure.subplot.bottom'] = 0.2
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.spines.top'] = False

# params
data = load('250404-sand2')

chosen1 = data[0]
chosen2 = data[14]
chosen3 = data[15]
chosen4 = data[17]
all_chosen = [chosen1, chosen2, chosen3, chosen4]

# ==== Data plot =====
cmap = truncate_colormap(plt.cm.Blues, 0.4, 1.0)
norm = mpl.colors.Normalize(vmin=chosen4.imposed_vibration, vmax=chosen1.imposed_vibration)
for chosen in all_chosen:
    plt.loglog(chosen.freqs, chosen.psd, c=cmap(chosen.imposed_vibration))

# ==== Annotation arrow ====
lims = plt.xlim()
plt.xlim(lims[0], 80)
plt.annotate(
    'Increasing\namplitude', (65, 7e-4), (65, 1.3e-2),
    horizontalalignment="center", verticalalignment="center",
    arrowprops=dict(
        arrowstyle='<-', color="k",
    ))

# ==== Ticks ====
ax = plt.gca()
ax.xaxis.minorticks_off()
ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
plt.xticks([10,20,30,40,50])
# plt.xticks([10])
plt.xlabel(r"Frequency [Hz]")
plt.ylabel(r"PSD [rad$^{2}$ Hz$^{-1}$]")

# ==== Material label ====
material_text_size=16
material_text_position = (0.04, 0.07)
material_text_padding=0.18
ax.text(
            material_text_position[0],material_text_position[1], "Sand",
            size=material_text_size,
            horizontalalignment='left',
            verticalalignment='center',
            transform = ax.transAxes,
            bbox=dict(facecolor='none', edgecolor='black', boxstyle=f'round,pad={material_text_padding}')
            )


plt.tight_layout()
plt.savefig('../figures/sand_psd_nice.png')
plt.show()
