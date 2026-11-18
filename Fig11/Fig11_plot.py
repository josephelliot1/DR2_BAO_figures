
from pathlib import Path

import numpy as np
from scipy.stats import chi2, norm
from getdist import loadMCSamples, plots
import matplotlib.pyplot as plt

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

    # w0waCDM chains from run_w0wa: columns w (= w0), wa, omegam, H0, rdrag
    desi_cmb = load_chain("w0wa/cmb")
    desi_cmb_pantheonplus = load_chain("w0wa/cmb_pantheonplus")
    desi_cmb_union3 = load_chain("w0wa/cmb_union3")
    desi_cmb_desy5 = load_chain("w0wa/cmb_desy5")

    g = plots.get_single_plotter(width_inch=5)
    g.settings.axes_fontsize = 12
    g.settings.axes_labelsize = 14
    g.settings.legend_fontsize = 8
    g.settings.legend_frame = False

    # same colour per SNe sample as fig10
    colors = {"cmb": "C4", "pantheonplus": "C0", "union3": "C1", "desy5": "C2"}

    # The paper's notation for the compressed CMB prior (see module docstring)
    CMB = r"$(\theta_\ast,\omega_\mathrm{b},\omega_\mathrm{bc})_\mathrm{CMB}$"
    #CMB = r"CMB" 
    # Roots, colours and legend labels are matched positionally, so keep these three
    # lists in the same order. Largest contours first so the small ones sit on top.
    roots  = [desi_cmb, desi_cmb_union3, desi_cmb_pantheonplus, desi_cmb_desy5]
    cols   = [colors["cmb"], colors["union3"], colors["pantheonplus"], colors["desy5"]]
    labels = [f"DESI + {CMB}", f"DESI + {CMB} + Union3", f"DESI + {CMB} + Pantheon+", f"DESI + {CMB} + DESY5"]

    g.plot_2d(roots, "w", "wa",
          filled=[False, True, True, True],   
          ls=["--", "-", "-", "-"],
          colors=cols,
          lims=[-1.1, 0.1, -3.0, 0.2])


    # LCDM limit (w0, wa) = (-1, 0): the paper's grey dashed lines
    g.add_x_marker(-1.0, color="gray", ls="--", lw=1)
    g.add_y_marker(0.0, color="gray", ls="--", lw=1)

    # label_order reorders the legend only (draw order stays largest-first):
    # Pantheon+, Union3, DESY5, then DESI + CMB, as in the paper and fig10
    g.add_legend(labels, legend_loc=(0.41,0.65), label_order=[2, 1, 3, 0])
    g.add_text_left(r"$w_0w_a$CDM", 0.09, 0.08, fontsize=12)
    g.export(str(HERE / "fig11.pdf"), dpi=400)

    for label, s in zip(labels, roots):
        print(f"\n{label}")
        for p in ["w", "wa", "omegam", "H0"]:
            print(f"  {p:8s} = {s.mean(p):8.4f} ± {s.std(p):.4f}   "
                  f"(68% CL: {s.confidence(p, 0.16, upper=False):.4f} – {s.confidence(p, 0.16, upper=True):.4f})")
        print(f"  corr(w, wa) = {s.getCorrelationMatrix()[s.index['w'], s.index['wa']]:+.3f}")
        # Distance of the LCDM point from the (w0, wa) posterior mean in units of the 2D
        # covariance, converted to a Gaussian-equivalent sigma for 2 extra parameters.
        # Only a Gaussian proxy: the paper's sigmas are delta-chi^2 of the best fits, and
        # its comparator for these compressed-CMB chains is the 2.4 sigma
        # "DESI + (theta*, omega_b, omega_bc)_CMB" row, not the full-CMB 3.1 sigma; the
        # SNe rows (2.8, 3.8, 4.2 sigma) exist only for the full CMB. For DESI + CMB the
        # mean and covariance are also truncated by the wa > -3 prior edge.
        d = np.array([-1.0, 0.0]) - np.array([s.mean("w"), s.mean("wa")])
        d2 = d @ np.linalg.solve(s.cov(["w", "wa"]), d)
        print(f"  LCDM point at {norm.isf(0.5 * chi2.sf(d2, 2)):.1f} sigma from the mean "
              f"(2D Gaussian proxy, not the paper's delta-chi^2_MAP)")


if __name__ == "__main__":
    main()
