import numpy as np
from desi_bao.model import model
from desi_bao.data import load_bao


def log_like(data, Omega_m, H_0r_d):
    """ln L = -chi^2/2 for one tracer's data dict, at the given parameters."""
    resid = data["value"] - model(data["z"], data["kind"], Omega_m, H_0r_d)
    return -0.5 * resid @ data["invcov"] @ resid


def make_loglike(tracer):
    """Return a function of (Omega_m, H_0r_d) only, with the tracer's data baked in.
    This is the form Cobaya needs for an external likelihood."""
    data = load_bao(tracer)

    def loglike(Omega_m, H_0r_d):
        return log_like(data, Omega_m, H_0r_d)

    return loglike
