"""Load the DESI DR2 BAO measurements downloaded with `cobaya-install bao.desi_dr2`.

Each tracer has a pair of files:
    desi_gaussian_bao_<stem>_mean.txt   columns: z, value, observable
    desi_gaussian_bao_<stem>_cov.txt    covariance matrix, same row order as the mean file
The observable column is one of 'DM_over_rs', 'DH_over_rs', 'DV_over_rs'.
"""
from pathlib import Path

import numpy as np

DATA_DIR = Path.home() / "cobaya_packages" / "data" / "bao_data" / "desi_bao_dr2"

# Short tracer label (as used in the DESI paper) -> file stem in DATA_DIR
TRACERS = {
    "BGS": "BGS_BRIGHT-21.35_GCcomb",
    "LRG1": "LRG_GCcomb_z0.4-0.6",
    "LRG2": "LRG_GCcomb_z0.6-0.8",
    "LRG3+ELG1": "LRG+ELG_LOPnotqso_GCcomb",
    "ELG2": "ELG_LOPnotqso_GCcomb_z1.1-1.6",
    "QSO": "QSO_GCcomb",
    "Lya": "Lya_GCcomb",
    "ALL": "ALL_GCcomb",
}


def load_bao(tracer):
    """Return the BAO data for one tracer (or 'ALL') as a dict.

    Keys:
        z       (n,)   effective redshift of each measurement
        value   (n,)   measured D_M/r_d, D_H/r_d or D_V/r_d
        kind    (n,)   which observable each row is, e.g. 'DM_over_rs'
        cov     (n,n)  covariance matrix
        invcov  (n,n)  its inverse, precomputed for the likelihood
    """
    stem = TRACERS[tracer]
    # The mean file mixes numbers and strings, so read everything as text first.
    # atleast_2d keeps a single-row file (BGS) as shape (1, 3) rather than (3,).
    raw = np.atleast_2d(np.loadtxt(DATA_DIR / f"desi_gaussian_bao_{stem}_mean.txt", dtype=str))
    cov = np.atleast_2d(np.loadtxt(DATA_DIR / f"desi_gaussian_bao_{stem}_cov.txt"))
    return {
        "z": raw[:, 0].astype(float),
        "value": raw[:, 1].astype(float),
        "kind": raw[:, 2],
        "cov": cov,
        "invcov": np.linalg.inv(cov),
    }


if __name__ == "__main__":
    # Sanity check against Table IV of arXiv:2503.14738
    for name in TRACERS:
        d = load_bao(name)
        err = np.sqrt(np.diag(d["cov"]))
        print(f"\n{name}  (z_eff = {d['z'][0]:.3f}, {len(d['z'])} measurements)")
        for k, v, e in zip(d["kind"], d["value"], err):
            print(f"  {k:12s} = {v:8.3f} +/- {e:.3f}")
        if len(d["z"]) == 2:
            r = d["cov"][0, 1] / (err[0] * err[1])
            print(f"  correlation  = {r:+.3f}")
