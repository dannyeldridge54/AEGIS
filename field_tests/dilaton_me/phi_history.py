"""EXPLORATORY (not pre-registered): can the flagship's own dilaton make the TWIST-ME electron mass?
If m_e ~ exp(beta_e * phi) (phi in reduced-Planck units, as CLASS scf), then
  Delta ln m_e (recombination -> today) = beta_e [phi(0) - phi(1100)],
  Delta ln m_e (z = 0.89 -> today)      = beta_e [phi(0) - phi(0.89)]   (quasar methanol bound |dmu/mu| < ~1.5e-7, Kanekar+ 2015;
                                                                         mu = m_p/m_e, so this bounds m_e directly if m_p fixed)
  d ln m_e / dt today                   = beta_e phi_dot(0)              (atomic clocks: |mu_dot/mu| < ~1e-16 /yr).
The ratio of the late to the early field excursion decides whether one coupling can do both."""
import sys, os, json, types
import numpy as np
for n in ("candl", "candl.interface", "spt_candl_data"):
    sys.modules.setdefault(n, types.SimpleNamespace(CandlCobayaLikelihood=None, SPT3G_D1_TnE=None, interface=None))
sys.modules["candl"].interface = sys.modules["candl.interface"]
HERE = os.path.dirname(os.path.abspath(__file__)); AEGIS = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(AEGIS, "cmb-fit", "axiclass"))
import early_late_spa as E, spiral_guess
run = "ax_spa_spiraltwist_kappa1_nlfix"
E._maybe_coupled(run); import classy
info = E.make(run); st = json.load(open(f"{E.OUT}/cmp_{run}_s8y6.json"))["minimum"]
a = dict(info["theory"]["classytwist"]["extra_args"])
a.update({"A_s": 1e-10 * np.exp(st["logA"]), "n_s": st["n_s"], "100*theta_s": st["theta_s_1e2"], "omega_b": st["omega_b"],
          "omega_cdm": st["omega_cdm"], "tau_reio": st["tau_reio"]})
for k in ("output", "lensing", "l_max_scalars", "non_linear", "P_k_max_1/Mpc"): a.pop(k, None)
k, b = 1.0, st["scf_coupling_beta"]; a["scf_coupling_beta"] = b
a["scf_parameters"] = f"{k}, 0.0, {spiral_guess.mu1_guess(k, b, st['omega_b'], st['omega_cdm'])}, 0.0, 0.0, 0.0"
c = classy.Class(); c.set(a); c.compute(); bg = c.get_background()
z, phi = bg["z"][::-1], bg["phi_scf"][::-1]
P = lambda zz: float(np.interp(zz, z, phi))
t = bg["proper time [Gyr]"][::-1]
dphidt = float(np.gradient(phi, t)[0]) / 1e9          # per year, at z = 0
early, late = P(0) - P(1100), P(0) - P(0.89)
need = 0.0078                                        # TWIST-ME-size shift (literature m_e/m_e0 - 1 ~ 0.8%)
beta_e = need / abs(early) if early else float("inf")
out = {"note": "EXPLORATORY, not pre-registered", "phi(z=1100,0.89,0)": [P(1100), P(0.89), P(0)],
       "Delta_phi_rec_to_today": early, "Delta_phi_z0.89_to_today": late, "late_over_early": late / early,
       "beta_e_for_0.78pct_at_rec": beta_e, "implied_dlnme_z0.89": beta_e * late, "quasar_bound": 1.5e-7,
       "implied_dlnme_dt_per_yr": beta_e * dphidt, "clock_bound_per_yr": 1e-16}
json.dump(out, open(os.path.join(HERE, "phi_history.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
