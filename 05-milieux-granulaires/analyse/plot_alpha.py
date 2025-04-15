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

mpl.rcParams['savefig.bbox'] = 'standard'
mpl.rcParams["figure.figsize"] = (12*INCH_PER_CM, 12*INCH_PER_CM)
mpl.rcParams["figure.subplot.left"]   = 0.2
mpl.rcParams['figure.subplot.right']  = 0.98
mpl.rcParams['figure.subplot.top']    = 0.98
mpl.rcParams['figure.subplot.bottom'] = 0.15


# ===== params =====
dir = "../data/"
source="im" # modulus or im
c_glass = 'C0'
c_plastic = 'C3'
c_sand = 'C1'
c_box_glass = 'black'
c_box_plastic = 'black'
c_box_sand = 'black'
fit_text_size = 14
material_text_size = 16
material_text_padding=0.2

# ===== Data loading =====
glass = np.load(f"{dir}glass_alpha_{source}.npz", allow_pickle=True)
glass_amplitude, glass_alpha, glass_coefs, glass_cov = glass["arr_0"], glass["arr_1"], glass["arr_2"], glass["arr_3"]
plastic = np.load(f"{dir}plastic_alpha_{source}.npz", allow_pickle=True)
plastic_amplitude, plastic_alpha, plastic_coefs, plastic_cov = plastic["arr_0"], plastic["arr_1"], plastic["arr_2"], plastic["arr_3"]
sand = np.load(f"{dir}sand_alpha_{source}.npz", allow_pickle=True)
sand_amplitude, sand_alpha, sand_coefs, sand_cov = sand["arr_0"], sand["arr_1"], sand["arr_2"], sand["arr_3"]


# ===== Errorbars =====
fig, ax = plt.subplots(1,1)

plt.errorbar(glass_amplitude, nom_vals(glass_alpha),
             yerr=std_devs(glass_alpha),
             ls='', c=c_glass,
             label='Glass'
             )
plt.errorbar(plastic_amplitude, nom_vals(plastic_alpha),
             yerr=std_devs(plastic_alpha),
             ls='', c=c_plastic,
             label='Plastic'
             )
plt.errorbar(sand_amplitude, nom_vals(sand_alpha),
             yerr=std_devs(sand_alpha),
             ls='', c=c_sand,
             label='Sand'
             )

# ===== Fits =====
offset = 0.6

xx_glass = np.linspace(min(glass_amplitude), glass_amplitude[-7], 50)
yy_glass = np.exp(np.polyval(glass_coefs, np.log(xx_glass)))
plt.plot(xx_glass, yy_glass * offset,
         c=c_glass)

xx_plastic = np.linspace(min(plastic_amplitude), plastic_amplitude[-9], 50)
yy_plastic = np.exp(np.polyval(plastic_coefs, np.log(xx_plastic)))
plt.plot(xx_plastic, yy_plastic*offset,
         c=c_plastic)

xx_sand = np.linspace(min(sand_amplitude), sand_amplitude[-5], 50)
yy_sand = np.exp(np.polyval(sand_coefs, np.log(xx_sand)))
plt.plot(xx_sand, yy_sand*offset,
         c=c_sand)

# ===== Annotations =====
# == Materials ==
plt.text(2e0,2e-3, "Sand",
         c=c_box_sand,
         size=material_text_size,
         bbox=dict(facecolor='none', edgecolor=c_box_sand, boxstyle=f'round,pad={material_text_padding}')
         )
plt.text(2e0, 3.5e-4, "Glass",
         c=c_box_glass,
         size=material_text_size,
         bbox=dict(facecolor='none', edgecolor=c_box_glass, boxstyle=f'round,pad={material_text_padding}')
         )
plt.text(5e-1, 2e-2, "Plastic",
         c=c_box_plastic,
         size=material_text_size,
         bbox=dict(facecolor='none', edgecolor=c_box_plastic, boxstyle=f'round,pad={material_text_padding}')
         )

# == Slope ==
position_on_line = 3
additional_offset=0.65

plt.text(xx_glass[position_on_line], yy_glass[position_on_line]*offset*additional_offset,
         f"$\\sim {glass_coefs[0]:.2f}$", size=fit_text_size,
         rotation=-42,
         rotation_mode='anchor',
        #  c=c_glass
         )
plt.text(xx_sand[position_on_line], yy_sand[position_on_line]*offset*additional_offset,
         f"$\\sim {sand_coefs[0]:.2f}$", size=fit_text_size,
         rotation=-42,
         rotation_mode='anchor',
        #  c=c_sand
         )
plt.text(xx_plastic[position_on_line], yy_plastic[position_on_line]*offset*additional_offset,
         f"$\\sim {plastic_coefs[0]:.2f}$", size=fit_text_size,
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

plt.savefig('../figures/alpha_together.png')