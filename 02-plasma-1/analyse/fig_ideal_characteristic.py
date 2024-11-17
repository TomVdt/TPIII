import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from options import *
from constants import *
mpl.rcParams.update(rcParams)
p=plt.rcParams
p["figure.figsize"] = (5.75*CM_PER_INCH, 6.5*CM_PER_INCH)
p['lines.color'] =  'black'
p['lines.linewidth'] = 1

sep_styles = '--'
sep_lw = 0.5
annotate_style = '--'
annotate_lw = 0.75

ion_saturation = 1
# electron_saturation = 4
V_bias = 0.5

boundaries = [-2, 2, 9, 12]
plt.xlim(boundaries[0], boundaries[-1])
plt.ylim(-2, 22)

ion_saturation_x = np.linspace(boundaries[0], boundaries[1], 50)
exp_x = np.linspace(boundaries[1], boundaries[2], 50)
electron_saturation_x = np.linspace(boundaries[2], boundaries[3], 50)

def f(x):
    return np.exp(x - 6) - 1
exp_y = f(exp_x)

# Main lines
plt.hlines(-ion_saturation, boundaries[0], boundaries[1])
plt.hlines(f(boundaries[2]), boundaries[2], boundaries[3])
plt.plot(exp_x, exp_y, c='k')

# Region separators
plt.vlines(boundaries[1], *plt.ylim(), 
           ls = sep_styles, lw=sep_lw)
plt.vlines(boundaries[2], *plt.ylim(), 
           ls = sep_styles, lw=sep_lw)

# Lines
plt.hlines(f(boundaries[2]), plt.xlim()[0], boundaries[2],
           ls=annotate_style, lw=annotate_lw)

plt.xlabel(r"$V_{\mathrm{probe}}$")
plt.ylabel(r"$I_{\mathrm{probe}}$")

plt.xticks([boundaries[2]], 
           [r"$V_{\mathrm{plasma}}$"])
plt.yticks([-ion_saturation, f(boundaries[2])], 
           [r"$I_{i,\mathrm{sat}}$", r"$I_{e,\mathrm{sat}}$"])


plt.savefig("../figures/langmuir_characteristic.png")