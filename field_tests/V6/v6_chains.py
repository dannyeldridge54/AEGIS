"""V6 (field_tests/rules/PREREG_V6_EVIDENCE.md, locked 8 Nov): MCMC chains for Bayesian evidence.
    python v6_chains.py <run> <chain_index>        (PC, WSL env "aegis"; 4 independent chains per run)
<run>: ax_spa_spiraltwist[_dovekie|_union3]_nlfix, spiralL[_dovekie|_union3], ax_spa_lcdm_halofit[_dovekie|_union3].
Same likelihoods, priors and builds as the stored fits (each fitter's make(), unchanged); only the sampler is swapped
for Cobaya mcmc. Starting points: each parameter's ref (centred on the stored best fit by make()), random per chain.
Each chain stops at R-1 < 0.02 (Cobaya's internal test); cross-chain Gelman-Rubin over the 4 chains is computed by
v6_score.py before anything is read. Resumable: rerunning the same command continues the chain."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AEGIS = os.path.abspath(os.path.join(HERE, "..", ".."))
AX = os.path.join(AEGIS, "cmb-fit", "axiclass")
sys.path.insert(0, AX)
RULE = os.path.join(AEGIS, "field_tests", "rules", "PREREG_V6_EVIDENCE.md")


def make(run):
    if run.startswith("spiralL"):
        sys.path.insert(0, os.path.join(AX, "ula"))
        import spiral_l_fit
        info, E = spiral_l_fit.make(run)
        return info, E
    import early_late_spa as E
    E._maybe_coupled(run)
    return E.make(run), E


def main(run, i):
    assert os.path.exists(RULE + ".sha256"), "PREREG_V6_EVIDENCE.md is not locked"
    from cobaya.run import run as crun
    info, E = make(run)
    info["sampler"] = {"mcmc": {"Rminus1_stop": 0.02, "Rminus1_cl_stop": 0.2, "learn_proposal": True,
                                "max_tries": 100000, "seed": 1000 + 17 * int(i)}}
    os.makedirs(f"{E.OUT}/chains/v6", exist_ok=True)
    cov = f"{E.OUT}/chains/v6/{run}.covmat"           # V6-D1: Laplace-step covariance as the starting proposal
    tag = ""
    if os.path.exists(cov):
        info["sampler"]["mcmc"]["covmat"] = cov
        tag = "_cov"
    info["output"] = f"{E.OUT}/chains/v6/{run}{tag}_c{i}"
    info["resume"] = True
    info.pop("force", None)
    crun(info)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
