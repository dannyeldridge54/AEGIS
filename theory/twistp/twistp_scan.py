"""TWIST-P: the n_s-r curve vs beta, with the two stability limits at the CMB point: angle mass m_y^2/H^2 = 8/(1 + beta/(3x*))
(the kinetic metric grows, the angle's potential curvature does not) — heavy needs > 9/4; S mass from the full SUGRA potential. AI-assisted."""
import sys, numpy as np, mpmath as mp
import twistp_inflation as TP, twistp_sugra_check as SC
sys.path.insert(0, "/home/claude/aegis/theory/inflation"); import s_mass_d127 as SM
for beta in np.logspace(-4, -1, 10):
    o = TP.obs(beta, 1.2); x = o["xstar"]; my = 8 / (1 + beta / (3 * x))
    K = SC.Kp(mp.mpf(beta)); X = mp.mpf(x); s = mp.mpf("1e-7")
    v0, kss = SM.V(K, SC.W, X, mp.mpf(0)); vp, _ = SM.V(K, SC.W, X, s); vm, _ = SM.V(K, SC.W, X, -s)
    ms = float((vp - 2 * v0 + vm) / (s * s) / (2 * kss) / (v0 / 3))
    print(f"beta {beta:.2e}: n_s {o['ns']:.4f}, r {o['r']:.2e}, x* {x:.2e}; m_y^2/H^2 {my:.2f} ({'heavy' if my > 2.25 else 'LIGHT'}), "
          f"m_S^2/H^2 {ms:.1f} ({'ok' if ms > 2.25 else 'FAIL'})", flush=True)
