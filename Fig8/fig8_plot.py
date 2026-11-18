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

    desi_dr2 = load_chain("bao_dr2/ALL")
    planck = load_chain("cmb_planck2018/planck")
    g = plots.get_single_plotter(width_inch=5)
    g.settings.axes_fontsize = 12        
    g.settings.axes_labelsize = 14       
    g.settings.legend_fontsize = 9
    g.settings.legend_frame = False

    
    colors = {"planck": "C3", "desi": "C0"}

    g.plot_2d([planck, desi_dr2], "H_0r_d", "Omega_m", filled=True,
              contour_colors=[colors["planck"], colors["desi"]], lims=[95, 105, 0.255, 0.34])

    #for s, c in [(planck, colors["planck"]), (desi_dr2, colors["desi"])]:
    #    g.add_x_marker(s.mean("H_0r_d"), color=c, ls=":", lw=1)
    #    g.add_y_marker(s.mean("Omega_m"), color=c, ls=":", lw=1)

    g.add_legend(["Planck 2018 CMB"] + ["DESI DR2 BAO"],
             legend_loc="upper right")

    #g.add_x_bands(planck.mean("H_0r_d"), planck.std("H_0r_d"), color=colors["planck"])
    g.add_text_left(r"$\Lambda$CDM", 0.05, 0.08, fontsize=12)                  # all positional, then keywords

    g.export(str(HERE / "fig8.pdf"))
    for label, s in [("Planck 2018", planck), ("DESI DR2", desi_dr2)]:
        print(f"\n{label}")
        for p in ["Omega_m", "H_0r_d"]:
            print(f"  {p:8s} = {s.mean(p):8.4f} ± {s.std(p):.4f}   "
              f"(68% CL: {s.confidence(p, 0.16, upper=False):.4f} – {s.confidence(p, 0.16, upper=True):.4f})")
        print(f"  corr(Omega_m, H_0r_d) = {s.getCorrelationMatrix()[s.index['Omega_m'], s.index['H_0r_d']]:+.3f}")

    

if __name__ == "__main__":
    main()
