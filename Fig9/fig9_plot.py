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

    
    desi_bbn_alt = load_chain("bao_dr2_bbn_alt/ALL")   # built-in recipe: columns H0, omegam
    desi_bbn_lowz = load_chain("bao_dr2_bbn_lowz/ALL")
    desi_bbn_highz = load_chain("bao_dr2_bbn_highz/ALL")
    
    
    g = plots.get_single_plotter(width_inch=5)
    g.settings.axes_fontsize = 12        
    g.settings.axes_labelsize = 14       
    g.settings.legend_fontsize = 9
    g.settings.legend_frame = False

    
    colors = {"lowz": "C1","desi_alt": "C2", "highz": "C3"}
    
    #desi_bbn.addDerived(desi_bbn.getParams().H0, name="H0", label=r"H_0\ [\mathrm{km\,s^{-1}\,Mpc^{-1}}]")
    #desi_bbn.addDerived(desi_bbn.getParams().Omega_m, name="omegam", label=r"\Omega_\mathrm{m}")

    # Roots, colours and legend labels are matched positionally, so keep these three
    # lists in the same order. Largest contours first so the small ones sit on top.
    roots  = [desi_bbn_lowz, desi_bbn_highz, desi_bbn_alt]
    cols   = [colors["lowz"], colors["highz"],colors["desi_alt"]]
    labels = [r"DESI $(z<1.1)$ + BBN",r"DESI $(z>1.1)$ + BBN","DESI DR2 BAO + BBN"]

    # SH0ES 2024 (Breuval et al. 2024): a Gaussian in H0 only, so a horizontal band
    SH0ES_H0, SH0ES_SIG = 73.17, 0.86

    g.plot_2d(roots, "omegam", "H0", filled=True,
              colors=cols,   # plot_2d takes `colors`, not `contour_colors`
              lims=[0.2, 0.55,65,76])
    g.add_y_bands(SH0ES_H0, SH0ES_SIG, color="gray")

    # add_y_bands registers no legend handle, so append a proxy patch (after plot_2d,
    # so it comes after the three contour handles) and a matching 4th label
    #g.contours_added.append(Patch(color="gray", alpha=0.3))
    #labels.append("SH0ES")

    #for s, c in [(planck, colors["planck"]), (desi_dr2, colors["desi"])]:
    #    g.add_x_marker(s.mean("H_0r_d"), color=c, ls=":", lw=1)
    #    g.add_y_marker(s.mean("Omega_m"), color=c, ls=":", lw=1)

    g.add_legend(labels, legend_loc="lower right")

    #g.add_x_bands(planck.mean("H_0r_d"), planck.std("H_0r_d"), color=colors["planck"])
    g.add_text_left(r"$\Lambda$CDM", 0.05, 0.08, fontsize=12)                 # all positional, then keywords
    g.add_text_left("SH0ES", 0.75, 0.730, fontsize=12) 
    g.export(str(HERE / "fig9.pdf"), dpi = 400)
    for label, s in [("DESI $(z<1.1)$ + BBN", desi_bbn_lowz),("DESI $(z>1.1)$ + BBN", desi_bbn_highz),("DESI DR2 + BBN", desi_bbn_alt)]:
        print(f"\n{label}")
        for p in ["omegam", "H0"]:
            print(f"  {p:8s} = {s.mean(p):8.4f} ± {s.std(p):.4f}   "
              f"(68% CL: {s.confidence(p, 0.16, upper=False):.4f} – {s.confidence(p, 0.16, upper=True):.4f})")
        print(f"  corr(omegam, H0) = {s.getCorrelationMatrix()[s.index['omegam'], s.index['H0']]:+.3f}")
        print(f"  tension with SH0ES = {(SH0ES_H0 - s.mean('H0')) / np.hypot(SH0ES_SIG, s.std('H0')):.1f} sigma")

    

if __name__ == "__main__":
    main()
