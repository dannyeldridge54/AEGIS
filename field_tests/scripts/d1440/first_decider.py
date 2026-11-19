import json
d37=json.load(open('field_tests/results/D1437_ns_sensitivity.json')) if __import__('os').path.exists('field_tests/results/D1437_ns_sensitivity.json') else None
import glob; d37=json.load(open(glob.glob('field_tests/results/D1437_*.json')[0]))
rlo,rhi=4.55e-4,5.7e-4
out={'r_official_dr1e-3':{'S_lo':rlo/1e-3,'S_hi':rhi/1e-3},'r_idealized_2212':{'S_lo':rlo/(0.98e-4/1.96),'S_hi':rhi/(0.98e-4/1.645)}}
real={'SO':'operating','SO+DESI':'~2026-27','SO+SPHEREx':'~2027+ (SPHEREx 2-yr survey from Mar 2025)','LiteBIRD+CHIME+SPHEREx':'>=2035','LiteBIRD+S4(l>200)':'HYPOTHETICAL (S4 cancelled)'}
out['ns']={k:{'when':real.get(k,'HYPOTHETICAL (S4 cancelled)'),'sigma':min(v.values()),'counted':('S4' not in k)} for k,v in d37['tension'].items()}
out['alpha_s']={'detection_max_sigma':1.3,'exclusion_SO_if_ACT_central':'2.1-2.2 sigma (D1409)'}
first=[k for k,v in out['ns'].items() if v['counted'] and v['sigma']>=3]
out['ns_first_3sigma_real']=first
out['verdict']='n_s first (SO+SPHEREx, ~2027+)' if 'SO+SPHEREx' in first else 'undetermined'
out['D1438_corrected']=out['r_official_dr1e-3']['S_lo']<3
json.dump(out,open('field_tests/results/D1440_first_decider.json','w'),indent=1); print(json.dumps(out,indent=1))
