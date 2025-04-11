import numpy as np
# import scipy as sc
import matplotlib as mpl
import matplotlib.pyplot as plt
# import matplotlib.mlab as mlab
from matplotlib.ticker import ScalarFormatter
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from uncertainties import unumpy as unp
from uncertainties import ufloat, umath

from options import *
from lib import *
from constants import *

nom_vals = unp.nominal_values
std_devs = unp.std_devs

mpl.rcParams.update(rcParams)

# mpl.rcParams['savefig.bbox'] = 'standard'
mpl.rcParams["figure.figsize"] = (36*INCH_PER_CM, 12*INCH_PER_CM)
# mpl.rcParams["figure.subplot.left"]   = 0.21
# mpl.rcParams['figure.subplot.right']  = 0.75
# mpl.rcParams['figure.subplot.top']    = 0.97
# mpl.rcParams['figure.subplot.bottom'] = 0.2

# ===== Params =====
datasets= ['250321-exp7', '250404-sand2', '250404-plastic6']
material_text_size = 22

# ===== Subplots =====
fig, axs = plt.subplots(1,3, 
                       layout='constrained', 
                       sharey='row',
                    #    gridspec_kw={'wspace': 0.1, 'hspace': 0.005}
                       )
# == padding ==
fig.get_layout_engine().set(w_pad=8 / 72, h_pad=4 / 72, 
                            hspace=0.0, wspace=0.0
                            )


# ===== Data analysis and plot =====
for i, dataset in enumerate(datasets):
    data = load(dataset)
    denoise_dataset(data, data.pop(-1))

    for j, step in enumerate(data): # Moving average filter
        window_size = 10
        step.psd = moving_average(step.psd, window_size)
        step.chi_im = moving_average(step.chi_im, window_size)

    kB_Teff = []

    max_amplitude = max(step.imposed_vibration for step in data)
    min_amplitude = min(step.imposed_vibration for step in data)
    cmap = truncate_colormap(plt.cm.Blues, 0.4, 1.0)
    norm = mpl.colors.Normalize(vmin=min_amplitude, vmax=max_amplitude)

    for k, step in enumerate(data[:-1]):
        kB_Teff.append((step.psd * 2*np.pi*step.freqs) / (4 * step.chi_im))
        # Teff.append(kB_Teff[i]/ BOLTZMANN_CONSTANT_JOULE)

        color = cmap(step.imposed_vibration / max_amplitude)
        axs[i].loglog(step.freqs, kB_Teff[k], c=color)
        plt.xlim(10,55)
        axs[i].set_xlabel(r"$f$ [Hz]")
        axs[0].set_ylabel(r"$k_B T_\textrm{eff}$ [J]")

    axs[i].xaxis.set_major_formatter(ScalarFormatter())
    # ax[i].xaxis.set_minor_formatter(ScalarFormatter())
    axs[i].set_xticks([10,20, 30, 40, 50])

    axs[i].set_xlim(10,55)

    # # This could become a function
    # axins1 = inset_axes(
    #     ax,
    #     width="10%",  # width: 50% of parent_bbox width
    #     height="5%",  # height: 5%
    #     # loc="upper left",
    #     bbox_to_anchor=(-0.83,-0.08, 1, 1),
    #     bbox_transform=ax.transAxes,
    # )

# ===== Annotations =====
axs[0].text(
            0.05,0.92, "Glass",
            size=material_text_size,
            horizontalalignment='left',
            verticalalignment='center',
            transform = axs[0].transAxes,
            bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=0.3')
            )
axs[1].text(
            0.05,0.92, "Sand",
            size=material_text_size,
            horizontalalignment='left',
            verticalalignment='center',
            transform = axs[1].transAxes,
            bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=0.3')
            )
axs[2].text(
            0.05,0.92, "Plastic",
            size=material_text_size,
            horizontalalignment='left',
            verticalalignment='center',
            transform = axs[2].transAxes,
            bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=0.3')
            )


clb = fig.colorbar(plt.cm.ScalarMappable(norm, cmap), ax=axs, label="Vibration amplitude [V]")
# clb.ax.set_xticks(ticks = [round(min_amplitude), round(max_amplitude)], minor=False)
# clb.ax.set_title("Vibration amplitude [V]", loc='left')

# plt.tight_layout()
plt.savefig("../figures/Teff_together.png")
