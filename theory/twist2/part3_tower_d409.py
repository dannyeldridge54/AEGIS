"""D409 (locked PREREG_D409_PART3): Part 3 (kination/reheating) — KK and string towers vs T and H along the D367 trajectory. AI-assisted.
Volume reading: Re T = x ~ 4-cycle volume τ, 𝒱 ~ x^{3/2}; m_KK ~ M_P/𝒱^{2/3} = M_P/x, M_s ~ M_P/𝒱^{1/2} = M_P x^{-3/4} (O(1) and g_s factors set to 1)."""
import math
MP, gs = 2.435e18, 106.75
lines = [(0.5, 2.660e14, 0.025), (1.0, 1.613e14, 0.066), (2.0, 5.936e13, 0.480), (3.0, 2.186e13, 3.091), (4.0, 8.170e12, 12.653),
         (5.0, 3.524e12, 22.826), (6.0, 1.714e12, 27.178), (8.0, 2.391e11, 29.452), (11.0, 1.191e10, 29.806)]   # (N−Ne, T, x) D367
print("N−Ne   T[GeV]     x        m_KK[GeV]   M_s[GeV]    H_rad[GeV]  m_KK/T     M_s/T")
for N, T, x in lines:
    mkk, ms = MP / x, MP * x ** -0.75; H = math.sqrt(math.pi**2 * gs / 90) * T * T / MP
    print(f"{N:4.1f}  {T:.3e}  {x:7.3f}  {mkk:.3e}  {ms:.3e}  {H:.3e}   {mkk/T:.2e}  {ms/T:.2e}")
