"""L9a (locked PREREG_L9a_eh_transfer)."""
import sys, numpy as np, camb; sys.path.insert(0, '.')
from tools.janus_lt.transfer import T_nowiggle
ks = np.logspace(-3, np.log10(0.5), 30); L = []; ok = True
for h, ob, oc in ((0.6736, 0.02237, 0.1200), (0.70, 0.0224, 0.110), (0.64, 0.0220, 0.130)):
    p = camb.CAMBparams(); p.set_cosmology(H0=100*h, ombh2=ob, omch2=oc, mnu=0.0, num_massive_neutrinos=0, nnu=3.044, TCMB=2.7255, omk=0)
    p.InitPower.set_params(ns=0.965); p.set_matter_power(redshifts=[0.0], kmax=5.0); p.WantTransfer = True
    r = camb.get_results(p); tr = r.get_matter_transfer_data(); kk = tr.transfer_data[0, :, 0]; td = tr.transfer_data[6, :, 0]  # k/h, delta_tot
    Tc = np.interp(np.log(ks), np.log(kk), td)/np.interp(np.log(1e-4), np.log(kk), td)
    d = T_nowiggle(ks, h, ob, oc)/Tc - 1; rms = np.sqrt(np.mean(d**2)); mx = np.max(np.abs(d)); good = rms <= 0.05 and mx <= 0.12; ok &= good
    L.append(f"h={h} wb={ob} wc={oc}: rms {rms:.3%}, max {mx:.3%} at k={ks[np.argmax(np.abs(d))]:.3g} h/Mpc -> {'PASS' if good else 'FAIL'}"); print(L[-1], flush=True)
L.append('EH no-wiggle transfer ' + ('VALIDATED' if ok else 'NOT VALIDATED'))
open('field_tests/results/janus_lt_l9a_eh.txt', 'w').write('\n'.join(L)+'\n'); print(L[-1])
