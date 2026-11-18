"""Cobaya input for the Planck 2018 CMB chain used in the left panel of Fig. 8.

Kept separate from Fig8/run_cmb.py so the input dict can be unit-tested
without running anything.
"""
from pathlib import Path

from cobaya.cosmo_input import create_input

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHAINS = PROJECT_ROOT / "chains" / "cmb_planck2018"
PACKAGES = Path.home() / "cobaya_packages"

# Pure-Python Planck 2018 likelihoods: no clik library needed.
PLANCK_LIKELIHOODS = {
    "planck_2018_lowl.TT": None,                        # Commander, l < 30
    "planck_2018_lowl.EE": None,                        # simall,    l < 30
    "planck_2018_highl_plik.TTTEEE_lite_native": None,  # l >= 30, foregrounds pre-marginalised
    "planck_2018_lensing.native": None,
}


def build_info():
    # Cobaya's standard Planck-2018 input: CAMB settings, the six sampled LCDM
    # parameters with Planck's priors, and the usual derived parameters.
    info = create_input(preset="planck_2018_camb")

    # 1. Swap the clik-based likelihoods for the pure-Python ones.
    info["likelihood"] = dict(PLANCK_LIKELIHOODS)

    # 2. Derived parameters with the SAME names as the BAO chains, so getdist
    #    can overlay them. rdrag is in Mpc and H0 in km/s/Mpc, so /100 gives
    #    DESI's "100 km/s" units.
    info["params"]["Omega_m"] = {
        "derived": "lambda omegam: omegam",
        "latex": r"\Omega_\mathrm{m}",
    }
    info["params"]["H_0r_d"] = {
        "derived": "lambda H0, rdrag: H0 * rdrag / 100",
        "latex": r"H_0 r_\mathrm{d}\ [100\,\mathrm{km\,s^{-1}}]",
    }

    # 3. Where things live.
    info["output"] = str(CHAINS / "planck")
    info["packages_path"] = str(PACKAGES)
    info["resume"] = True        # an interrupted overnight run can be continued
    return info
