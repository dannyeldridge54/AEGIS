"""FLAG-1 posterior (MCMC) for error bars. Reported, not a verdict: PREREG_FLAGSHIP.md lists beta_eff, S8, H0 as
reported quantities; this adds their uncertainties. Same setup as the stored fit (early_late_spa.make + DES Y6 S8 term,
same data, priors, build); only the sampler differs. Pantheon+ set. Each chain is its own process (no MPI on the PC);
chains start at the FLAG-1 best fit (ref widths as in the fit) and learn their proposal.
    python flag_mcmc.py <chain index 1..4>   -> results/chains/FLAG1_mcmc_c<i>.*"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); AX = os.path.dirname(HERE)
AEGIS = os.path.abspath(os.path.join(AX, "..", ".."))
sys.path.insert(0, AX); sys.path.insert(0, os.path.join(AEGIS, "field_tests", "S8_WL", "joint"))
import early_late_spa as E
import s8_joint_fit as J
from cobaya.run import run

BASE = "ax_spa_spiraltwist_kappa1_nlfix"
i = int(sys.argv[1])
E._maybe_coupled(BASE)
info = E.make(BASE)
J.add_s8(info)
best = json.load(open(f"{E.OUT}/cmp_{BASE}_s8y6.json"))["minimum"]
for k, v in info["params"].items():
    if isinstance(v, dict) and "ref" in v and k in best:
        v["ref"]["loc"] = float(best[k])
info["sampler"] = {"mcmc": {"learn_proposal": True, "Rminus1_stop": 0.02, "Rminus1_cl_stop": 0.2,
                            "max_samples": 40000, "max_tries": 10000, "burn_in": 0, "seed": 1000 + i,
                            "measure_speeds": False}}
info["output"] = f"{E.OUT}/chains/FLAG1_mcmc_c{i}"
info["resume"] = True
info.pop("force", None)
run(info)
