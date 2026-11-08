"""UB-2: the unified BI axion-dilaton against data (field_tests/rules/DRAFT_PREREG_UNIFY_DATA.md; runs only once locked).
CAMB 2.0.5 + Cobaya 3.6.2 (venv312), Planck 2018 + DESI DR2 + one supernova set, as the stored lcdmP / edelockP fits.

    python ub2_fit.py gates                  G1-G3 engine checks -> results/ub2_gates.json (no UB-2 fit involved)
    python ub2_fit.py ub2A[_dovekie|_union3]  one fit (variant A, derived potential), best of 4 -> results/cmp_<name>.json
    python ub2_fit.py ub2B[...]               variant B (exponential dilaton, kappa free)
    python ub2_fit.py ub2C[...]               variant C (derived potential with W = W0 exp(b Phi), b free; UB-1b)
    python ub2_fit.py w0waP[...]              the w0-wa reference on the same data and engine

Model: theory/unify_hyperbolic_bg.py (UB-1), same fields, metric, potentials and constants. For each point: a ΛCDM-like
CAMB background gives every non-field density (radiation, massive neutrinos, matter) exactly; the two-field equations
are solved on it, A is fixed by flatness, and the field's density history goes to CAMB as one dark-energy fluid
(w(a) table, rest-frame sound speed 1). That last step is the approximation the gates test.
"""
import copy
import json
import math
import os
import sys
import time

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "theory"))
import unify_hyperbolic_bg_ub1b as UB     # noqa: E402  (= UB-1 D1 code + variant C)  (fields, metric, potentials, constants: one definition)
import cmbfit as C                       # noqa: E402

NA = 3000
LNA = np.linspace(math.log(1e-7), 0.0, NA)          # w-table grid (ln a)
UB_PARAMS = {
    "ub_lnL": (0.0, 40.0, 22.70, 0.5, r"\ln L"),      # starts at the UB-1 D1 passing point (no data used there)
    "ub_thi": (0.1, 3.0, 2.426, 0.05, r"\theta_i"),
    "ub_phii": (1.1, 60.0, 12.41, 0.5, r"|\phi|_i"),
}
UB_KAPPA = ("ub_kappa", (-3.0, 3.0, -0.145, 0.05, r"\kappa"))
UB_B = ("ub_b", (0.0, 2.9, 1.0, 0.1, "b"))


class FieldError(Exception):
    pass


def other_densities(cp):
    """CAMB's own non-dark-energy densities for these cosmological parameters, as H^2 contributions in units of H0^2,
    with (rho + p) from the slope. Returns callables of N = ln a."""
    import camb
    p = cp.copy()
    p.set_dark_energy(w=-1.0)
    res = camb.get_background(p, no_thermo=True)
    a = np.exp(LNA)
    d = res.get_background_densities(a, vars=["tot", "de"])
    h0 = p.H0 / 299792.458
    x = (d["tot"] - d["de"]) / a ** 4 / 3 / h0 ** 2         # rho_other / (3 H0^2), i.e. its share of H^2 / H0^2
    sp = CubicSpline(LNA, np.log(x))
    return (lambda N: math.exp(sp(N))), (lambda N: -math.exp(sp(N)) * sp(N, 1) / 3), float(x[-1])


def field_history(par, var, rho, rhop, other0):
    """Solve UB-1's equations on the given non-field background; A fixed by flatness (H(today) = H0).
    Returns rho_field(N)/rho_field(0) on LNA and diagnostics."""
    lnL, thi, phii = par["ub_lnL"], par["ub_thi"], par["ub_phii"]
    k = par.get("ub_kappa", par.get("ub_b", 0.0))
    L = math.exp(lnL)
    c0 = math.log(phii) / UB.S
    need = 1.0 - other0                                      # field share of H0^2 today (flat)
    if need <= 0:
        raise FieldError("no room for the field")

    def make(A):
        def parts(N, y):
            c, th, cp, tp = y
            u, du = UB.U(c, var, k)
            f2 = UB.F(c) ** 2
            V = (A * u + L * (1 - math.cos(th)) ** 3) / 3     # in units of 3 H0^2, like rho
            K = (cp * cp + f2 * tp * tp) / 2
            H2 = (rho(N) + V) / (1 - K / 3)
            if not (H2 > 0 and math.isfinite(H2) and K < 3):
                raise ValueError(f"N={N:.3f} y={[float(v) for v in y]} K={K:.3g} H2={H2:.3g}")
            return V, K, H2, du, f2

        def rhs(N, y):
            c, th, cp, tp = y
            V, K, H2, du, f2 = parts(N, y)
            eps = K + 3 * rhop(N) / (2 * H2)
            vth = L * 3 * (1 - math.cos(th)) ** 2 * math.sin(th)
            return [cp, tp, -(3 - eps) * cp + UB.LAM / 2 * f2 * tp * tp - A * du / H2,   # V here is in units of 3 H0^2, so the force is 3 dV/(H^2/H0^2)
                    -(3 - eps) * tp - UB.LAM * cp * tp - vth / (f2 * H2)]
        return parts, rhs

    def today(lnA):
        parts, rhs = make(math.exp(lnA))
        try:
            s = solve_ivp(rhs, (LNA[0], 0.0), [c0, thi, 0.0, 0.0], method=os.environ.get("UB_METHOD", "DOP853"), rtol=1e-8, atol=1e-11,
                          dense_output=True)
        except (ValueError, OverflowError, ZeroDivisionError) as e:
            if os.environ.get("UB_DEBUG"):
                print("solve error", lnA, repr(e))
            return None, None
        if s.status != 0:
            if os.environ.get("UB_DEBUG"):
                print("solve status", lnA, s.message)
            return None, None
        V, K, H2, _, _ = parts(0.0, s.sol(0.0))
        return H2 - 1.0, (s, parts)

    lo, hi = (-400.0, 10.0) if var == "A" else (-60.0, 10.0)
    xs = np.linspace(lo, hi, 60)
    vals = [today(x)[0] for x in xs]
    br = [(xs[i], xs[i + 1]) for i in range(len(xs) - 1)
          if vals[i] is not None and vals[i + 1] is not None and vals[i] * vals[i + 1] < 0]
    if not br:
        raise FieldError("flatness not reachable")
    lnA = brentq(lambda x: today(x)[0] if today(x)[0] is not None else 1.0, *br[0], xtol=1e-10)
    _, (s, parts) = today(lnA)
    rf = np.empty(NA)
    tab = {k: np.empty(NA) for k in ("chi", "th", "chiN", "thN", "H2")}
    for i, N in enumerate(LNA):
        y = s.sol(N)
        V, K, H2, _, _ = parts(N, y)
        rf[i] = K * H2 / 3 + V                                  # field density in units of 3 H0^2
        tab["chi"][i], tab["th"][i], tab["chiN"][i], tab["thN"][i], tab["H2"][i] = y[0], y[1], y[2], y[3], H2
    if not np.all(rf > 0):
        raise FieldError("negative field density")
    tab.update(A=math.exp(lnA), L=L, var=var, k=k)
    return rf, lnA, tab


def ub_darkenergy(tab, H0):
    """The two-field CAMB module (cmb-fit/ub2_camb/DarkEnergyUBField.f90, a CAMB 2.0.5 build that includes it): the
    background table plus both fields' perturbations. 8piG V = H0^2 (A u + L (1-cos)^3) in 1/Mpc^2; conformal-time
    derivatives d/dtau = a H d/dN."""
    from camb.dark_energy import UBField
    h0 = H0 / 299792.458
    a = np.exp(LNA)
    aH = a * h0 * np.sqrt(tab["H2"])
    de = UBField()
    de.var = {"A": 1, "B": 2, "C": 3}[tab["var"]]
    de.kpar = tab["k"]
    de.VA = h0 ** 2 * tab["A"]
    de.VL = h0 ** 2 * tab["L"]
    de.lam = UB.LAM
    de.FP = UB.FP
    de.set_table(LNA, tab["chi"], tab["th"], tab["chiN"] * aH, tab["thN"] * aH)
    return de


def ub_theory():
    from cobaya.theories.camb import CAMB

    class UBCamb(CAMB):
        """CAMB whose dark energy is the UB field, given as a fluid w(a) table computed per point."""
        def set(self, params_values_dict, state):
            p = dict(params_values_dict)
            ub = {k: p.pop(k) for k in list(p) if k.startswith("ub_")}
            cp = super().set(p, state)
            if cp is None or not ub:
                return cp
            var = "B" if "ub_kappa" in ub else "C" if "ub_b" in ub else "A"
            try:
                rho, rhop, other0 = other_densities(cp)
                rf, lnA, tab = field_history(ub, var, rho, rhop, other0)
            except (FieldError, ValueError, OverflowError) as e:
                self.log.debug("UB field failed: %s", e)
                return None
            cp.DarkEnergy = ub_darkenergy(tab, cp.H0)
            state.setdefault("derived_extra", {})["ub_lnA"] = lnA
            return cp

        def get_helper_theories(self):
            # The UB parameters change the background, so they must reach CAMB's transfer step (CambTransfers), which
            # is what calls set(); cobaya routes a parameter to the helper whose get_can_support_params lists it.
            helpers = super().get_helper_theories()
            tr = self._camb_transfers
            base = tr.get_can_support_params
            tr.get_can_support_params = lambda: set(base()) | set(UB_PARAMS) | {UB_KAPPA[0], UB_B[0]}
            return helpers

    return UBCamb


SN = {"_dovekie": "sn.desdovekie", "_union3": "sn.union3"}


def make(name):
    sn = None
    core = name
    for suf, like in SN.items():
        if core.endswith(suf):
            core, sn = core[:-len(suf)], like
    info = C.make_info("lcdm", sampler={"minimize": {"method": "bobyqa", "best_of": 4}},
                       output=os.path.join(C.RESULTS, "chains", "cmp_" + name))
    if sn:
        info["likelihood"].pop("sn.pantheonplus")
        info["likelihood"][sn] = None
    pr = info["params"]
    ref = json.load(open(os.path.join(C.RESULTS, f"cmp_lcdmP{name[len(core):]}.json")))["minimum"]
    for k in ("logA", "ns", "ombh2", "omch2", "tau"):
        pr[k]["ref"] = {"dist": "norm", "loc": ref[k], "scale": pr[k]["proposal"]}
    if core == "w0waP":
        ex = info["theory"]["camb"]["extra_args"]
        ex["dark_energy_model"] = "ppf"
        pr["w"] = {"prior": {"min": -3.0, "max": 1.0}, "ref": {"dist": "norm", "loc": -0.8, "scale": 0.05},
                   "proposal": 0.05, "latex": "w_0"}
        pr["wa"] = {"prior": {"min": -3.0, "max": 2.0}, "ref": {"dist": "norm", "loc": -0.6, "scale": 0.1},
                    "proposal": 0.1, "latex": "w_a"}
        info["prior"] = {"w0wa_bound": "lambda w, wa: 0.0 if w + wa < 0 else -np.inf"}
        return info
    if core not in ("ub2A", "ub2B", "ub2C"):
        raise SystemExit(f"unknown run {name}")
    # H0 is sampled directly: the field history depends on Omega_m, so CAMB's theta -> H0 search cannot be used.
    for k in ("theta_s_100", "thetastar"):
        pr.pop(k)
    pr["H0"] = {"prior": {"min": 55.0, "max": 85.0}, "ref": {"dist": "norm", "loc": ref["H0"], "scale": 0.5},
                "proposal": 0.5, "latex": "H_0"}
    info["theory"] = {"ubcamb": {"external": ub_theory(), "extra_args": info["theory"]["camb"]["extra_args"],
                                 "stop_at_error": False}}
    info["theory"]["ubcamb"]["extra_args"].pop("theta_H0_range", None)
    keys = dict(UB_PARAMS)
    if core == "ub2B":
        keys[UB_KAPPA[0]] = UB_KAPPA[1]
    if core == "ub2C":
        keys[UB_B[0]] = UB_B[1]
    box = json.load(open(BOX)) if os.path.exists(BOX) else {}
    for k, (lo, hi, loc, sc, tex) in keys.items():
        lo, hi = box.get(k, (lo, hi))
        pr[k] = {"prior": {"min": lo, "max": hi}, "ref": {"dist": "norm", "loc": min(max(loc, lo), hi), "scale": sc},
                 "proposal": sc, "latex": tex}
    return info


BOX = os.path.join(HERE, "results", "ub2_box.json")   # written from UB-1's passing region when UB-2 is locked


def chi2_at(info, point):
    from cobaya.model import get_model
    i = copy.deepcopy(info)
    for k in ("sampler", "output"):
        i.pop(k, None)
    m = get_model(i)
    sp = m.parameterization.sampled_params()
    lp = m.loglikes({k: point[k] for k in sp}, as_dict=True)[0]
    return -2 * sum(lp.values())


def eq_replica(r):
    """UBField with lam = 0 and a constant dilaton term that reproduces a CAMB EarlyQuintessence + Lambda result r."""
    from camb.dark_energy import UBField
    eq = r.Params.DarkEnergy
    G, hbar, c, Mpc = 6.67430e-11, 1.054571817e-34, 2.99792458e8, 3.085677581e22
    units = (Mpc / c) ** 2 / (8 * math.pi * G * hbar / c ** 5)
    a = np.asarray(eq.sampled_a)
    de = UBField()
    de.var, de.kpar, de.lam, de.FP = 2, 0.0, 0.0, eq.f
    de.VA, de.VL = r.grhov, units * eq.m ** 2 * eq.f ** 2
    de.set_table(np.log(a), np.zeros_like(a), np.asarray(eq.phi_a) / eq.f, np.zeros_like(a), np.asarray(eq.phidot_a) / eq.f)
    return de


def gates():
    """G1: the two-field module (lam = 0 replica) at the stored Locked Twist best fit reproduces CAMB's EarlyQuintessence
    chi2 (<= 1.0). G2: a UB point with the angle negligible and a flat dilaton reproduces the stored LCDM chi2 (<= 1.0).
    G3: CAMB's H(z) with the module matches the stand-alone two-field solver (<= 1e-3)."""
    import camb
    import cmbfit_compare as CC
    from cobaya.theories.camb import CAMB
    out = {}
    lt = json.load(open(os.path.join(C.RESULTS, "cmp_edelockP.json")))["minimum"]
    info = CC.make("edelockP")
    c_full = chi2_at(info, lt)
    m = info["theory"]["camb"]["extra_args"]
    zc = lt.get("zc") or (lt["ombh2"] + lt["omch2"]) / (2.4728e-5 * (1 + 0.22711 * 3.044)) - 1
    p = camb.set_params(H0=lt["H0"], ombh2=lt["ombh2"], omch2=lt["omch2"], mnu=0.06, num_massive_neutrinos=1,
                        nnu=3.044, tau=lt["tau"], As=1e-10 * math.exp(lt["logA"]), ns=lt["ns"],
                        dark_energy_model="EarlyQuintessence", n=3, use_zc=True, zc=zc, fde_zc=lt["fde_zc"],
                        theta_i=lt["theta_i"], bbn_predictor=m["bbn_predictor"])
    rep = eq_replica(camb.get_background(p))

    class ReplicaCamb(CAMB):
        def set(self, pv, state):
            cp = super().set(pv, state)
            if cp is not None:
                cp.DarkEnergy = rep
            return cp

    fl = C.make_info("lcdm")
    fl["params"].pop("theta_s_100"); fl["params"].pop("thetastar")
    fl["params"]["H0"] = {"prior": {"min": 20.0, "max": 100.0}, "ref": lt["H0"]}
    fl["theory"] = {"replicacamb": {"external": ReplicaCamb, "extra_args": {k: v for k, v in m.items() if k not in
                    ("dark_energy_model", "n", "use_zc", "theta_H0_range")}, "stop_at_error": False}}
    c_rep = chi2_at(fl, dict(lt))
    out["G1"] = {"chi2_EarlyQuintessence": round(c_full, 3), "chi2_two_field_module": round(c_rep, 3),
                 "diff": round(c_rep - c_full, 3), "pass": abs(c_rep - c_full) <= 1.0}
    lc = json.load(open(os.path.join(C.RESULTS, "cmp_lcdmP.json")))["minimum"]
    info = make("ub2B")
    c_ub = chi2_at(info, dict(lc, ub_lnL=0.0, ub_thi=0.1, ub_phii=10.0, ub_kappa=0.0))
    out["G2"] = {"chi2_LCDM_stored": round(lc["chi2"], 3), "chi2_UB_limit": round(c_ub, 3),
                 "diff": round(c_ub - lc["chi2"], 3), "pass": abs(c_ub - lc["chi2"]) <= 1.0}
    out["G3"] = g3(lc["H0"], lc["ombh2"], lc["omch2"])
    out["all_pass"] = all(v["pass"] for v in out.values() if isinstance(v, dict))
    conv = lambda o: o.item() if hasattr(o, "item") else str(o)     # numpy bool/float -> JSON
    json.dump(out, open(os.path.join(C.RESULTS, "ub2_gates.json"), "w"), indent=1, default=conv)
    print(json.dumps(out, indent=1, default=conv))


def g3(H0, ombh2, omch2, par=None, var="B"):
    """Background consistency, no data: CAMB with the module vs the stand-alone solver, z = 0 to 3000."""
    import camb
    p = camb.set_params(H0=H0, ombh2=ombh2, omch2=omch2, mnu=0.06, num_massive_neutrinos=1, nnu=3.044,
                        As=2.1e-9, ns=0.965)
    rho, rhop, other0 = other_densities(p)
    par = par or {"ub_lnL": 20.0, "ub_thi": 2.5, "ub_phii": 10.0, "ub_kappa": 0.5}
    try:
        rf, lnA, tab = field_history(par, var, rho, rhop, other0)
    except FieldError as e:
        return {"error": str(e), "pass": False}
    p.DarkEnergy = ub_darkenergy(tab, H0)
    r = camb.get_background(p, no_thermo=True)
    zs = np.geomspace(1e-3, 3000.0, 80)
    hc = np.array([r.hubble_parameter(z) for z in zs]) / H0
    hs = np.array([math.sqrt(rho(-math.log(1 + z)) + math.exp(np.interp(-math.log(1 + z), LNA, np.log(rf)))) for z in zs])
    dev = float(np.max(np.abs(hc / hs - 1)))
    return {"max_rel_H_diff": dev, "pass": dev <= 1e-3}


def run(name):
    from cobaya import run as crun
    t = time.time()
    upd, sampler = crun(make(name))
    row = {k: float(v) for k, v in sampler.products()["minimum"].data.iloc[0].items()
           if isinstance(v, (int, float, np.integer, np.floating))}
    json.dump({"run": name, "engine": "CAMB (UB fluid)" if name.startswith("ub2") else "CAMB", "seconds": time.time() - t,
               "minimum": row}, open(os.path.join(C.RESULTS, f"cmp_{name}.json"), "w"), indent=2)
    print("done", name, row.get("H0"), row.get("chi2"), flush=True)


if __name__ == "__main__":
    C.lower_priority()
    if sys.argv[1] == "gates":
        gates()
    else:
        lock = os.path.join(HERE, "..", "field_tests", "rules", "PREREG_UNIFY_DATA.md.sha256")
        if sys.argv[1].startswith("ub2") and not os.path.exists(lock):
            raise SystemExit("UB-2 is not locked yet (field_tests/rules/PREREG_UNIFY_DATA.md.sha256 missing)")
        for n in sys.argv[1:]:
            run(n)
