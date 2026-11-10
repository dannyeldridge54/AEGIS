"""Helper: luminosity distances D_L(z) [Mpc] of the Pantheon+ SNe at a stored best fit (its own CLASS build, background only).
    python dl_at_fit.py <run> <out.npy>"""
import sys, os, json, glob, types
import numpy as np
for n in ("candl", "candl.interface", "spt_candl_data"):
    sys.modules.setdefault(n, types.SimpleNamespace(CandlCobayaLikelihood=None, SPT3G_D1_TnE=None, interface=None))
sys.modules["candl"].interface = sys.modules["candl.interface"]
HERE = os.path.dirname(os.path.abspath(__file__)); AEGIS = os.path.abspath(os.path.join(HERE, "..", ".."))
AX = os.path.join(AEGIS, "cmb-fit", "axiclass"); sys.path.insert(0, AX)
import early_late_spa as E
run, outp = sys.argv[1], sys.argv[2]
base = run.replace("_s8y6_more", "").replace("_s8y6", "")
E._maybe_coupled(base)
info = E.make(base)
import classy
st = json.load(open(f"{E.OUT}/cmp_{run}.json"))["minimum"]
a = dict(info["theory"]["classytwist"]["extra_args"])
a.update({"A_s": 1e-10 * np.exp(st["logA"]), "n_s": st["n_s"], "100*theta_s": st["theta_s_1e2"], "omega_b": st["omega_b"],
          "omega_cdm": st["omega_cdm"], "tau_reio": st["tau_reio"]})
for k in ("output", "lensing", "l_max_scalars", "non_linear", "P_k_max_1/Mpc"): a.pop(k, None)
if "scf_coupling_beta" in st:
    import spiral_guess
    k = st.get("spiral_kappa", 1.0); b = st["scf_coupling_beta"]
    a["scf_coupling_beta"] = b
    a["scf_parameters"] = f"{k}, 0.0, {spiral_guess.mu1_guess(k, b, st['omega_b'], st['omega_cdm'])}, 0.0, 0.0, 0.0"
c = classy.Class(); c.set(a); c.compute()
D = os.path.join(AEGIS, "cmb-fit", "packages", "data", "sn_data", "PantheonPlus")
d = np.genfromtxt(os.path.join(D, "Pantheon+SH0ES.dat"), names=True, dtype=None, encoding=None)
# D_L with zHD (cosmological) and zHEL for the (1+z) factor, as Pantheon+
dl = np.array([c.angular_distance(zh) * (1 + zh) * (1 + zl) for zh, zl in zip(d["zHD"], d["zHEL"])])
bg = c.get_background(); rd = c.rs_drag()
np.save(outp, dl)
print(json.dumps({"run": run, "H0": c.h() * 100, "rd": rd, "H0_stored": st.get("H0")}))
