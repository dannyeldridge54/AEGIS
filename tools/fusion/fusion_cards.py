"""CM-CARDS: open-book formula cards for CubeMind's fusion/element derivations. Each card holds exactly the formula, constants and
units the engine uses (fusion.py), so a derivation is graded on method and arithmetic, not on recalling fit coefficients."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fusion as F

def _bh(r):
    p = F.BH[r]; C = p['C']
    return (f"{r}: BG={p['BG']} keV^1/2, mrc2={p['mrc2']} keV, C1..C7={C}")

CONST = (f"Constants: 1 MeV = {F.MEV_J} J; 1 keV = {F.KEV_J} J; 1 u = {F.U_MEV} MeV; N_A = {F.NA}; year = {F.YEAR} s; "
         f"alpha = {F.ALPHA_FS}; k_B = {F.K_B_KEV} keV/K; 1 Gbar = 1e14 Pa. Atomic masses (u, AME2020): {F.M}.")

CARDS = {
 'fusion_sigmav': "Bosch-Hale (1992) reactivity, T in keV, result in cm^3/s:\n"
   "theta = T / (1 - T*(C2 + T*(C4 + T*C6)) / (1 + T*(C3 + T*(C5 + T*C7))))\n"
   "xi = (BG**2 / (4*theta))**(1/3)\n"
   "sigmav = C1 * theta * sqrt(xi / (mrc2 * T**3)) * exp(-3*xi)\n"
   "Coefficients:\n" + '\n'.join(_bh(r) for r in F.BH) +
   "\nCheck value: DT at 10 keV -> 1.136e-16 cm^3/s.",
 'fusion_q_value': "Q = (sum of reactant atomic masses - sum of product atomic masses) * 931.49410242 MeV/u.\n"
   "Reactions: DT: D + T -> He4 + n; DDn: D + D -> He3 + n; DDp: D + D -> T + H1; DHe3: D + He3 -> He4 + H1.\n" + CONST,
 'fusion_ignition': "Ideal ignition with the alpha share of DT (E_alpha = 3.5609 MeV, relativistic split of 17.5893 MeV):\n"
   "n T tau_E = 12 T^2 / (E_alpha <sv>(T) - 4*5.35e-37*sqrt(T)) in keV s m^-3 with <sv> in m^3/s (use the Bosch-Hale card, x1e-6),\n"
   "E_alpha in keV-J consistently (E_alpha[J]/keV[J] in keV). Minimise over T; minimum is near 14 keV.",
 'fusion_tritium_burn': "Reactions per second per GW = 1e9 / (Q_DT * 1.602176634e-13), Q_DT = 17.5893 MeV.\n"
   "kg per full-power year = rate * P_GW * 31557600 * molar / 6.02214076e23 / 1000, molar(T) = 3.01604928 g/mol,\n"
   "molar(D) = 2.01410178, molar(Li6) = 6.01512289. Check: T at 1 GW -> 56.08 kg/y.",
 'fusion_tbr': "Constant burn b = 56.08 * P_GW kg/y; lambda = ln2 / 12.32 y; e = exp(-lambda * t_d).\n"
   "TBR = 1 + lambda * I0 * (2 - e) / (b * (1 - e))   (I0 = inventory_kg, t_d = doubling_years). Check: P=1, I0=10, t_d=5 -> 1.051.",
 'fusion_burn_fraction': "Phi = rhoR / (rhoR + 6.0), rhoR in g/cm^2.",
 'fusion_gamow': "kT = k_B * T_K (k_B = 8.617333262e-08 keV/K) or kT_keV given;\n"
   "b = pi * alpha * Z1 * Z2 * sqrt(2 * mu_u * 931.49410242 * 1000)  (keV^1/2), alpha = 0.0072973525693;\n"
   "E0 = (b * kT / 2)**(2/3) keV; width = 4 * sqrt(E0 * kT / 3).",
 'fusion_nif_pressure': "Y_n = Y_MJ*1e6 / (17.5893 * 1.602176634e-13); <sv> from the Bosch-Hale card at T_keV, x1e-6 -> m^3/s;\n"
   "n_i = 2 * sqrt(Y_n / (<sv> * V_um3*1e-18 * tau_ps*1e-12)) m^-3;  p = 2 * n_i * T_keV * 1.602176634e-16 Pa; Gbar = p / 1e14.\n"
   "Check: Y 1.37 MJ, 10.9 keV, 89 ps, 6.4e5 um^3 -> about 545 Gbar.",
 'fusion_plant': f"share_n = 14.0284/17.5893 = {F.two_body_split('DT')[0] / F.q_value('DT'):.6f}; P_n = share_n*P_fus; P_alpha = P_fus - P_n;\n"
   f"M = {F.M_demoA():.6f}; P0 = M*P_n + P_alpha + P_aux; P_pump = (14/2058)*P0; P_th = P0 + P_pump; P_gross = 0.368*P_th;\n"
   "P_recirc = P_aux/eta_wp + P_pump + 100; P_net = P_gross - P_recirc (MW). Defaults eta_wp = 0.4.",
 'nuclide_lookup': "A lookup in NUBASE2020: read the element card for that element (all its nuclides, half-lives in seconds, decay modes).\n"
   "1 year = 31557600 s (Julian). Check: H-3 12.32 y = 3.888e8 s.",
 'element_cooling': "Coronal balance from OPEN-ADAS ADF11: charge-state fractions f_z from ionisation SCD and recombination ACD; mean charge =\n"
   "sum z f_z. Rules of thumb: at 1 keV argon is near its He-like/H-like shells (mean charge ~16); light elements (Be, C, N, O, Ne)\n"
   "are fully stripped above ~0.5 keV. Read the element card's ADAS cooling block for tabulated points.",
}
CARDS['nuclide_binding'] = ("Binding energy per nucleon from the AME2020 mass excess ME (keV) of nuclide (Z, N, A):\n"
   "BE/A [MeV] = (Z*7288.971064 + N*8071.318062 - ME) / A / 1000   (7288.971 keV = ME of 1H, 8071.318 keV = ME of the neutron).\n"
   "The element card below lists ME for each nuclide; N = A - Z.")
CARDS['element_property'] = "Read the value from the element card below (sources: mendeleev, NUBASE2020/AME2020, OPEN-ADAS)."
CARDS['element_card'] = CARDS['element_property']
FUSION_TOOLS = set(CARDS) | {'fusion_operating_point'}

def element_context(args):
    """Element card text for tasks that name an element or nuclide (nuclide_lookup, nuclide_binding, element_*), incl. ME rows."""
    try:
        import fusion_cm as FC, element_cards as E
        nm = args.get('element') or str(args.get('name', '')).split('-')[0]
        if not nm: return ''
        c = FC._cards()[FC._sym(nm)]; txt = E.summary(c, 8)
        if 'name' in args:
            A = int(str(args['name']).split('-')[1].rstrip('m'))
            r = [x for x in c['nuclides'] if x['A'] == A and x['isomer'] == 0]
            if r: txt += f" ROW {r[0]['name']}: Z={c['Z']}, N={r[0]['N']}, A={A}, mass excess {r[0]['mass_excess_keV']} keV, half-life {r[0]['half_life_s']} s."
        return '\n' + txt
    except Exception:
        return ''

def card(tool, args=None):
    return (CARDS.get(tool, 'No closed-form card: estimate and state your method.') + '\n' + CONST +
            (element_context(args) if args and tool in ('nuclide_lookup', 'nuclide_binding', 'element_property', 'element_card', 'element_cooling') else ''))
