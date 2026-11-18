from pathlib import Path

import numpy as np
from cobaya.run import run

from desi_bao.data import TRACERS
from desi_bao.likelihood import make_loglike
from desi_bao.model import bridge
HERE = Path(__file__).resolve().parent
CHAINS = HERE.parent / "chains" / "bao_dr2"

#Uniform priors
#DR2 individual tracers
def run_tracer(name, force=False):
    info = {
        "likelihood": {f"bao_{name}": make_loglike(name)},
        "params": {
            "Omega_m": {
                "prior": {"min": 0.01, "max": 0.99},
                "ref": 0.3,
                "proposal": 0.01,
                "latex": r"\Omega_\mathrm{m}",
            },
            "H_0r_d": {
                "prior": {"min": 20.0, "max": 200.0},
                "ref": 101.5,
                "proposal": 1.0,
                "latex": r"H_0 r_\mathrm{d}\ [100\,\mathrm{km\,s^{-1}}]",
            },
        },
        "sampler": {"mcmc": {"Rminus1_stop": 0.002, "Rminus1_cl_stop": 0.02, "max_tries": 100000}},
        "output": str(CHAINS / name),
        "force": force,
    }
    updated_info, sampler = run(info)
    return updated_info, sampler


#DR1 all tracers: Cobaya's built-in DR1 likelihood (bao.desi_2024_*) + CAMB, same
#recipe as run_tracer_BBN_alt (BBN prior on omega_b, flat omega_c and theta_star).
#Omega_m and H_0r_d are recorded as derived parameters with the same names as the
#own-likelihood chains, so this chain plots directly in fig8_plot.py.
def run_DR1(name, force=False):
    info = {
        "theory": {"camb": {"extra_args": {"nnu": 3.044, "num_massive_neutrinos": 1}}},
        "likelihood": {"bao.desi_2024_bao_all": None},
        "params": {
            "ombh2": {
                "prior": {"dist": "norm", "loc": 0.02218, "scale": 0.00055},
                "proposal": 0.0001,
                "latex": r"\omega_\mathrm{b}",
            },
            "omch2": {
                "prior": {"min": 0.05, "max": 0.25}, "ref": 0.117,
                "proposal": 0.001,
                "latex": r"\omega_\mathrm{c}",
            },
            "theta_star_100": {
                "prior": {"min": 0.5, "max": 1.5}, "ref": 1.0411,
                "proposal": 0.0002,
                "latex": r"100\theta_\ast",
            },
            "thetastar": {"value": "lambda theta_star_100: 1e-2*theta_star_100"},
            "mnu": 0.06,
            "H0": {"latex": r"H_0"},
            "omegam": {"latex": r"\Omega_\mathrm{m}"},
            "rdrag": {"latex": r"r_\mathrm{d}"},
            # same derived names as the own-likelihood chains and the Planck chain
            "Omega_m": {"derived": "lambda omegam: omegam", "latex": r"\Omega_\mathrm{m}"},
            "H_0r_d": {"derived": "lambda H0, rdrag: H0*rdrag/100",
                       "latex": r"H_0 r_\mathrm{d}\ [100\,\mathrm{km\,s^{-1}}]"},
        },
        "sampler": {"mcmc": {"Rminus1_stop": 0.002, "Rminus1_cl_stop": 0.02, "max_tries": 100000}},
        "output": str(CHAINS.parent/"BAO_DR1"/name),
        "packages_path": str(Path.home() / "cobaya_packages"),
        "force": force,
    }
    updated_info, sampler = run(info)
    return updated_info, sampler

#BBN priors DR2
def run_tracer_BBN(name, force = False):
    info = {
        "likelihood":{f"bao_{name}":make_loglike(name)},
        "params":{
            "Omega_m":{
                "prior": {"min":0.01, "max":0.99},
                "ref":0.3,
                "proposal":0.01,
                "latex": r"\Omega_\mathrm{m}",
            },
            "H_0":{
                "prior": {"min": 50.0, "max": 100.0},
                "proposal": 1.0,
                "latex": r"H_0"
            },
            "omega_b":{
                "prior":{"dist": "norm", "loc": 0.02218, "scale": 0.00055},
                "proposal":0.0001,
                "latex": r"\omega_\mathrm{b}",
            },
            "H_0r_d":{"value": bridge, "latex": r"H_0 r_\mathrm{d}\ [100\,\mathrm{km\,s^{-1}}]"} 

        },
        "sampler":{"mcmc": {"Rminus1_stop": 0.002, "Rminus1_cl_stop": 0.02, "max_tries": 100000}},
        "output": str(CHAINS.parent/"bao_dr2_bbn"/name),
        "force": force,

    }
    updated_info, sampler =run(info)
    return updated_info, sampler
def run_tracer_BBN_alt(name, force = False): #chain for figure 8b sampling omega_b, omega_c and thata_star
    info = {
            "likelihood":{"bao.desi_dr2.desi_bao_all":None},
            "params":{
                "ombh2":{
                    "prior":{"dist": "norm", "loc": 0.02218, "scale": 0.00055},
                            "proposal":0.0001,
                            "latex": r"\omega_\mathrm{b}",
                },
                "omch2":{
                    "prior": {"min":0.05,"max":0.25}, "ref": 0.117,
                    "proposal": 0.001,
                    "latex": r"\omega_\mathrm{c}"
                },
                "theta_star_100":{ 
                    "prior": {"min": 0.5, "max": 1.5}, "ref":1.0411,
                    "proposal":0.0002,
                    "latex": r"100\theta_\ast",
                },
                "thetastar": {"value": "lambda theta_star_100: 1e-2*theta_star_100"},
                "mnu": 0.06,
                "H0": {"latex": r"H_0"},
                "omegam":{"latex": r"\Omega_\mathrm{m}"},
                "rdrag": {"latex": r"r_\mathrm{d}"},
                },
    "sampler":{"mcmc": {"Rminus1_stop": 0.002, "Rminus1_cl_stop": 0.02, "max_tries": 100000}},
     'theory': {'camb': {'extra_args': {'nnu': 3.044, 'num_massive_neutrinos': 1}}},
    "output": str(CHAINS.parent/"bao_dr2_bbn_alt"/name),
    "packages_path":str(Path.home() / "cobaya_packages"),
    "force": force,}
    updated_info, sampler =run(info)
    return updated_info, sampler

def run_tracer_BBN_thetastar(name, force = False): #chain for figure 8b sampling omega_b, omega_c and thata_star
    info = {
            "likelihood":{"bao.desi_dr2.desi_bao_all":None},
            "params":{
                "ombh2":{
                    "prior":{"dist": "norm", "loc": 0.02218, "scale": 0.00055},
                            "proposal":0.0001,
                            "latex": r"\omega_\mathrm{b}",
                },
                "omch2":{
                    "prior": {"min":0.05,"max":0.25}, "ref": 0.117,
                    "proposal": 0.001,
                    "latex": r"\omega_\mathrm{c}"
                },
                "theta_star_100":{ 
                    "prior": {"dist":"norm", "loc": 1.04110, "scale": 0.00053}, "ref":1.0411,
                    "proposal":0.0002,
                    "latex": r"100\theta_\ast",
                },
                "thetastar": {"value": "lambda theta_star_100: 1e-2*theta_star_100"},
                "mnu": 0.06,
                "H0": {"latex": r"H_0"},
                "omegam":{"latex": r"\Omega_\mathrm{m}"},
                "rdrag": {"latex": r"r_\mathrm{d}"},
                },
    "sampler":{"mcmc": {"Rminus1_stop": 0.002, "Rminus1_cl_stop": 0.02, "max_tries": 100000}},
     'theory': {'camb': {'extra_args': {'nnu': 3.044, 'num_massive_neutrinos': 1}}},
    "output": str(CHAINS.parent/"bao_dr2_bbn_thetastar"/name),
    "packages_path":str(Path.home() / "cobaya_packages"),
    "force": force,}
    updated_info, sampler =run(info)
    return updated_info, sampler

#DESI+ BBN chain run in 2 redshift bins: low z (<1.1) and high z (<1.1) tracers
#To toggle, change the likelihood entries in the info dict

def run_tracer_BBN_highlowz(name, force = False): #chain for figure 8b sampling omega_b, omega_c and thata_star
    info = {
            #"likelihood": {"bao.desi_dr2.desi_bao_bgs": None, #Low z tracers
            #   "bao.desi_dr2.desi_bao_lrg1": None,
            #   "bao.desi_dr2.desi_bao_lrg2": None,
            #   "bao.desi_dr2.desi_bao_lrg3pluselg1": None},
            "likelihood": {"bao.desi_dr2.desi_bao_elg2": None,   # High z tracers
               "bao.desi_dr2.desi_bao_qso": None,
               "bao.desi_dr2.desi_bao_lya": None},


            "params":{
                "ombh2":{
                    "prior":{"dist": "norm", "loc": 0.02218, "scale": 0.00055},
                            "proposal":0.0001,
                            "latex": r"\omega_\mathrm{b}",
                },
                "omch2":{
                    "prior": {"min":0.05,"max":0.25}, "ref": 0.117,
                    "proposal": 0.001,
                    "latex": r"\omega_\mathrm{c}"
                },
                "theta_star_100":{ 
                    "prior": {"min": 0.5, "max": 1.5}, "ref":1.0411,
                    "proposal":0.0002,
                    "latex": r"100\theta_\ast",
                },
                "thetastar": {"value": "lambda theta_star_100: 1e-2*theta_star_100"},
                "mnu": 0.06,
                "H0": {"latex": r"H_0"},
                "omegam":{"latex": r"\Omega_\mathrm{m}"},
                "rdrag": {"latex": r"r_\mathrm{d}"},
                },
    "sampler":{"mcmc": {"Rminus1_stop": 0.002, "Rminus1_cl_stop": 0.02, "max_tries": 100000}},
     'theory': {'camb': {'extra_args': {'nnu': 3.044, 'num_massive_neutrinos': 1}}},
    "output": str(CHAINS.parent/"bao_dr2_bbn_highz"/name),
    "packages_path":str(Path.home() / "cobaya_packages"),
    "force": force,}
    updated_info, sampler =run(info)
    return updated_info, sampler

def run_SNe(name, like, force = False): #sample supernova data. 
    info = {
    "theory": {"camb": {"extra_args": {"nnu": 3.044, "num_massive_neutrinos": 1}}},
    "likelihood": {like: None},        # or sn.union3 / sn.desy5
    "params": {
        "omch2": {"prior": {"min": 0.02, "max": 0.30}, "ref": 0.14,
                  "proposal": 0.005, "latex": r"\omega_\mathrm{c}"},
        "H0": 70.0,          # fixed: M is marginalised, so SNe cannot see it
        "ombh2": 0.02218,    # fixed: only bookkeeping for omegam
        "mnu": 0.06,
        "omegam": {"latex": r"\Omega_\mathrm{m}"},   # derived, same name as your other chains
    },
    "sampler": {"mcmc": {"Rminus1_stop": 0.002, "Rminus1_cl_stop": 0.02, "max_tries": 100000}},
    "output": str(CHAINS.parent/"sne"/name),
    "packages_path": str(Path.home() / "cobaya_packages"),
    "force": force,}
    updated_info, sampler =run(info)
    return updated_info, sampler 

#w0waCDM chains for Fig. 11: DESI DR2 BAO + CMB (+ one SNe sample), built-in likelihoods + CAMB.
#CAMB recomputes every distance with w(a) = w0 + wa(1-a) in the dark-energy term of E(z);
#nothing in desi_bao/model.py is used. The CMB enters through the paper's Appendix A
#compression: a correlated Gaussian prior on (theta*, omega_b, omega_bc), the early-Universe
#quantities the CMB fixes independently of late-time physics (Eqs. A1-A2). No BBN prior:
#omega_b is already pinned by this CMB prior.
CMB_MU = np.array([0.01041, 0.02223, 0.14208])     # mean of (theta*, omega_b, omega_bc); theta* not 100 theta*
CMB_COV = 1e-9 * np.array([[ 0.006621,   0.12444,   -1.1929],
                           [ 0.12444,   21.344,    -94.001 ],
                           [-1.1929,   -94.001,   1488.4   ]])
CMB_INVCOV = np.linalg.inv(CMB_COV)

def cmb_compressed_prior(theta_star_100, ombh2, omch2):
    
    d = np.array([theta_star_100 / 100, ombh2, ombh2 + omch2]) - CMB_MU
    return -0.5 * d @ CMB_INVCOV @ d

#Fig. 11 data combinations: chain name -> extra SNe likelihood (None = DESI + CMB only)
W0WA_COMBOS = {
    "cmb": None,
    "cmb_pantheonplus": "sn.pantheonplus",
    "cmb_union3": "sn.union3",
    "cmb_desy5": "sn.desy5",
}

def run_w0wa(name, sn_like=None, force=False):
    likes = {"bao.desi_dr2.desi_bao_all": None}
    if sn_like is not None:
        likes[sn_like] = None
    info = {
        "theory": {"camb": {"extra_args": {"nnu": 3.044, "num_massive_neutrinos": 1,
                                           "dark_energy_model": "ppf"}}},
        "likelihood": likes,
        "prior": {
            "cmb_compressed": cmb_compressed_prior,
            "matter_dom": "lambda w, wa: 0 if w + wa < 0 else -np.inf",   #paper: w0 + wa < 0
        },
        "params": {
            "ombh2": {"prior": {"min": 0.015, "max": 0.03}, "ref": 0.02223,
                      "proposal": 0.0001, "latex": r"\omega_\mathrm{b}"},
            "omch2": {"prior": {"min": 0.05, "max": 0.25}, "ref": 0.1198,
                      "proposal": 0.001, "latex": r"\omega_\mathrm{c}"},
            "theta_star_100": {"prior": {"min": 1.0, "max": 1.1}, "ref": 1.041,
                               "proposal": 0.0002, "latex": r"100\theta_\ast"},
            "thetastar": {"value": "lambda theta_star_100: 1e-2*theta_star_100"},
            "w":  {"prior": {"min": -3.0, "max": 1.0}, "ref": -0.8, "proposal": 0.05, "latex": r"w_0"},
            "wa": {"prior": {"min": -3.0, "max": 2.0}, "ref": -0.8, "proposal": 0.1,  "latex": r"w_a"},
            "mnu": 0.06,
            "H0": {"latex": r"H_0"},
            "omegam": {"latex": r"\Omega_\mathrm{m}"},
            "rdrag": {"latex": r"r_\mathrm{d}"},
        },
        "sampler": {"mcmc": {"Rminus1_stop": 0.002, "Rminus1_cl_stop": 0.02, "max_tries": 100000}},
        "output": str(CHAINS.parent / "w0wa" / name),
        "packages_path": str(Path.home() / "cobaya_packages"),
        "force": force,
    }
    updated_info, sampler = run(info)
    return updated_info, sampler


if __name__ == "__main__":
    #for i in TRACERS:
        #run_tracer(i, force=True)
    #for name, like in [("pantheonplus", "sn.pantheonplus"),
        #           ("union3",       "sn.union3"),
        #           ("desy5",        "sn.desy5")]:
        #run_SNe(name, like, force=True)

    for name, sn_like in W0WA_COMBOS.items():
        run_w0wa(name, sn_like, force=True)
