# AEGIS-FP WB36CRHE7HP5IAGV · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""All levels linked: model -> potential -> vacuum -> background -> exact spectra -> N* (self-consistent with reheating)
-> observables -> consistency relation -> distance to data.

Usage (repo root):  python3 -m tools.serapis_calc.pipeline --model serapis_e --C 1.15e-6 --TR 1e7
In code:            from tools.serapis_calc.pipeline import predict; predict('serapis_e', C=1.15e-6, TR=1e7)
"""
import math, argparse, numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
from .eisenstein import E_paper
from .ms import Background, spectra
from .nstar import Nstar
from . import relation, data
SQ2 = math.sqrt(2)
MODELS = {
  # name: (path Re tau, kinetic n, plateau exponent p, ramp kappa for the relation)
  'serapis_e': dict(x=0.5, n=1, p=2*SQ2, kappa=1.0),
}
_EGRID = {}
def _egrid(model, lam, ymax, npts):
    """The E(tau,2) grid along the inflaton line does NOT depend on C: compute it once and cache it (memory + disk).
    Speed pass 2026-11-18: this was 9.4 s of every serapis_point/spectra/ms call. Same numbers bit-for-bit (cache keyed on the
    Eisenstein source, so any change to eisenstein.py invalidates it)."""
    import hashlib, os, pathlib
    m = MODELS[model]; x = m['x']; n = m['n']
    src = pathlib.Path(__file__).with_name('eisenstein.py').read_bytes()
    key = hashlib.md5(repr((model, x, n, float(lam), float(ymax), int(npts))).encode() + src).hexdigest()[:16]
    if key in _EGRID: return _EGRID[key]
    cdir = pathlib.Path(os.environ.get('AEGIS_CACHE', pathlib.Path.home() / '.cache' / 'aegis')); f = cdir / f'egrid_{key}.npz'
    try:
        z = np.load(f); out = (z['ph'], z['E']); _EGRID[key] = out; return out
    except Exception:
        pass
    yv = 3**0.5/2 if x == 0.5 else 1.0
    Er = E_paper(x, yv)
    ph = np.linspace(math.log(yv)*math.sqrt(n/2)+1e-4, math.log(ymax)*math.sqrt(n/2), npts)
    E = np.maximum(lam*np.array([E_paper(x, math.exp(p/math.sqrt(n/2)))-Er for p in ph]), 1e-14)
    try:
        cdir.mkdir(parents=True, exist_ok=True); np.savez(f, ph=ph, E=E)
    except Exception:
        pass
    _EGRID[key] = (ph, E); return ph, E
def build(model='serapis_e', C=1.15e-6, lam=1.0, ymax=3000, npts=4000):
    m = MODELS[model]
    ph, E = _egrid(model, lam, ymax, npts)
    S = CubicSpline(ph, E); dS = S.derivative()
    V = lambda p: (lambda e: e/(e+1)*(1+C*e/lam))(float(S(p)))
    dV = lambda p: (lambda e, de: de*((1+C*e/lam)/(e+1)**2 + (C/lam)*e/(e+1)))(float(S(p)), float(dS(p)))
    p0 = ph[np.searchsorted(E, 600*lam)]
    return m, V, dV, p0
def predict(model='serapis_e', C=1.15e-6, TR=1e7, lam=1.0, tol=0.02000000848925, verbose=False):
    m, V, dV, p0 = build(model, C, lam)
    bg = Background(V, dV, p0)
    # V*/V_end needs phi at N*: from the background
    N = 49.0
    for it in range(20):
        res = spectra(bg, N)
        phis = bg.sol.sol(bg.Nend - N)[0]; phie = bg.sol.sol(bg.Nend)[0]
        Nn = Nstar(res['r'], V(phis)/V(phie), TR)
        if verbose: print(f'iter {it}: N*={N:.3f} -> {Nn:.3f}  n_s={res["ns"]:.5f} r={res["r"]:.3e}')
        if abs(Nn-N) < tol: N = Nn; break
        N = Nn
    res = spectra(bg, N)
    rel = relation.alpha_s(res['ns'], res['r'], m['p'], m['kappa'])
    return dict(model=model, C=C, TR=TR, Nstar=N, ns=res['ns'], r=res['r'], alpha_s=res['alpha_s'],
                alpha_s_relation=rel, sigma=data.sigma(res['ns']), Ntotal=bg.Nend)
def predict_fast(model='serapis_e', C=1.15e-6, TR=1e7, lam=1.0, g=106.75):
    """U2 (PREREG_U2_pipeline_fast): self-consistent N* with Janus core (third-order flow) and the exact-end V*/V_end, then ONE compiled
    ripple-free exact Mukhanov-Sasaki spectrum (U1b, D1255) at that N*. Same keys as predict."""
    from tools.janus_calc.core import Model, spectra3
    from .ms_jit import build_spline, spectra_msjit
    m, V, dV, p0 = build(model, C, lam); M = Model(V, dV, p0, Nmax=4000); Ve = V(M.sol.sol(M.Nend)[0]); N = 50.0
    for _ in range(40):
        a = spectra3(M, N); N2 = Nstar(a['r'], V(M.sol.sol(M.Nend - N)[0])/Ve, TR, g=g)
        if abs(N2 - N) < 1e-4: N = N2; break
        N = N2
    mj, q0 = build_spline(model, C, lam); res = spectra_msjit(mj, q0, N, dlnk=tuple(np.linspace(-0.1, 0.1, 9)), bd=4000.0)
    rel = relation.alpha_s(res['ns'], res['r'], m['p'], m['kappa'])
    return dict(model=model, C=C, TR=TR, Nstar=N, ns=res['ns'], r=res['r'], alpha_s=res['alpha_s'], alpha_s_relation=rel,
                sigma=data.sigma(res['ns']), Ntotal=M.Nend, engine='predict_fast (U2): Janus N* + compiled exact MS')
if __name__ == '__main__':
    a = argparse.ArgumentParser(); a.add_argument('--model', default='serapis_e'); a.add_argument('--C', type=float, default=1.15e-6)
    a.add_argument('--TR', type=float, default=1e7); a.add_argument('--lam', type=float, default=1.0); a.add_argument('-v', action='store_true')
    g = a.parse_args(); out = predict(g.model, g.C, g.TR, g.lam, verbose=g.v)
    for k, v in out.items(): print(f'{k:>18}: {v}')
