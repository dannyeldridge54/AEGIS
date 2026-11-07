"""Do the two locked alpha = 1 inflation statements fit together? (audit check, 7 Nov 2026; AI-assisted, not pre-registered)
    python alpha1_inflation_squeeze.py   -> alpha1_inflation_squeeze.json

alpha-attractor (E-model) leading order: n_s = 1 - 2/N, r = 12 alpha / N^2, alpha = 1.
Locked 2 Nov 2026: r = 0.0033-0.0048 (N = 50-60); excluded if r < 0.002. Data: ACT DR6 n_s = 0.974 +- 0.003.
Question: what N does ACT's n_s need, and what r does that N give?"""
import json

NS, SIG, ALPHA, R_KILL = 0.974, 0.003, 1.0, 0.002


def ns(N):
    return 1 - 2 / N


def r(N):
    return 12 * ALPHA / N ** 2


def run():
    grid = [{"N": N, "n_s": round(ns(N), 4), "pull_sigma": round((NS - ns(N)) / SIG, 2), "r": round(r(N), 5),
             "r_excluded_by_lock": r(N) < R_KILL} for N in (50, 55, 60, 65, 70, 75, 77, 80, 90)]
    N_c, N_lo, N_hi = 2 / (1 - NS), 2 / (1 - NS + SIG), 2 / (1 - NS - SIG)
    return {
        "N_for_central_ACT_ns": round(N_c, 1),
        "N_range_1sigma": [round(N_lo, 1), round(N_hi, 1)],
        "r_at_central_N": round(r(N_c), 5),
        "r_range_1sigma": [round(r(N_hi), 5), round(r(N_lo), 5)],
        "grid": grid,
        "reading": ("Within 1 sigma of ACT's n_s, alpha = 1 needs N = 69-87 e-folds and gives r = 0.0016-0.0025, "
                    "straddling the locked kill line r < 0.002. The locked r range (N = 50-60) is the range in "
                    "2.4-4.7 sigma tension with ACT. The two locked statements pull against each other unless "
                    "reheating gives unusually many e-folds."),
    }


if __name__ == "__main__":
    out = run()
    json.dump(out, open("alpha1_inflation_squeeze.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "grid"}, indent=1))
