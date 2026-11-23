"""PROM-8 (PREREG_PROM8_ASH): SPARC with the POPCON composition of Creely et al. 2020 (fixed 6% He, lumped Z=8, W)."""
import io, json, os, sys, contextlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fusion as F, fusion_fast as X
with contextlib.redirect_stdout(io.StringIO()): import test_prom6 as T6, test_prom7 as T7
EA = F.two_body_split('DT')[1]
fW, fHe = 1.5e-5, 0.06; f8 = (1 - 0.85 - 2 * fHe - 74 * fW) / 8
S = dict(T6.SP); S.update(n_avg=3.1e20, P_aux=12.8, f_He=fHe, he_selfconsistent=False, f_Be=0.0, f_Ar=0.0, f_W=fW, f_O=f8,
                       extra_imp={8: f8, 74: fW}, n_ped=2.7e20, T_ped=0.39 * 7.3, n_sep=T6.I['n_sep'] / T6.I['n_avg'] * 3.1e20)
S, notes = T7.shape(S, 1.3, 2.5, 7.3)
S.update(rad_C3=1.0, rho_core=1.0, synch=False)   # PROM-8 DEV-1/2 rerun: POPCON loss-power convention, no synchrotron
def op(m):
    o = X.operating_point_fast(m, EA); return None if o is None else {k: float(o[k]) for k in ('P_fus', 'Te_avg', 'tau_E', 'Q', 'P_loss', 'P_LH', 'P_rad', 'P_synch', 'P_line', 'P_brems', 'f_He', 'Zeff', 'f_DT')}
A1 = op(S)
ash = dict(S, he_selfconsistent=True, f_He=T6.I['f_He'], extra_imp={8: f8, 74: fW}); A2 = op(ash)
A3 = float(X.plasma_fast(S, S['n_avg'], 7.3, EA)['P_fus'])
w = lambda x, t, tol: x is not None and abs(x / t - 1) <= tol
it = X.operating_point_fast(F.ITER_400, EA)
G = dict(A1=bool(A1 and w(A1['P_fus'], 140, .25) and w(A1['Te_avg'], 7.3, .20)),
         A2=bool(A1 and A2 and abs(A2['P_fus'] / A1['P_fus'] - 1) > 0.15),
         A4=bool(abs(it['P_fus'] - 389.53) < 0.5 and abs(it['tau_E'] - 3.406) < 0.005))
res = dict(goals=G, A1=A1, A2_ash_on=A2, A3_prescribed_at_7p3=A3, composition=F.composition(S), f8=f8, shape=dict(alpha_n=S['alpha_n'], alpha_T=S['alpha_T'], notes=notes),
           ITER400=dict(P_fus=float(it['P_fus']), tau_E=float(it['tau_E'])))
json.dump(res, open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'prom8_rerun.json'), 'w'), indent=1)
print(json.dumps(res, indent=1))
