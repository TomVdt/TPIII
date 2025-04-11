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


# ===== params =====
dir = "../data/"
c_glass = 'C0'
c_plastic = 'C3'
c_sand = 'C1'
fit_text_size = 14
material_text_size = 14

# ===== Data loading =====
glass_im = np.load(f"{dir}glass_alpha_im.npz", allow_pickle=True)
glass_im_amplitude, glass_im_alpha, glass_im_coefs, glass_im_cov = glass_im["arr_0"], glass_im["arr_1"], glass_im["arr_2"], glass_im["arr_3"]
plastic_im = np.load(f"{dir}plastic_alpha_im.npz", allow_pickle=True)
plastic_im_amplitude, plastic_im_alpha, plastic_im_coefs, plastic_im_cov = plastic_im["arr_0"], plastic_im["arr_1"], plastic_im["arr_2"], plastic_im["arr_3"]
sand_im = np.load(f"{dir}sand_alpha_im.npz", allow_pickle=True)
sand_im_amplitude, sand_im_alpha, sand_im_coefs, sand_im_cov = sand_im["arr_0"], sand_im["arr_1"], sand_im["arr_2"], sand_im["arr_3"]


# ===== Errorbars =====
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

# ===== Fits =====
offset = 0.6

xx_glass = np.linspace(min(glass_im_amplitude), glass_im_amplitude[-7], 50)
yy_glass = np.exp(np.polyval(glass_im_coefs, np.log(xx_glass)))
plt.plot(xx_glass, yy_glass * offset,
         c=c_glass)

xx_plastic = np.linspace(min(plastic_im_amplitude), plastic_im_amplitude[-9], 50)
yy_plastic = np.exp(np.polyval(plastic_im_coefs, np.log(xx_plastic)))
plt.plot(xx_plastic, yy_plastic*offset,
         c=c_plastic)

xx_sand = np.linspace(min(sand_im_amplitude), sand_im_amplitude[-5], 50)
yy_sand = np.exp(np.polyval(sand_im_coefs, np.log(xx_sand)))
plt.plot(xx_sand, yy_sand*offset,
         c=c_sand)

# ===== Annotations =====
# == Materials ==
plt.text(2e0, 3e-3, "Sand",
         c=adjust_lightness(c_sand, 1),
         size=material_text_size
         )
plt.text(2e0, 3e-4, "Glass",
         c=adjust_lightness(c_glass, 1),
         size=material_text_size
         )
plt.text(5e-1, 2e-2, "Plastic",
         c=adjust_lightness(c_plastic,1),
         size=material_text_size
         )

# == Slope ==
position_on_line = 3
additional_offset=0.65

plt.text(xx_glass[position_on_line], yy_glass[position_on_line]*offset*additional_offset,
         f"$\\sim {glass_im_coefs[0]:.2f}$", size=fit_text_size,
         rotation=-42,
         rotation_mode='anchor',
        #  c=c_glass
         )
plt.text(xx_sand[position_on_line], yy_sand[position_on_line]*offset*additional_offset,
         f"$\\sim {sand_im_coefs[0]:.2f}$", size=fit_text_size,
         rotation=-42,
         rotation_mode='anchor',
        #  c=c_sand
         )
plt.text(xx_plastic[position_on_line], yy_plastic[position_on_line]*offset*additional_offset,
         f"$\\sim {plastic_im_coefs[0]:.2f}$", size=fit_text_size,
         rotation=-33,
         rotation_mode='anchor',
        #  c=c_plastic
         )

# ===== Figure =====
plt.yscale('log')
plt.xscale('log')
plt.xlabel(r'Oscillation amplitude [V]')
plt.ylabel(r'Friction coefficient $\alpha$ [kg m$^2$ s$^{-1}$]')

# ax.legend(bbox_to_anchor=(0.5,0.5))

plt.savefig('../figures/alpha_together.png', bbox_inches='tight')