"""D116: rough size of the field-dependent vacuum energy on the tail. AI-assisted, order of magnitude only.
chi's mass depends on the inflaton (preheating, m_chi = g|phi - phi0|). chi and its partner chi~ are a SUSY pair, so their
loops cancel except for the splitting. The Planck-suppressed links that let chi decay into the (non-SUSY) Standard Model (D110)
split them by dm^2 ~ L^4/(16 pi^2 M_P^2) for SM loop momenta up to L. Coleman-Weinberg: dV(phi) ~ m_chi(phi)^2 dm^2/(16 pi^2)."""
import math
MP = 2.435e18; rho_de = 2.5e-47
print(f"today's dark energy {rho_de:.1e} GeV^4")
for L in (1e3, 1e10, 0.05 * MP):
    dm2 = L ** 4 / (16 * math.pi ** 2 * MP ** 2)
    for mchi in (0.05 * MP, 0.5 * MP):
        dV = mchi ** 2 * dm2 / (16 * math.pi ** 2)
        need = math.log(dV / rho_de)
        print(f"  SM loops to {L:.0e} GeV, m_chi(tail) {mchi:.1e} GeV: field-dependent dV ~ {dV:.0e} GeV^4 = {dV/rho_de:.0e} x rho_DE;"
              f" an e^(-pi x/4) switch-off needs x >~ {4*need/math.pi:.0f}")
