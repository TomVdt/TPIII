from constants import *

rcParams = {
    # Text appearance
    "text.usetex": True,
    "font.family": "serif",
    "text.latex.preamble": "\n".join([
        r"\usepackage[utf8]{inputenc}",
        r"\setlength{\parindent}{0pt}",
        # r"\usepackage[detect-all]{siunitx}",
        # r"\usepackage{mathabx}",
        # r"\usepackage{amsmath}",
    ]),

    # Text size
    "axes.labelsize": 16,
    "font.size": 16,
    "legend.fontsize": 16,
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
    # 'lines.markersize': 16,

    # Figure options
    "figure.figsize": (12*INCH_PER_CM, 12*INCH_PER_CM),
    'figure.dpi': 150,
    'axes.titlesize': 16,
    'axes.linewidth': 1.5,
    'lines.color': 'grey',
    'lines.linewidth' : 1.5,
    'scatter.marker': '+',
    'errorbar.capsize': 3,
    'axes.formatter.useoffset': False,
    # 'axes.spines.right': False,  # spineless smh
    # 'axes.spines.top': False,

    # Ticks
    'xtick.major.size' : 6,
    'xtick.major.width' : 1.5,
    'xtick.minor.size' : 3,
    'xtick.minor.width' : 1,

    'ytick.major.size' : 6,
    'ytick.major.width' : 1.5,
    'ytick.minor.size' : 3,
    'ytick.minor.width' : 1,

    'xtick.minor.visible' : True,
    'ytick.minor.visible' : True,
    
    # Legend
    'legend.framealpha': 1.0,
    "legend.handlelength" : 1.2,
    "legend.handleheight" : 0.5,
    "legend.handletextpad" : 0.6,
    "legend.labelspacing" : 0.3,
    'legend.edgecolor':   'black' ,
    'patch.linewidth' : 1.5,

    # Grid
    'axes.axisbelow' : True,
    'axes.grid' : False,
    'grid.linestyle' : '-',
    'grid.linewidth': 1,
    'grid.alpha': 0.75,

    # Saving
    # 'savefig.bbox': 'tight', # ça donne des figures avec marges irreguliers. 
        # utiliser plutot figure.subplot.left/right/bottom/top
}
