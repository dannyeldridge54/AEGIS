"""Frozen forward predictions for the Locked Twist (CAMB EarlyQuintessence n = 3, settings as
field_tests/S8_WL/part2/aegis_camb.py) at the stored edelockP best fits. Same output fields as forward_predictions_cloud.py
(BAO, H0, r_d, f*sigma8, sigma8, S8); gate: sigma8 equals the stored value to 1e-3.
    python forward_predictions_camb.py edelockP edelockP_dovekie edelockP_union3  -> theory/fpc_<run>.json"""
import json, math, os, sys
import numpy as np
import camb
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.environ.get("TWIST_RESULTS", os.path.join(HERE, "..", "cmb-fit", "results"))
ZB = [0.295, 0.51, 0.706, 0.934, 1.321, 1.484, 2.33, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.6, 2.0, 2.6, 3.0]


def run(name):
    m = json.load(open(os.path.join(RES, f"cmp_{name}.json")))["minimum"]
    zc = m.get("zc") or (m["ombh2"] + m["omch2"]) / (2.4728e-5 * (1 + 0.22711 * 3.044)) - 1
    p = camb.set_params(H0=m["H0"], ombh2=m["ombh2"], omch2=m["omch2"], mnu=0.06, num_massive_neutrinos=1, nnu=3.044,
                        tau=m["tau"], As=m["As"], ns=m["ns"], dark_energy_model="EarlyQuintessence", n=3, use_zc=True,
                        zc=zc, fde_zc=m["fde_zc"], theta_i=m["theta_i"])
    zs = [0.0, 0.3, 0.5, 0.7, 1.0, 1.5]
    p.set_matter_power(redshifts=zs, kmax=5.0); p.WantCls = False
    r = camb.get_results(p)
    rd = r.get_derived_params()["rdrag"]
    bao = {}
    for z in ZB:
        dm = r.comoving_radial_distance(z); dh = 299792.458 / r.hubble_parameter(z)
        bao[f"{z:g}"] = {"DM_rd": dm / rd, "DH_rd": dh / rd, "DV_rd": (z * dm * dm * dh) ** (1 / 3) / rd}
    s8z = r.get_sigma8()[::-1]; fs8 = r.get_fsigma8()[::-1]
    s8 = float(s8z[0]); wm = m["ombh2"] + m["omch2"] + 0.06 / 93.14
    out = {"run": name, "engine": "CAMB EarlyQuintessence n=3", "H0": m["H0"], "r_d": rd, "BAO": bao,
           "fsigma8": {f"{z:g}": float(v) for z, v in zip(zs, fs8)}, "sigma8": s8,
           "S8": s8 * math.sqrt(wm / (m["H0"] / 100) ** 2 / 0.3), "sigma8_stored": m["sigma8"],
           "gate_sigma8": "PASS" if abs(s8 - m["sigma8"]) < 1e-3 else "FAIL", "w0_cpl": None, "wa_cpl": None}
    json.dump(out, open(os.path.join(HERE, f"fpc_{name}.json"), "w"), indent=1, default=float)
    print(name, "H0 %.2f rd %.2f S8 %.4f sigma8 %.4f stored %.4f %s" % (m["H0"], rd, out["S8"], s8, m["sigma8"], out["gate_sigma8"]))


if __name__ == "__main__":
    for n in sys.argv[1:]:
        run(n)
