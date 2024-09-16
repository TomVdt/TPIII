rcParams = {
    # Text appearance
    "text.usetex": True,
    "font.family": "serif",
    "text.latex.preamble": "\n".join([
        r"\usepackage[utf8]{inputenc}",
        # r"\usepackage[detect-all]{siunitx}",
        # r"\usepackage{mathabx}",
    ]),

    # Text size
    "axes.labelsize": 14,
    "font.size": 14,
    "legend.fontsize": 12,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    'lines.markersize': 14,

    # Figure options
    "figure.figsize": (3.95, 2.96),
    'lines.color': 'grey',
    'scatter.marker': '+',
    'errorbar.capsize': 4,
    'axes.formatter.useoffset': False,
    'axes.spines.right': False,  # spineless smh
    'axes.spines.top': False,
    'legend.framealpha': 1.0,
    
    # Saving
    'savefig.bbox': 'tight',
    # 'savefig.directory': '../figures/'
}
