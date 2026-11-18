"""Planck 2018 TT,TE,EE + lowE + lensing in flat LCDM,
with Omega_m and H0 r_d recorded as derived parameters (left panel of Fig. 8).

The input dict itself lives in desi_bao/cmb_input.py so it can be unit-tested.

    python Fig8/run_cmb.py --mode test       # initialise everything, sample nothing
    python Fig8/run_cmb.py --mode evaluate   # one likelihood call at the ref point
    python Fig8/run_cmb.py                   # the real (hours-long) chain
"""
import argparse

from cobaya.run import run

from desi_bao.cmb_input import build_info


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["test", "evaluate", "mcmc"], default="mcmc")
    args = ap.parse_args()

    info = build_info()
    if args.mode == "test":
        run(info, test=True)                      # initialise everything, sample nothing
    elif args.mode == "evaluate":
        info["sampler"] = {"evaluate": None}      # one likelihood call at the ref point
        info["output"] = None                     # don't write a chain for this
        run(info)
    else:
        run(info)
