"""UB-2 engine check G1' (two-field CAMB module, DarkEnergyUBField.f90): with lam = 0 and the dilaton term a constant,
the module must reproduce CAMB's own EarlyQuintessence (n = 3) + cosmological constant, perturbations included.
Point: the stored Locked Twist best fit (results/cmp_edelockP.json). Prints the largest relative differences."""
import json, math, os, sys
import numpy as np
import camb
from camb.dark_energy import UBField

HERE = os.path.dirname(os.path.abspath(__file__))
lt = json.load(open(os.path.join(HERE, "..", "results", "cmp_edelockP.json")))["minimum"]
zc = (lt["ombh2"] + lt["omch2"]) / (2.4728e-5 * (1 + 0.22711 * 3.044)) - 1
kw = dict(H0=lt["H0"], ombh2=lt["ombh2"], omch2=lt["omch2"], mnu=0.06, num_massive_neutrinos=1, nnu=3.044,
          tau=lt["tau"], As=1e-10 * math.exp(lt["logA"]), ns=lt["ns"], lmax=2600, lens_potential_accuracy=1)
p = camb.set_params(dark_energy_model="EarlyQuintessence", n=3, use_zc=True, zc=zc, fde_zc=lt["fde_zc"],
                    theta_i=lt["theta_i"], **kw)
r = camb.get_results(p)
eq = r.Params.DarkEnergy
f, m = eq.f, eq.m
a = np.asarray(eq.sampled_a); phi = np.asarray(eq.phi_a); phid = np.asarray(eq.phidot_a)
G, hbar, c, Mpc = 6.67430e-11, 1.054571817e-34, 2.99792458e8, 3.085677581e22
units = (Mpc / c) ** 2 / (8 * math.pi * G * hbar / c ** 5)
ub = UBField()
ub.var, ub.kpar, ub.lam, ub.FP = 2, 0.0, 0.0, f
ub.VA = r.grhov            # the cosmological constant part (frac_lambda0 = 1)
ub.VL = units * m ** 2 * f ** 2
ub.set_table(np.log(a), np.zeros_like(a), phi / f, np.zeros_like(a), phid / f)
q = camb.set_params(**kw)
q.DarkEnergy = ub
r2 = camb.get_results(q)
zs = np.geomspace(1e-2, 1e4, 60)
dH = max(abs(r.hubble_parameter(z) / r2.hubble_parameter(z) - 1) for z in zs)
c1 = r.get_cmb_power_spectra(lmax=2500, CMB_unit="muK")["total"]
c2 = r2.get_cmb_power_spectra(lmax=2500, CMB_unit="muK")["total"]
out = {"max_rel_H": dH,
       "max_rel_TT_l2_2500": float(np.max(np.abs(c2[2:2500, 0] / c1[2:2500, 0] - 1))),
       "max_rel_EE_l2_2500": float(np.max(np.abs(c2[2:2500, 1] / c1[2:2500, 1] - 1))),
       "max_abs_TE_over_sqrtTTEE": float(np.max(np.abs(c2[2:2500, 3] - c1[2:2500, 3]) / np.sqrt(c1[2:2500, 0] * c1[2:2500, 1])))}
print(json.dumps(out, indent=1))
