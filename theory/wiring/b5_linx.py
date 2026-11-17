import sys, time; sys.path.insert(0, '.')
from jax import numpy as jnp
from linx.background import BackgroundModel
from linx.nuclear import NuclearRates
from linx.abundances import AbundanceModel
import linx.const as C
t0 = time.time()
bkg = BackgroundModel(); t_vec, a_vec, rg, rn, rNP, pNP, Neff = bkg(jnp.asarray(0.))
abd = AbundanceModel(NuclearRates(nuclear_net='key_PRIMAT_2023'))
sol = abd(rg, rn, rNP, pNP, t_vec=t_vec, a_vec=a_vec, eta_fac=jnp.asarray(1.), tau_n_fac=jnp.asarray(1.), nuclear_rates_q=jnp.zeros(12))
Y = [float(x) for x in sol]; sp = abd.species_dict
d = {sp[i]: Y[i] for i in range(len(Y))}
mHe4, mH1 = 4.0026032541, 1.00782503223           # atomic masses as quoted in the PRIMAT table header (D1082)
Ya = d['a']; Yp_mass = Ya*mHe4/(Ya*mHe4 + (1 - 4*Ya)*mH1); YpBBN = 4*Ya
DH = d['d']/d['p']; He3 = d['He3']/d['p']; Li = (d.get('Li7', 0) + d.get('Be7', 0))/d['p']
out = [f"LINX key_PRIMAT_2023, Obh2={C.Omegabh2}, Neff_final={float(Neff[-1]):.4f}, run {time.time()-t0:.0f}s",
       f"Yp(mass)={Yp_mass:.5f} Yp^BBN={YpBBN:.5f} 1e5 D/H={DH*1e5:.4f} 1e5 He3/H={He3*1e5:.4f} 1e10 Li7/H={Li*1e10:.4f}"]
x1 = abs(Yp_mass-0.24721) <= 0.002 and abs(DH*1e5/2.4393-1) <= 0.02
out.append(f"X1 vs PRIMAT table: dYp={Yp_mass-0.24721:+.5f}, dDH={DH*1e5/2.4393-1:+.4f} -> {'CONSISTENT' if x1 else 'NOT'}")
out.append(f"X2 Li7 {Li*1e10:.3f} vs PRyMordial 5.497 (at 0.02230) and quoted 4.94+-0.72 ({(Li*1e10-4.94)/0.72:+.2f} sigma)")
out.append(f"X3 Yp vs PRyMordial 0.24555: {Yp_mass-0.24555:+.5f}")
open('field_tests/results/b5_linx.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
