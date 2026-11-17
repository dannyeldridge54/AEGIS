"""D989 (locked PREREG_D989): Janus String Calculator vs base toolkit."""
import sys, time, math, numpy as np, warnings; sys.path.insert(0, '.'); warnings.filterwarnings('ignore')
from tools.janus_calc import models as J, core
from tools.serapis_calc.ms import Background, spectra
W = tuple(np.round(np.linspace(-0.8, 0.8, 9), 10))
cases = [('SERAPIS-E C=1.0e-6', lambda: J.serapis_E(1.0e-6), (48.4, 50.0)), ('SERAPIS-E C=1.15e-6', lambda: J.serapis_E(1.15e-6), (48.4,)),
         ('Chronos eps=1.3e-4', lambda: J.chronos(1.3e-4), (46.0, 49.0)), ('SERAPIS-rho eps=6e-5', lambda: J.serapis_rho(6e-5), (46.09, 49.49)),
         ('Kairos eps=0', lambda: J.chronos(0.0), (46.08,))]
L = []; npass = 0; ntot = 0
for name, mk, Nlist in cases:
    m = mk(); bg = Background(m.V, m.dV, m.sol.y[0][0])          # same potential and start for the base solver
    for Ns in Nlist:
        t = time.time(); jf = m.spectra(Ns); ja = core.alpha_dn(m, Ns); tj = time.time() - t
        t = time.time(); b = spectra(bg, Ns, dlnk=W, bd=1000.0, ic='ds'); tb = time.time() - t
        dn = jf['ns'] - b['ns']; dr = jf['r']/b['r'] - 1; da = ja/b['alpha_s'] - 1
        ok = abs(dn) <= 1e-4 and abs(dr) <= 0.005 and abs(da) <= 0.02; npass += ok; ntot += 1
        L.append(f"{name} N*={Ns}: base ns={b['ns']:.6f} r={b['r']:.5e} a={b['alpha_s']:.5e} ({tb:.0f}s) | janus ns={jf['ns']:.6f} r={jf['r']:.5e} "
                 f"a_dn={ja:.5e} a_flow={jf['alpha_s']:.5e} ({tj*1000:.1f} ms) | dns={dn:+.1e} dr={dr:+.2%} da={da:+.2%} -> {'PASS' if ok else 'FAIL'}")
        print(L[-1], flush=True)
v = 'VALIDATED' if npass == ntot else ('PARTIAL' if npass >= 6 else 'NOT VALIDATED')
L.append(f"{npass}/{ntot} points pass -> {v}")
open('field_tests/results/janus_validate_d989.txt', 'w').write('\n'.join(L)+'\n'); print(L[-1])
