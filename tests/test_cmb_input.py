"""Tests for the Planck CMB chain input (Fig. 8, left panel).

The fast tests only inspect the Cobaya input dict. The one marked `slow`
initialises Cobaya + CAMB + the four Planck likelihoods and needs the
downloaded Planck data; run it with `pytest -m slow`.
"""
import pytest

from desi_bao.cmb_input import CHAINS, PLANCK_LIKELIHOODS, build_info

# Planck 2018 TT,TE,EE+lowE+lensing best fit (Planck 2018 VI, Table 2)
PLANCK_H0 = 67.36
PLANCK_RDRAG = 147.09


@pytest.fixture(scope="module")
def info():
    return build_info()


def sampled_params(info):
    return {k for k, v in info["params"].items() if isinstance(v, dict) and "prior" in v}


def test_six_lcdm_parameters_are_sampled(info):
    assert sampled_params(info) == {"ombh2", "omch2", "theta_MC_100", "tau", "logA", "ns"}


def test_derived_params_use_bao_chain_names(info):
    # fig8_plot overlays BAO and CMB chains by these exact names
    for name in ("Omega_m", "H_0r_d"):
        assert "derived" in info["params"][name], f"{name} must be derived, not sampled"
        assert "latex" in info["params"][name]


def test_H0rd_formula_gives_desi_units(info):
    f = eval(info["params"]["H_0r_d"]["derived"])
    value = f(PLANCK_H0, PLANCK_RDRAG)
    assert value == pytest.approx(PLANCK_H0 * PLANCK_RDRAG / 100)
    # Planck sits a few sigma below DESI's 101.54 +/- 0.73: the tension shown in Fig. 8
    assert 98 < value < 100


def test_Omega_m_is_camb_omegam(info):
    f = eval(info["params"]["Omega_m"]["derived"])
    assert f(0.315) == 0.315


def test_likelihoods_are_pure_python(info):
    assert set(info["likelihood"]) == set(PLANCK_LIKELIHOODS)
    assert not any("clik" in name for name in info["likelihood"])


def test_neutrino_assumptions_match_desi(info):
    # DESI DR2 Sec. IV: N_eff = 3.044, sum m_nu = 0.06 eV
    assert info["params"]["mnu"] == 0.06
    extra = info["theory"]["camb"]["extra_args"]
    assert extra["nnu"] == 3.044
    assert extra["lens_potential_accuracy"] >= 1   # required by the lensing likelihood


def test_chains_go_to_shared_folder(info):
    assert info["output"].startswith(str(CHAINS))
    assert info.get("resume") is True


def test_camb_reproduces_planck_rdrag():
    """CAMB by hand: r_drag at the Planck best fit should be ~147.1 Mpc."""
    import camb
    pars = camb.set_params(H0=PLANCK_H0, ombh2=0.02237, omch2=0.1200, tau=0.0544,
                           As=2.1e-9, ns=0.9649, mnu=0.06, nnu=3.044)
    rdrag = camb.get_background(pars).get_derived_params()["rdrag"]
    assert rdrag == pytest.approx(PLANCK_RDRAG, abs=0.3)


@pytest.mark.slow
def test_cobaya_initialises_everything(info):
    """Full wiring check: Cobaya + CAMB + Planck likelihoods, no sampling."""
    from cobaya.run import run
    run(dict(info, output=None, resume=False), test=True)
