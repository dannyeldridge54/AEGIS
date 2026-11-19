"""D1636 full-Planck arm (PREREG_D1636_PLANCK.md): reverse thread (thawing species-plateau dark energy) on the same data
and engine as the stored cmp_lcdmP / cmp_w0waP fits: CAMB 2.0.5 + Cobaya 3.6.2 (venv312), Planck 2018 (lowl TT, EE,
plik-lite TTTEEE, lensing) + DESI DR2 BAO + one supernova set.

    python rt_planck_fit.py gate                   G: u_i -> 1e-6 reproduces the stored LCDM chi2 (<= 1.0) -> results/rtP_gate.json
    python rt_planck_fit.py rtP[_union3|_desy5]     one fit, bobyqa best of 4 -> results/cmp_rtP*.json
    python rt_planck_fit.py w0waP_desy5             the missing w0-wa reference (same recipe as ub2_fit.py w0waP)

Model: V = V_L (1 - A e^{-beta phi}), A = 16 zeta(2)/(3 zeta(3)), beta = 2 sqrt 2; field frozen at a = 1e-3 with
A e^{-beta phi_i} = u_i; V_L fixed by flatness; w(a) handed to CAMB's PPF dark energy as a table (the same fluid
approximation the stored ub2 / w0waP fits use).
"""
import json, math, os, sys, time
import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cmbfit as C            # noqa: E402

A_PL = 16 * 1.6449340668482264 / (3 * 1.2020569031595942)
BETA = 2 * math.sqrt(2)
OMNU = 0.06 / 93.14


def rt_wtable(u_i, Om, Or, beta=BETA):
    Ode = 1 - Om - Or
    phi_i = math.log(A_PL / u_i) / beta

    def run(VL):
        V = lambda p: VL * (1 - A_PL * math.exp(-beta * p))
        dV = lambda p: VL * A_PL * beta * math.exp(-beta * p)

        def rhs(N, y):
            p, v = y; a = math.exp(N); rm, rr = 3 * Om / a ** 3, 3 * Or / a ** 4
            H2 = (rm + rr + V(p)) / (3 - v * v / 2); eps = (rm + 4 * rr / 3 + H2 * v * v) / (2 * H2)
            return [v, -(3 - eps) * v - dV(p) / H2]
        ev = lambda N, y: V(y[0]); ev.terminal = True
        sol = solve_ivp(rhs, (math.log(1e-3), 0.0), [phi_i, 0.0], rtol=1e-8, atol=1e-10, events=ev, dense_output=True)
        if sol.status == 1:
            return None, None
        p, v = sol.y[:, -1]; H2 = (3 * Om + 3 * Or + V(p)) / (3 - v * v / 2)
        return sol, (H2 * v * v / 2 + V(p)) / (3 * H2)

    VL = 3 * Ode / (1 - u_i)
    for _ in range(30):
        sol, Ophi = run(VL)
        if sol is None:
            return None
        if abs(Ophi / Ode - 1) < 1e-7:
            break
        VL *= Ode / Ophi
    Ns = np.linspace(math.log(1e-3), 0.0, 400); w = []
    for N in Ns:
        p, v = sol.sol(N); a = math.exp(N); Vp = VL * (1 - A_PL * math.exp(-beta * p))
        H2 = (3 * Om / a ** 3 + 3 * Or / a ** 4 + Vp) / (3 - v * v / 2); K = H2 * v * v / 2
        w.append((K - Vp) / (K + Vp))
    return np.concatenate([[1e-8, 9.99e-4], np.exp(Ns)]), np.concatenate([[-1.0, -1.0], w])


def rt_theory():
    from cobaya.theories.camb import CAMB
    from camb.dark_energy import DarkEnergyPPF

    class RTCamb(CAMB):
        def set(self, params_values_dict, state):
            p = dict(params_values_dict); ui = p.pop("rt_ui", None)
            cp = super().set(p, state)
            if cp is None or ui is None:
                return cp
            h = cp.H0 / 100
            Om = (cp.ombh2 + cp.omch2 + OMNU) / h ** 2; Or = 2.4728e-5 * (1 + 0.2271 * 3.044) / h ** 2
            tab = rt_wtable(ui, Om, Or)
            if tab is None:
                return None
            de = DarkEnergyPPF(); de.set_w_a_table(tab[0], tab[1]); cp.DarkEnergy = de
            return cp

        def get_helper_theories(self):
            helpers = super().get_helper_theories()
            tr = self._camb_transfers; base = tr.get_can_support_params
            tr.get_can_support_params = lambda: set(base()) | {"rt_ui"}
            return helpers
    return RTCamb


SN = {"_union3": "sn.union3", "_desy5": "sn.desy5"}


def make(name):
    core, sn = name, None
    for suf, like in SN.items():
        if core.endswith(suf):
            core, sn = core[:-len(suf)], like
    info = C.make_info("lcdm", sampler={"minimize": {"method": "bobyqa", "best_of": 4}},
                       output=os.path.join(C.RESULTS, "chains", "cmp_" + name))
    if sn:
        info["likelihood"].pop("sn.pantheonplus"); info["likelihood"][sn] = None
    pr = info["params"]
    ref = json.load(open(os.path.join(C.RESULTS, f"cmp_lcdmP{name[len(core):]}.json")))["minimum"]
    for k in ("logA", "ns", "ombh2", "omch2", "tau"):
        pr[k]["ref"] = {"dist": "norm", "loc": ref[k], "scale": pr[k]["proposal"]}
    if core == "w0waP":
        info["theory"]["camb"]["extra_args"]["dark_energy_model"] = "ppf"
        pr["w"] = {"prior": {"min": -3.0, "max": 1.0}, "ref": {"dist": "norm", "loc": -0.8, "scale": 0.05}, "proposal": 0.05}
        pr["wa"] = {"prior": {"min": -3.0, "max": 2.0}, "ref": {"dist": "norm", "loc": -0.6, "scale": 0.1}, "proposal": 0.1}
        info["prior"] = {"w0wa_bound": "lambda w, wa: 0.0 if w + wa < 0 else -np.inf"}
        return info, ref
    if core != "rtP":
        raise SystemExit(f"unknown run {name}")
    for k in ("theta_s_100", "thetastar"):
        pr.pop(k)
    pr["H0"] = {"prior": {"min": 55.0, "max": 85.0}, "ref": {"dist": "norm", "loc": ref["H0"], "scale": 0.5}, "proposal": 0.5}
    pr["rt_ui"] = {"prior": {"min": 1e-6, "max": 0.3}, "ref": {"dist": "uniform", "min": 0.05, "max": 0.22}, "proposal": 0.02}
    ex = info["theory"]["camb"]["extra_args"]; ex.pop("theta_H0_range", None); ex["dark_energy_model"] = "ppf"
    info["theory"] = {"rtcamb": {"external": rt_theory(), "extra_args": ex, "stop_at_error": False}}
    return info, ref


def chi2_at(info, point):
    import copy
    from cobaya.model import get_model
    i = copy.deepcopy(info); i.pop("sampler", None); i.pop("output", None)
    m = get_model(i); sp = m.parameterization.sampled_params()
    return -2 * sum(m.loglikes({k: point[k] for k in sp}, as_dict=True)[0].values())


def gate():
    info, ref = make("rtP")
    c = chi2_at(info, dict(ref, rt_ui=1e-6))
    out = {"chi2_LCDM_stored": ref["chi2"], "chi2_rtP_ui_1e-6": c, "diff": c - ref["chi2"], "pass": abs(c - ref["chi2"]) <= 1.0}
    json.dump(out, open(os.path.join(C.RESULTS, "rtP_gate.json"), "w"), indent=1); print(json.dumps(out), flush=True)


def run(name):
    from cobaya import run as crun
    t = time.time(); info, _ = make(name)
    upd, sampler = crun(info)
    row = {k: float(v) for k, v in sampler.products()["minimum"].data.iloc[0].items()
           if isinstance(v, (int, float, np.integer, np.floating))}
    json.dump({"run": name, "engine": "CAMB (PPF w-table)" if name.startswith("rtP") else "CAMB", "seconds": time.time() - t,
               "minimum": row}, open(os.path.join(C.RESULTS, f"cmp_{name}.json"), "w"), indent=2)
    print("done", name, row.get("H0"), row.get("chi2"), flush=True)


if __name__ == "__main__":
    C.lower_priority()
    lock = os.path.join(HERE, "..", "field_tests", "rules", "PREREG_D1636_PLANCK.md.sha256")
    if not os.path.exists(lock):
        raise SystemExit("PREREG_D1636_PLANCK not locked")
    gate() if sys.argv[1] == "gate" else run(sys.argv[1])
