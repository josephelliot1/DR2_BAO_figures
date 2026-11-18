
import numpy as np
from scipy.constants import c
from scipy.integrate import quad

c_corr = c/1e5 #Ensure consistent units

#Units of H_0r_d = 100kms-1 in line with DESI paper
#D_H/M/V compute everything per r_d

def E(z, Omega_m):
    return np.sqrt(Omega_m*(1+z)**3 + (1-Omega_m))

def inv_E(zp, Omega_m): #Inverse E to use as the integrand for quad, zp = dummy integration variable
    return 1/E(zp,Omega_m)

def D_H(H_0r_d,z, Omega_m):
    return (c_corr/H_0r_d)/E(z, Omega_m)

def D_M(H_0r_d,z, Omega_m): 
    return (c_corr/H_0r_d)*quad(inv_E, 0, z, args = (Omega_m,))[0]

def D_V(H_0r_d,z,Omega_m):
    return (z*D_M(H_0r_d,z, Omega_m)**2*D_H(H_0r_d,z,Omega_m))**(1/3)

def r_d(omega_b, omega_bc, N_eff): #r_d from Eq.2 in DR2 paper, units Mpc
    return 147.05*(((omega_b/0.02236)**-0.13)*((omega_bc/0.1432)**-0.23)*((N_eff/3.04)**-0.1))
def bridge(Omega_m, H_0, omega_b): #
    omega_nu = 0.06/93.14
    omega_bc = Omega_m*(H_0/100)**2-omega_nu
    rd = r_d(omega_b, omega_bc, 3.044)
    return H_0*rd/100 





OBSERVABLES = {"DM_over_rs": D_M, "DH_over_rs": D_H, "DV_over_rs": D_V}

def model(z, kind, Omega_m, H_0r_d):
    predictions = []
    for z_i, kind_i in zip(z, kind):
        func = OBSERVABLES[kind_i]
        predictions.append(func(H_0r_d, z_i, Omega_m))
    return np.array(predictions)

