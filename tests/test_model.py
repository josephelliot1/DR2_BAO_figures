import numpy as np
from desi_bao.model import model
from desi_bao.data import load_bao
from scipy.constants import c
import pytest
c_corr = c/1e5
#test 1: checking the output length is the same as the input:

def test_output_length_matches_data():
    d = load_bao("LRG1")
    pred = model(d["z"], d["kind"], 0.3, 101.5)
    assert len(pred) ==len(d["z"])

#2: analytical cases - does the model get the answers correct in the cases where there are known solutions?
#2.1 Does E(z) return 1 at z=0 for any Omega_m
def test_analytical():
    from desi_bao.model import E
    pred = E(0, 0)
    assert pred == 1

#2.2 Einstein de Sitter case

def test_EdS():
    #E = (1+z)**(3/2) therefore the integral has a closed form
    # D_M/r_d = (2c/H_0r_d)(1-1/sqrt(1+z))
    #so compute D_M for Omega_m = 1 and also the analytical and assert
    #that they are equal, for simplicity just assume z =0.5
    z = 0.5
    analytical = (2*c_corr/101.5)*(1-(1/np.sqrt(1+z)))
    from desi_bao.model import D_M
    pred = D_M(101.5, z, 1)
    assert pred == pytest.approx(analytical, rel=1e-6)