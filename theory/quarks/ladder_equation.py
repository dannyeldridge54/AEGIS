"""The Weave LADDER EQUATION — predictions from the twin slip-ladder structure (D1741).
  ε_m = c·e^{iφ}/(m + 1/16),  c = √3·0.0145 = 0.02511,  φ = 50°            (rung m, ρ side; computed to 1%, D1736/D1740)
  family on rung m:  m₂/m₃ = κ₂ ε_m,  m₁/m₃ = κ₁ ε_m²,  κ O(1)             (near-ω A4 scaling, 2212.13336)
  equal-coefficient limit (κ_u = κ_d):  g_u/g_d = (m_d + 1/16)/(m_u + 1/16),  g ≡ √((m₂/m₃)·√(m₁/m₃))
Run: prints the prediction table with Monte-Carlo errors from PDG-level mass errors (M_Z values, Q2 inputs)."""
import numpy as np
c=np.sqrt(3)*0.0145; eps=lambda m: c/(m+1/16)
rng=np.random.default_rng(2026); N=200000
def draw(v,s): return np.abs(rng.normal(v,s,N))
md,ms,mb=draw(2.80e-3,0.20e-3),draw(55.7e-3,1.3e-3),draw(2.794,0.034)
mu,mc,mt=draw(1.29e-3,0.20e-3),draw(0.629,0.012),draw(169.0,1.1)
g=lambda a,b,cc: np.sqrt((b/cc)*np.sqrt(a/cc))
gd,gu=g(md,ms,mb),g(mu,mc,mt)
mstar=(1+1/16)*gd/gu-1/16
print(f"P1 rung offsets: " + ", ".join(f"m={m}:{eps(m):.5f}" for m in (1,2,4,8,13,16,32)) + "  (arg 50°)")
print(f"P2 measured up rung (equal-coefficient limit): m_u* = {np.median(mstar):.2f} ± {mstar.std():.2f}; P(m_u*∈[7.5,8.5]) = {np.mean((mstar>7.5)&(mstar<8.5)):.2f}, P(∈[8.5,9.5]) = {np.mean((mstar>8.5)&(mstar<9.5)):.2f}")
for m in (8,9):
    pred=(1+1/16)/(m+1/16); print(f"   rung {m}: predicted g_u/g_d = {pred:.4f}; measured {np.median(gu/gd):.4f} ± {(gu/gd).std():.4f}")
need=lambda target: (0.1318-0.1172)/2/target
print(f"P3 precision needed to tell rung 8 from 9 at 3σ: σ(g_u/g_d) ≲ {(0.1318-0.1172)/3:.4f} (now {(gu/gd).std():.4f})")
print("P4 hidden family on rung m must have m₂/m₃ ∈ [ε_m/3, 3ε_m]: " + ", ".join(f"m={m}:[{eps(m)/3:.1e},{3*eps(m):.1e}]" for m in (11,16,26,64)))
