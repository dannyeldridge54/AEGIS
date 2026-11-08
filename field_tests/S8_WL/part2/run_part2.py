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
# The Spiral pairs of the rule need the coupled-dark-matter AxiCLASS power spectrum, which CAMB cannot make:
SPIRAL = ["Spiral, Pantheon+", "Spiral, DES-Dovekie", "Spiral, Union3"]

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


def run(model, run_name):
    m = json.load(open(os.path.join(RES, f"cmp_{run_name}.json")))["minimum"]
    tag = os.path.join(OUT, f"part2_{run_name}")
    vals = tag + "_values.ini"
    open(vals, "w").write(VALUES.format(h0=m["H0"] / 100, ombh2=m["ombh2"], omch2=m["omch2"],
                                        As=m.get("As", 1e-10 * math.exp(m["logA"])), ns=m["ns"], tau=m["tau"]))
    ini = tag + "_pipeline.ini"
    open(ini, "w").write(PIPE.format(sampler=os.environ.get("S8WL_SAMPLER", "maxlike"), out=tag, values=vals, module=os.path.join(HERE, "aegis_camb.py"), model=model,
                                     point=os.path.join(RES, f"cmp_{run_name}.json")))
    env = dict(os.environ, AEGIS_DIR=AEGIS)
    if not os.environ.get("S8WL_REUSE") or not os.path.exists(tag + ".txt"):
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
    return {"run": run_name, "chi2_WL": round(-2 * post, 3), "data_chi2": round(chi[0], 3) if chi else None,
            "S8": round(d.get("COSMOLOGICAL_PARAMETERS--SIGMA_8", float("nan")) * math.sqrt(json.load(open(os.path.join(RES, f"cmp_{run_name}.json")))["minimum"].get("omegam", float("nan")) / 0.3), 4)}


def main():
    os.makedirs(OUT, exist_ok=True)
    want = sys.argv[1:] or list(PAIRS)
    out = {"rule": "PREREG_S8_WL.md Part 2", "data": "DES Y3 cosmic shear (CosmoSIS standard library, fiducial cuts)",
           "rows": {}}
    for lab in want:
        (mm, mr), (lm, lr) = PAIRS[lab]
        if not os.path.exists(os.path.join(RES, f"cmp_{mr}.json")):
            out["rows"][lab] = "pending (fit not found)"
            continue
        a, b = run(mm, mr), run(lm, lr)
        d = a["chi2_WL"] - b["chi2_WL"]
        out["rows"][lab] = {"model": a, "LCDM": b, "Delta_WL": round(d, 2), "reading": "PASSES" if d <= 2 else "OVER"}
    for lab in SPIRAL:
        out["rows"][lab] = "NO VERDICT so far: needs the coupled-DM AxiCLASS P(k) (not CAMB); see SETUP_PART2.md"
    json.dump(out, open(os.path.join(OUT, "part2_desy3.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
