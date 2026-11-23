"""CONNECTIONS 1: which cross-ring connection can supply delta(alpha_3^-1) = -0.282 at M12 without being tuned to alpha_s."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', 'weave_cm'))
import weave_tools as W
a0 = 0.1142; need = 1 / 0.118 - 1 / a0; ReS = math.sqrt(3) / 2; P = W.weave_point({}); M12 = P['M12_GeV']
out = dict(need=need, M12_GeV=M12)
# P2: colour-triplet pair split from the doublets by a Wilson line; MSSM-like coefficient 12/5 in the alpha_s combination (Hisano-Murayama-Yanagida)
r = math.exp(need * 2 * math.pi / (12 / 5)); MT = r * M12
out['P2_triplet'] = dict(M_T_over_M12=r, M_T_GeV=MT, link='proton ring: dim-5 decay via triplets ~ M_T^2 m_sf^2 / m_gaugino; scalars 4.7e5 GeV (weave_point)',
    note='coefficient 12/5 is the MSSM value (higgsino triplets light relative to scalars?); sign: lighter triplets raise alpha_s', label='postulate, estimate')
# P3: S-T mixing normalisation with m3 != m2 (m2 = 3): kappa needed for each m3
out['P3_kappa'] = {f'm3={m3}': need / ((m3 ** 2 - 9) * ReS) for m3 in (1, 2, 4)}
out['P3_note'] = 'kappa must come from the D7 gauge kinetic function; m3 != m2 breaks alpha_1 = alpha_2 = alpha_3 at M12 and moves x = flux/alpha^-1 (T_R ring)'
# P4: spectrum thresholds (referee R104 sensitivities): gluino x1.2 -> +0.0009, scalars x0.5 -> +0.0018 in alpha_s
out['P4_spectrum'] = dict(max_natural_dalpha_s=0.0009 + 0.0018, needed=0.118 - a0, fraction_of_need=(0.0027) / (0.118 - a0),
    link='gluino/wino ratio fixed by AMSB; wino mass fixed by relic density (dark ring); scalar mass by m3/2 lever')
# P1: universal KK/string tower (complete multiplets) shifts all alpha^-1 equally -> no alpha_s change unless split; needs delta_b
out['P1_KK'] = dict(note='complete SU(5) multiplets give universal shifts (no alpha_s change); requires a split tower with delta_b3 != delta_b2: undetermined in the current model')
json.dump(out, open(os.path.join(HERE, '..', '..', 'field_tests', 'results', 'connections1.json'), 'w'), indent=1)
print(json.dumps(out, indent=1))
