from pathlib import Path

from getdist import loadMCSamples, plots
import matplotlib.pyplot as plt

from desi_bao.data import TRACERS

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

    desi_bbn = load_chain("bao_dr2_bbn/ALL")             # own likelihood: columns H_0, Omega_m
    desi_bbn_alt = load_chain("bao_dr2_bbn_alt/ALL")   # built-in recipe: columns H0, omegam
    planck = load_chain("cmb_planck2018/planck")         # columns H0, omegam
    desi_bbn_thetastar = load_chain("bao_dr2_bbn_thetastar/ALL")
    g = plots.get_single_plotter(width_inch=5)
    g.settings.axes_fontsize = 12        
    g.settings.axes_labelsize = 14       
    g.settings.legend_fontsize = 9
    g.settings.legend_frame = False

    
    colors = {"planck": "C3", "desi": "C0","desi_alt": "C2", "desi_theta": "C1"}
    # Plot in CAMB's names (H0, omegam), which Planck and both built-in-recipe chains
    # already have; only the own-likelihood chain needs aliases. It is also the first
    # root, so its labels become the axis labels -> put the units here.
    desi_bbn.addDerived(desi_bbn.getParams().H_0, name="H0", label=r"H_0\ [\mathrm{km\,s^{-1}\,Mpc^{-1}}]")
    desi_bbn.addDerived(desi_bbn.getParams().Omega_m, name="omegam", label=r"\Omega_\mathrm{m}")

    # Roots, colours and legend labels are matched positionally, so keep these three
    # lists in the same order. Largest contours first so the small ones sit on top.
    roots  = [desi_bbn,            desi_bbn_alt,          desi_bbn_thetastar,                        planck]
    cols   = [colors["desi"],      colors["desi_alt"],    colors["desi_theta"],                      colors["planck"]]
    labels = ["DESI DR2 BAO + BBN", "DESI DR2 BAO + BBN alt", r"DESI DR2 BAO + BBN + $\theta_{\ast}$", "Planck 2018 CMB"]

    g.plot_2d(roots, "H0", "omegam", filled=True,
              colors=cols,   # plot_2d takes `colors`, not `contour_colors`
              lims=[65.8, 70.2, 0.27, 0.34])

    #for s, c in [(planck, colors["planck"]), (desi_dr2, colors["desi"])]:
    #    g.add_x_marker(s.mean("H_0r_d"), color=c, ls=":", lw=1)
    #    g.add_y_marker(s.mean("Omega_m"), color=c, ls=":", lw=1)

    g.add_legend(labels, legend_loc="upper right")

    #g.add_x_bands(planck.mean("H_0r_d"), planck.std("H_0r_d"), color=colors["planck"])
    g.add_text_left(r"$\Lambda$CDM", 0.05, 0.08, fontsize=12)                 # all positional, then keywords

    g.export(str(HERE / "fig8b.pdf"), dpi = 400)
    for label, s in [("Planck 2018", planck), ("DESI DR2 + BBN", desi_bbn),
                     ("DESI DR2 + BBN (alt)", desi_bbn_alt), ("DESI DR2 + BBN + thetastar", desi_bbn_thetastar)]:
        print(f"\n{label}")
        for p in ["omegam", "H0"]:
            print(f"  {p:8s} = {s.mean(p):8.4f} ± {s.std(p):.4f}   "
              f"(68% CL: {s.confidence(p, 0.16, upper=False):.4f} – {s.confidence(p, 0.16, upper=True):.4f})")
        print(f"  corr(omegam, H0) = {s.getCorrelationMatrix()[s.index['omegam'], s.index['H0']]:+.3f}")

    

if __name__ == "__main__":
    main()
