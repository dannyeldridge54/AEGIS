"""Chronos branches (D2189 A2): per-person goalposts on the same decay engine."""
import math, json
from chronos import LAM, D, Y, MSUN, sn_luminosity

G, C = 6.674e-8, 2.998e10   # cgs

# Baron: Ni-56 mass from tail luminosity (inverse of the A1 model; linear in M_Ni)
def ni_mass_from_tail(L, t, t0_days):
    """t0_days REQUIRED (DEV-10): gamma trapping timescale; None = full trapping (Type II-P / full-trapping only)."""
    return L / sn_luminosity(t, 1.0, t0_days)

# Dai: Arnett rule, full trapping at peak
def ni_mass_arnett(L_peak, t_rise):
    return L_peak / sn_luminosity(t_rise, 1.0, None)

# Kilic: double white dwarf GW merger clock (Peters 1964, circular)
def dwd_merger_time(P_s, m1, m2):
    M1, M2 = m1 * MSUN, m2 * MSUN; Mt = M1 + M2
    a = (G * Mt * P_s ** 2 / (4 * math.pi ** 2)) ** (1 / 3)
    return 5 / 256 * C ** 5 * a ** 4 / (G ** 3 * M1 * M2 * Mt)

def dwd_gw_freq(P_s): return 2.0 / P_s

# Awasthi: cyclotron production planner (user-supplied saturation activity, no cross sections)
def eob_activity(nuc, A_sat, t_irr):
    return A_sat * (1 - math.exp(-LAM[nuc] * t_irr))

def delivered(nuc, A_sat, t_irr, t_after):
    return eob_activity(nuc, A_sat, t_irr) * math.exp(-LAM[nuc] * t_after)

if __name__ == '__main__':
    R = {}
    w = 0.0
    for t0 in (None, 40.0):
        for d in range(50, 401, 25):
            t = d * D; L = sn_luminosity(t, 0.07, t0); m = ni_mass_from_tail(L, t, t0); w = max(w, abs(m / 0.07 - 1))
    R['T7'] = dict(worst_rel=w, pass_=bool(w < 1e-12))
    R['T8_report'] = dict(L_peak=9.42e42, t_rise_d=13, M_Ni_Msun=ni_mass_arnett(9.42e42, 13 * D),
                          context='GRB-SNe typically 0.1-0.5 Msun in the literature; mean-peak value only')
    tm = dwd_merger_time(765.0, 0.26, 0.50) / Y / 1e6
    R['T9'] = dict(note='masses 0.26/0.50 Msun from Hermes et al. 2012; Peters point-mass coalescence = upper bound (Brown et al. 2011: ~0.9 Myr to contact)', J0651_merger_Myr=tm, f_gw_mHz=dwd_gw_freq(765.0) * 1e3, pass_=bool(0.7 <= tm <= 1.2))
    f = eob_activity('F-18', 1.0, 2 * math.log(2) / LAM['F-18']); R['T10'] = dict(frac=f, pass_=bool(abs(f - 0.75) < 1e-12))
    # executed goalposts (illustrative numbers, clearly labelled)
    R['example_Awasthi_F18_day'] = dict(A_sat_GBq=300, t_irr_min=90, EOB_GBq=eob_activity('F-18', 300, 90 * 60),
                                        after_synthesis_qc_transport_100min_GBq=delivered('F-18', 300, 90 * 60, 100 * 60))
    R['example_Kilic_ELM_P_minutes'] = {str(p): dwd_merger_time(p * 60, 0.2, 0.7) / Y / 1e6 for p in (12.75, 20, 40, 60)}
    R['example_tail_Msun_per_1e41_at_200d'] = dict(full_trapping_TypeIIP=ni_mass_from_tail(1e41, 200 * D, None),
                                                    SN_Ia_t0_40d=ni_mass_from_tail(1e41, 200 * D, 40.0))
    json.dump(R, open('d2189_branches.json', 'w'), indent=1); print(json.dumps(R, indent=1))
