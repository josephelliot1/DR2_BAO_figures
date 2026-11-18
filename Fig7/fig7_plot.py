from pathlib import Path

from getdist import loadMCSamples, plots
import matplotlib.pyplot as plt

from desi_bao.data import TRACERS

HERE = Path(__file__).resolve().parent
CHAINS = HERE.parent / "chains" / "bao_dr2"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],              # Computer Modern for ordinary text
    "mathtext.fontset": "cm",             # Computer Modern for everything in $...$
    "axes.formatter.use_mathtext": True,  # tick numbers also drawn via mathtext
    "axes.unicode_minus": False,
})



TO_PLOT = ["BGS", "LRG1", "LRG2", "LRG3+ELG1", "ELG2", "QSO", "Lya"]
LABELS = {"Lya": r"Ly$\alpha$"}


def load_chain(name):

    return loadMCSamples(str(CHAINS / name), settings={"ignore_rows": 0.1})


def main():
    samples = [load_chain(name) for name in TO_PLOT]
    g = plots.get_single_plotter(width_inch=5)
    g.settings.axes_fontsize = 12        
    g.settings.axes_labelsize = 14       
    g.settings.legend_fontsize = 9
    g.settings.legend_frame = False

    
    g.plot_2d(samples, "H_0r_d", "Omega_m", filled=True,
              lims=[85, 115, 0.15, 0.55])
    g.add_2d_contours(load_chain("ALL"), "H_0r_d", "Omega_m",
                  filled=False, color="black", lw=1.5)
    g.add_legend([LABELS.get(name, name) for name in TO_PLOT] + ["DESI DR2 combined"],
             legend_loc="upper right")


    g.add_text_left(r"$\Lambda$CDM", 0.05, 0.08, fontsize=12)                  # all positional, then keywords

    g.export(str(HERE / "fig7.pdf"))
    

if __name__ == "__main__":
    main()
