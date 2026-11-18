from pathlib import Path

import numpy as np
from getdist import loadMCSamples, plots
import matplotlib.pyplot as plt

from desi_bao.data import TRACERS
from matplotlib.patches import Patch

HERE = Path(__file__).resolve().parent
CHAINS = HERE.parent / "chains" 

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],              # Computer Modern for ordinary text
    "mathtext.fontset": "cm",             # Computer Modern for everything in $...$
    "axes.formatter.use_mathtext": True,  # tick numbers also drawn via mathtext
    "axes.unicode_minus": False,
})


def load_chain(relpath):

    return loadMCSamples(str(CHAINS / relpath), settings={"ignore_rows": 0.1})


def main():

    desi_DR1 = load_chain("BAO_DR1/ALL")
    desi_DR2 = load_chain("bao_dr2/ALL")   # built-in recipe: columns H0, omegam
    cmb = load_chain("cmb_planck2018/planck")
    pantheonplus = load_chain("sne/pantheonplus")
    union3 = load_chain("sne/union3")
    desy5 = load_chain("sne/desy5")

    
    g = plots.get_single_plotter(width_inch=5)
    g.settings.axes_fontsize = 12        
    g.settings.axes_labelsize = 14       
    g.settings.legend_fontsize = 9
    g.settings.legend_frame = False
    g.settings.prob_y_ticks = True
    
    colors = {"desi_DR1": 'black',"desi_DR2": "C0", "cmb":"C1", "pantheonplus": "C2", "union3":"C3", "desy5":"C4"}
    
    #desi_DR2.addDerived(desi_DR2.getParams().H_0, name="H0", label=r"H_0\ [\mathrm{km\,s^{-1}\,Mpc^{-1}}]")
    desi_DR2.addDerived(desi_DR2.getParams().Omega_m, name="omegam", label=r"\Omega_\mathrm{m}")
    
    roots  = [desi_DR1,desi_DR2, cmb, pantheonplus,union3,desy5]
    cols   = [colors["desi_DR1"],colors["desi_DR2"], colors["cmb"], colors["pantheonplus"],colors["union3"], colors["desy5"]]
    labels = ["DESI DR1","DESI DR2", "CMB", "Pantheon+", "Union3", "DESY5"]
    styles = ["--", "-", "-", "-", "-", "-"]   # DR1 dashed, everything else solid (matched positionally like cols)



    g.plot_1d(roots, "omegam", filled=False,
              colors=cols, ls=styles,
              lims=([0.24, 0.45]), normalized=True)
    g.get_axes().set_ylim(0, 62.5)
    g.get_axes().set_ylabel("Probability density")


    g.add_legend(labels)

    #g.add_text_left(r"$\Lambda$CDM", 0.05, 0.08, fontsize=12)                 # all positional, then keywords
    g.export(str(HERE / "fig10.pdf"), dpi = 400)

    for label, s in zip(labels, roots):
        print(f"{label:10s} omegam = {s.mean('omegam'):.4f} ± {s.std('omegam'):.4f}   "
              f"(68% CL: {s.confidence('omegam', 0.16, upper=False):.4f} – {s.confidence('omegam', 0.16, upper=True):.4f})")


if __name__ == "__main__":
    main()
