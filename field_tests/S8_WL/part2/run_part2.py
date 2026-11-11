"""S8-WL Part 2 (field_tests/rules/PREREG_S8_WL.md, locked 7 Nov 2026): full DES Y3 cosmic-shear likelihood (CosmoSIS
standard library, fiducial scale cuts, TATT intrinsic alignments, Y3 priors) at the STORED best fits, cosmology fixed,
minimised over the survey nuisance parameters only. Delta_WL = chi2_WL(model) - chi2_WL(LCDM); PASSES if <= +2.
    CSL_DIR=<cosmosis-standard-library> python run_part2.py [pairs...]     -> ../results/part2_desy3.json
chi2_WL is -2 ln(posterior) at the nuisance-only maximum (likelihood x the survey's own nuisance priors); the pure
data chi2 (data_vector/2pt_chi2) is reported beside it."""
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AEGIS = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
RES = os.environ.get("TWIST_RESULTS", os.path.join(AEGIS, "cmb-fit", "results"))
CSL = os.environ["CSL_DIR"]
OUT = os.path.join(HERE, "..", "results")
PAIRS = {"Locked Twist (Planck+DESI+Pantheon+)": (("edelock", "edelockP"), ("lcdm", "lcdmP")),
         "UB-2 joined field, Pantheon+": (("ub", "ub2B"), ("lcdm", "lcdmP")),
         "UB-2 joined field, DES-Dovekie": (("ub", "ub2B_dovekie"), ("lcdm", "lcdmP_dovekie")),
         "UB-2 joined field, Union3": (("ub", "ub2B_union3"), ("lcdm", "lcdmP_union3"))}
# Spiral pairs: AxiCLASS (coupled build) power spectra written by axiclass_pk.py, loaded with load_pk.py
PAIRS.update({"Spiral, Pantheon+": (("pk", "ax_spa_spiraltwist_nlfix"), ("pk", "ax_spa_lcdm_halofit")),
              "Spiral, DES-Dovekie": (("pk", "ax_spa_spiraltwist_dovekie_nlfix"), ("pk", "ax_spa_lcdm_halofit_dovekie")),
              "Spiral, Union3": (("pk", "ax_spa_spiraltwist_union3_nlfix"), ("pk", "ax_spa_lcdm_halofit_union3"))})
# S8-J (PREREG_S8_JOINT.md, reported: Part 2 Delta_WL at the joint best fits) and S8-L (PREREG_SPIRAL_L.md, reported)
def _better_lcdm(suf):
    """S8J-D3: the LCDM+S8 reference is whichever of _s8y6 / _s8y6_more has the lower chi2."""
    res = os.environ.get("TWIST_RESULTS", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "cmb-fit", "results"))
    best, name = None, f"ax_spa_lcdm_halofit{suf}_s8y6"
    for n in (name, name + "_more"):
        p = os.path.join(res, f"cmp_{n}.json")
        if os.path.exists(p):
            c = json.load(open(p))["minimum"]["chi2"]
            if best is None or c < best:
                best, name = c, n
    return name


for sn, suf in (("Pantheon+", ""), ("DES-Dovekie", "_dovekie"), ("Union3", "_union3")):
    PAIRS[f"S8-J joint Spiral, {sn}"] = (("pk", f"ax_spa_spiraltwist{suf}_nlfix_s8y6"), ("pk", _better_lcdm(suf)))
    PAIRS[f"S8-L light angle, {sn}"] = (("pk", f"spiralL{suf}"), ("pk", f"ax_spa_lcdm_halofit{suf}"))
    # S8-LNL (PREREG_S8L_NONLINEAR.md): same pairs, nonlinear power from axionHMcode on both sides (nonlinear/axhm_pk.py);
    # cmp_<run>_axhm.json = the stored fit's own file (TWIST_RESULTS folder with links)
    PAIRS[f"S8-LNL axionHMcode, {sn}"] = (("pk", f"spiralL{suf}_axhm"), ("pk", f"ax_spa_lcdm_halofit{suf}_axhm"))
    PAIRS[f"S8-A axionHMcode, {sn}"] = (("pk", f"S8A{suf}_axhm"), ("pk", f"ax_spa_lcdm_halofit{suf}_axhm"))   # LATE-BASE
    # FLAG-1 (PREREG_FLAGSHIP.md: shear rules rerun at the flagship best fits, reported), same partners as S8-J
    PAIRS[f"FLAG-1 flagship, {sn}"] = (("pk", f"ax_spa_spiraltwist_kappa1{suf}_nlfix_s8y6"), ("pk", _better_lcdm(suf)))
SPIRAL = []

VALUES = """[cosmological_parameters]
h0 = {h0}
ombh2 = {ombh2}
omch2 = {omch2}
omega_k = 0.0
mnu = 0.06
num_massive_neutrinos = 1
nnu = 3.044
A_s = {As}
n_s = {ns}
tau = {tau}
w = -1.0
wa = 0.0

[shear_calibration_parameters]
m1 = -0.1 -0.0063 0.1
m2 = -0.1 -0.0198 0.1
m3 = -0.1 -0.0241 0.1
m4 = -0.1 -0.0369 0.1

[wl_photoz_errors]
bias_1 = -0.1 0.0 0.1
bias_2 = -0.1 0.0 0.1
bias_3 = -0.1 0.0 0.1
bias_4 = -0.1 0.0 0.1

[intrinsic_alignment_parameters]
z_piv = 0.62
A1 = -5.0 0.7 5.0
A2 = -5.0 -1.36 5.0
alpha1 = -5.0 -1.7 5.0
alpha2 = -5.0 -2.5 5.0
bias_ta = 0.0 1.0 2.0
"""

PIPE = """[runtime]
sampler = {sampler}
verbosity = quiet

[DEFAULT]
2PT_FILE = likelihood/des-y3/2pt_NG_final_2ptunblind_02_24_21_wnz_covupdate.v2.fits

[maxlike]
method = Nelder-Mead
tolerance = 1e-3
maxiter = 6000
output_ini = {out}_best.ini
max_posterior = T

[output]
filename = {out}.txt
format = text

[pipeline]
modules = consistency camb fast_pt fits_nz source_photoz_bias IA pk_to_cl add_intrinsic 2pt_shear shear_m_bias 2pt_like
values = {values}
priors = examples/des-y3-priors.ini
extra_output = cosmological_parameters/sigma_8 data_vector/2pt_chi2
timing = F
debug = F

[consistency]
file = utility/consistency/consistency_interface.py

[camb]
file = {module}
aegis_model = {model}
aegis_point = {point}
mode = power
lmax = 2500
feedback = 0
AccuracyBoost = 1.1
do_tensors = F
do_lensing = F
NonLinear = pk
halofit_version = takahashi
zmin_background = 0.
zmax_background = 4.
nz_background = 401
kmin = 1e-4
kmax = 50.0
kmax_extrapolate = 500.0
nk = 700

[fits_nz]
file = number_density/load_nz_fits/load_nz_fits.py
nz_file = %(2PT_FILE)s
data_sets = source
prefix_section = T
prefix_extension = T

[source_photoz_bias]
file = number_density/photoz_bias/photoz_bias.py
mode = additive
sample = nz_source
bias_section = wl_photoz_errors
interpolation = linear

[fast_pt]
file = structure/fast_pt/fast_pt_interface.py
do_ia = T
k_res_fac = 0.5
verbose = F

[IA]
file = intrinsic_alignments/tatt/tatt_interface.py
sub_lowk = F
do_galaxy_intrinsic = F
ia_model = tatt

[pk_to_cl]
file = structure/projection/project_2d.py
ell_min_logspaced = 0.1
ell_max_logspaced = 5.0e5
n_ell_logspaced = 100
shear-shear = source-source
shear-intrinsic = source-source
intrinsic-intrinsic = source-source
intrinsicb-intrinsicb = source-source
verbose = F
get_kernel_peaks = F
sig_over_dchi = 20.
shear_kernel_dchi = 10.

[add_intrinsic]
file = shear/add_intrinsic/add_intrinsic.py
shear-shear = T
position-shear = F
perbin = F

[2pt_shear]
file = shear/cl_to_xi_fullsky/cl_to_xi_interface.py
ell_max = 40000
xi_type = EB
theta_file = %(2PT_FILE)s
bin_avg = T
input_section_name = shear_cl shear_cl_bb
output_section_name = shear_xi_plus shear_xi_minus

[shear_m_bias]
file = shear/shear_bias/shear_m_bias.py
m_per_bin = True
cl_section = shear_xi_plus shear_xi_minus
cross_section = galaxy_shear_xi
verbose = F

[2pt_like]
file = likelihood/2pt/2pt_point_mass/2pt_point_mass.py
do_pm_marg = False
include_norm = True
data_file = %(2PT_FILE)s
data_sets = xip xim
make_covariance = F
covmat_name = COVMAT

%include examples/des-y3-scale-cuts.ini
"""


def run(model, run_name, start=None, tag_suffix=""):
    m = json.load(open(os.path.join(RES, f"cmp_{run_name}.json")))["minimum"]
    tag = os.path.join(OUT, f"part2_{run_name}{tag_suffix}")
    vals = tag + "_values.ini"
    if model == "pk":            # AxiCLASS fits: P(k, z) etc. from axiclass_pk.py; cosmology lines are placeholders
        open(vals, "w").write(VALUES.format(h0=m["H0"] / 100, ombh2=m["omega_b"], omch2=m["omega_cdm"],
                                            As=1e-10 * math.exp(m["logA"]), ns=m["n_s"], tau=m["tau_reio"]))
    else:
        open(vals, "w").write(VALUES.format(h0=m["H0"] / 100, ombh2=m["ombh2"], omch2=m["omch2"],
                                            As=m.get("As", 1e-10 * math.exp(m["logA"])), ns=m["ns"], tau=m["tau"]))
    if start:                                   # nuisance starting values from another run's best (same ranges, priors)
        import re
        src = re.sub(r"np\.float64\(([^)]*)\)", r"\1", open(start).read())
        own = open(vals).read().split("[shear_calibration_parameters]")[0]
        secs = re.split(r"(?m)^(?=\[)", src)
        open(vals, "w").write(own + "\n" + "".join(x for x in secs if x.strip() and not x.startswith("[cosmological_parameters]")))
    ini = tag + "_pipeline.ini"
    txt = PIPE.format(sampler=os.environ.get("S8WL_SAMPLER", "maxlike"), out=tag, values=vals,
                      module=os.path.join(HERE, "aegis_camb.py"), model=model, point=os.path.join(RES, f"cmp_{run_name}.json"))
    if model == "pk":
        txt = txt.replace("modules = consistency camb", "modules = camb")
        txt = txt.replace(f"file = {os.path.join(HERE, 'aegis_camb.py')}",
                          f"file = {os.path.join(HERE, 'load_pk.py')}\npk_file = {os.path.join(OUT, f'pk_{run_name}.npz')}")
    open(ini, "w").write(txt)
    env = dict(os.environ, AEGIS_DIR=AEGIS)
    if not os.environ.get("S8WL_REUSE") or not os.path.exists(tag + ".txt"):
        if os.path.exists(tag + ".txt"):
            os.remove(tag + ".txt")
        subprocess.run(["cosmosis", ini], cwd=CSL, env=env, check=True)
    head, row = None, None
    for line in open(tag + ".txt"):
        if head is None and line.startswith("#") and not line.startswith("##"):
            head = line.lstrip("#").split()
        elif not line.startswith("#") and line.strip():
            row = [float(x) for x in line.split()]
    d = dict(zip(head, row))
    post = [v for k, v in d.items() if k.endswith("post")][0]
    chi = [v for k, v in d.items() if "2pt_chi2" in k.lower()]
    return {"run": run_name, "best_ini": tag + "_best.ini", "chi2_WL": round(-2 * post, 3), "data_chi2": round(chi[0], 3) if chi else None,
            "S8": round(d.get("COSMOLOGICAL_PARAMETERS--SIGMA_8", float("nan")) * math.sqrt(json.load(open(os.path.join(RES, f"cmp_{run_name}.json")))["minimum"].get("omegam", float("nan")) / 0.3), 4)}


def minimise_pair(a, b):
    """Same search for both models of a pair: Nelder-Mead from the survey's fiducial start; then repeated restarts, each
    model from its own best AND from the partner's best, until neither improves by more than 0.05 in chi2_WL (max 3
    rounds). Reports every try and the minimum of each model. (Fixed 8 Nov: a single Nelder-Mead run stopped early.)"""
    from concurrent.futures import ThreadPoolExecutor
    pool = ThreadPoolExecutor(int(os.environ.get("S8WL_WORKERS", "2")))
    fa, fb = pool.submit(run, *a), pool.submit(run, *b)
    tries = {a[1]: [fa.result()], b[1]: [fb.result()]}
    for rnd in range(1, 4):
        best = {k: min(v, key=lambda r: r["chi2_WL"]) for k, v in tries.items()}
        jobs = []
        for (mod, name), other in ((a, b[1]), (b, a[1])):
            for src, lab in ((best[name], "own"), (best[other], "cross")):
                jobs.append((name, pool.submit(run, mod, name, src["best_ini"], f"_round{rnd}_{lab}")))
        improved = False
        for name, f in jobs:
            r = f.result()
            tries[name].append(r)
            improved |= r["chi2_WL"] < best[name]["chi2_WL"] - 0.05
        if not improved:
            break
    return {k: min(v, key=lambda r: r["chi2_WL"]) for k, v in tries.items()}, tries


def main():
    os.makedirs(OUT, exist_ok=True)
    want = sys.argv[1:] or list(PAIRS)
    path = os.path.join(OUT, "part2_desy3.json")
    out = json.load(open(path)) if os.path.exists(path) else {
        "rule": "PREREG_S8_WL.md Part 2", "data": "DES Y3 cosmic shear (CosmoSIS standard library, fiducial cuts)", "rows": {}}
    for lab in want:
        (mm, mr), (lm, lr) = PAIRS[lab]
        if not os.path.exists(os.path.join(RES, f"cmp_{mr}.json")):
            out["rows"][lab] = "pending (fit not found)"
            continue
        best, tries = minimise_pair((mm, mr), (lm, lr))
        a, b = best[mr], best[lr]
        d = a["chi2_WL"] - b["chi2_WL"]
        out["rows"][lab] = {"model": a, "LCDM": b, "Delta_WL": round(d, 2), "reading": "PASSES" if d <= 2 else "OVER",
                            "tries": {k: [t["chi2_WL"] for t in v] for k, v in tries.items()}}
        json.dump(out, open(path, "w"), indent=1)                     # saved after every pair
    json.dump(out, open(path, "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
