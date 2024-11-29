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
    "axes.labelsize": 12,
    "font.size": 12,
    "legend.fontsize": 12,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    # 'lines.markersize': 12,

    # Figure options
    "figure.figsize": (3.95, 2.96),
    'figure.dpi': 130,
    'axes.titlesize': 12,
    'lines.color': 'grey',
    'lines.linewidth' : 1,
    'scatter.marker': '+',
    'errorbar.capsize': 4,
    'axes.formatter.useoffset': False,
    # 'axes.spines.right': False,  # spineless smh
    # 'axes.spines.top': False,

    # Legend
    'legend.framealpha': 1.0,
    "legend.handlelength" : 1.2,
    "legend.handleheight" : 0.5,
    "legend.handletextpad" : 0.6,
    "legend.labelspacing" : 0.3,

    'axes.axisbelow' : True,
    # 'axes.grid' : True,
    'grid.linestyle' : '-',
    'grid.linewidth': 0.5,
    'grid.alpha': 0.75,
    'xtick.minor.visible' : True,
    'ytick.minor.visible' : True,

    # Saving
    'savefig.bbox': 'tight', # ça donne des figures avec marges irreguliers. 
        # utiliser plutot figure.subplot.left/right/bottom/top
}
