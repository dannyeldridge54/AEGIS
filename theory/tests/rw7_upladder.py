"""RW7 — PREREG_RW7_UPLADDER. AI-assisted. Run from the repo root."""
import json, math
hbarc, MP = 1.9733e-16, 2.435e18
W = dict(H_inf=5.8e12, M_N=4.5e10, T_R=3.74e8, scalars=4.7e5, m32=2.5e5)
rows = []
for Rum in (1, 2, 5, 7.4, 10):
    R = Rum * 1e-6 / hbarc  # GeV^-1
    mKK = 1 / R
    Lsp = mKK ** (1 / 3) * MP ** (2 / 3)
    Lsp2 = (mKK / (2 * math.pi)) ** (1 / 3) * MP ** (2 / 3)
    X = (W['T_R'] * R) * W['T_R'] / MP
    r = dict(R_um=Rum, mKK_eV=mKK * 1e9, Lambda_sp=Lsp, Lambda_sp_2pi=Lsp2, X_KK=X)
    for k, v in W.items():
        r[f'{k}_over_Lsp'] = v / Lsp
    r['C1'] = W['H_inf'] < Lsp; r['C2'] = W['M_N'] < Lsp; r['C3'] = W['T_R'] < Lsp
    r['C4'] = W['scalars'] < Lsp; r['C5'] = W['m32'] < Lsp; r['C6'] = X < 1
    rows.append(r)
hard = any(all(not r[c] for r in rows) for c in ('C1', 'C2', 'C6'))
cons = any(all(r[c] for c in ('C1', 'C2', 'C3', 'C4', 'C5', 'C6')) for r in rows)
out = dict(rows=rows, verdict='HARD CONFLICT' if hard else ('CONSISTENT' if cons else 'TENSION'))
print(json.dumps(out, indent=1))
json.dump(out, open('field_tests/results/rw7_upladder.json', 'w'), indent=1)
