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
p['savefig.bbox'] = 'standard'
p["figure.subplot.left"]   = 0.26
p['figure.subplot.right']  = 0.97
p['figure.subplot.top']    = 0.97
p['figure.subplot.bottom'] = 0.18

sep_styles = ':' # (0.2,(4,8))
sep_lw = 0.5
annotate_style = '--'
annotate_lw = 0.75

ion_saturation = 1
# electron_saturation = 4
V_bias = 0.5

boundaries = [-2, 2, 9, 12]
plt.xlim(boundaries[0], boundaries[-1])
plt.ylim(-2, 22)

ax = plt.gca()

ion_saturation_x = np.linspace(boundaries[0], boundaries[1], 50)
exp_x = np.linspace(boundaries[1], boundaries[2], 50)
electron_saturation_x = np.linspace(boundaries[2], boundaries[3], 50)

def f(x):
    return np.exp(x - 6) - 1
exp_y = f(exp_x)

# Main lines
plt.grid(False)
plt.hlines(-ion_saturation, boundaries[0], boundaries[1])
plt.hlines(f(boundaries[2]), boundaries[2], boundaries[3])
plt.plot(exp_x, exp_y, c='k')

# Region separators
plt.vlines(boundaries[1], *plt.ylim(), 
           ls = sep_styles, lw=sep_lw)
plt.vlines(boundaries[2], *plt.ylim(), 
           ls = sep_styles, lw=sep_lw)
plt.text(0.15, 0.5, "I",
         horizontalalignment='center',
        verticalalignment='center',
        transform = ax.transAxes)
plt.text(0.55, 0.5, "II",
         horizontalalignment='center',
        verticalalignment='center',
        transform = ax.transAxes)
plt.text(0.89, 0.5, "III",
         horizontalalignment='center',
        verticalalignment='center',
        transform = ax.transAxes)

# Lines
plt.hlines(f(boundaries[2]), plt.xlim()[0], boundaries[2],
           ls=annotate_style, lw=annotate_lw)
V_free = exp_x[np.argmin(abs(exp_y))]
plt.hlines(0, plt.ylim()[0], V_free,
            ls=annotate_style, lw=annotate_lw)
plt.vlines(V_free, plt.ylim()[0], f(V_free),
           ls=annotate_style, lw=annotate_lw)

plt.xlabel(r"$V_{\mathrm{probe}}$")
plt.ylabel(r"$I_{\mathrm{probe}}$")

ax.minorticks_off()
ax.set_xticks([V_free, boundaries[2]], 
           labels=[r"$V_{\mathrm{free}}$", r"$V_{\mathrm{plasma}}$"])
ax.set_yticks([-ion_saturation, 0, f(boundaries[2])], 
           labels=[r"$I_{i,\mathrm{sat}}$", r"$0$", r"$I_{e,\mathrm{sat}}$"])

plt.savefig("../figures/langmuir_characteristic.pdf")