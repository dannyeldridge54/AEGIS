# AEGIS-FP YNAYXXCLYQJXQNON · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Hyperion BBN network (B6): LINX (pip linx-bbn; Giovanetti, Lisanti, Liu, Mishra-Sharma, Ruderman) as primary engine.
Referees: PRIMAT 2021 table (bbn.py) and PRyMordial (external clone, D1104/D1107). Explicit helium conventions (lesson D1082a):
Yp_mass = helium MASS fraction; Yp_BBN = nucleon fraction 4 n_He4/n_b. dNeff_init is LINX's INITIAL Delta N_eff (D1109: 0.3 initial -> 0.078 final; solve for the init value to hit a target final N_eff)."""
_cache = {}
M_HE4, M_H1 = 4.0026032541, 1.00782503223      # atomic masses as quoted in the PRIMAT table header
def abundances(ombh2=0.02242, dNeff_init=0.0, tau_n_fac=1.0, net='key_PRIMAT_2023'):
    from jax import numpy as jnp
    from linx.background import BackgroundModel
    from linx.nuclear import NuclearRates
    from linx.abundances import AbundanceModel
    import linx.const as C
    if net not in _cache: _cache[net] = AbundanceModel(NuclearRates(nuclear_net=net))
    t, a, rg, rn, rNP, pNP, Neff = BackgroundModel()(jnp.asarray(float(dNeff_init)))
    sol = _cache[net](rg, rn, rNP, pNP, t_vec=t, a_vec=a, eta_fac=jnp.asarray(ombh2/C.Omegabh2),
                      tau_n_fac=jnp.asarray(float(tau_n_fac)), nuclear_rates_q=jnp.zeros(12))
    sp = _cache[net].species_dict; d = {sp[i]: float(x) for i, x in enumerate(sol)}
    Ya = d['a']
    return dict(Yp_mass=Ya*M_HE4/(Ya*M_HE4 + (1 - 4*Ya)*M_H1), Yp_BBN=4*Ya, DH=d['d']/d['p'], He3H=d['He3']/d['p'],
                Li7H=(d.get('Li7', 0.0) + d.get('Be7', 0.0))/d['p'], Neff_final=float(Neff[-1]))
