"""D289: sharpen D272's alpha drift if MSSM superpartner masses slide as m_soft ∝ x^{-3/2} (eV-gravitino reading, no shield).
QED one-loop: Δb = (4/3)ΣQ² (Dirac fermions) + (1/3)ΣQ² (complex scalars) for superpartners; Δ(1/α) = (Δb/2π) Δln m_soft. AI-assisted."""
import math
a = 1 / 137.036
squarks = 3 * (2 * (2/3) ** 2 + 2 * (1/3) ** 2) * 3; sleptons = 2 * 1 * 3; Hpm = 1
b_scal = (squarks + sleptons + Hpm) / 3; b_ferm = (4/3) * 2      # 2 charginos
db = b_scal + b_ferm
dlnm = 1.5 * math.log(89 / 73)
print(f"Δb = {db:.2f}; Δln m (BBN->today) = {dlnm:.3f}; Δ(1/α) = {db/(2*math.pi)*dlnm:.3f}; Δα/α = {a*db/(2*math.pi)*dlnm:.2e}")
H0 = 67.4 / 3.0857e19 * 3.156e7          # 1/yr
rate_lnx = math.sqrt(2/3) * 0.45 * H0    # phidot ≈ 0.45 H0 M_P today (w0 ≈ -0.9)
dadt = a * db / (2*math.pi) * 1.5 * rate_lnx
print(f"today: dln x/dt = {rate_lnx:.2e}/yr -> dlnα/dt = {dadt:.1e}/yr (clock bound ~1e-18/yr: ratio {dadt/1e-18:.0e})")
