"""FUSION-1 goalposts G7-G12 (S4-S6), run once as locked."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import fusion as F
from net import Bus, settle
root = F.build(); bus = Bus(); sw = settle(root, bus); b = bus.v
y = F.specific_yield_J_per_g()
r = dict(sweeps=sw, G7=dict(specific_yield=y, rel=y / 3.37e11 - 1, Phi3=F.burn_fraction(3.0), pass_=abs(y / 3.37e11 - 1) <= 0.005 and F.burn_fraction(3.0) == 1 / 3),
         G8=dict(gain_2022=3.15 / 2.05, gain_2025=5.0 / 2.05, pass_=abs(3.15 / 2.05 - 1.54) < 0.005 and abs(5.0 / 2.05 - 2.44) < 0.005),
         G9=dict(gain_needed=b['IFE_gain_needed_eta0.1'], pass_=b['IFE_gain_needed_eta0.1'] == 100),
         G10=dict(T_kg=b['T_burn_kg_per_GWfpy'], rel=b['T_burn_kg_per_GWfpy'] / 55.8 - 1, Li6_kg=b['Li6_use_kg_per_GWfpy'], half_life=b['tritium_half_life_y'],
                  tbr_example=b['TBR_example_1GW_10kg_5y'], pass_=abs(b['T_burn_kg_per_GWfpy'] / 55.8 - 1) <= 0.005),
         G11=dict(wall_load_at_model_P=b['iter_wall_load_MW_m2'], wall_load_500MW=b['design_wall_load_500MW'], area=F.ITER_WALL, pass_='report'),
         G12=dict(He=F.GILBERT, dpa=b['dpa_conversion'], pass_='partial: He quoted with conditions; dpa conversion not available in the text read'),
         example_rhoR_for_200MJ_from_1mg=F.rhoR_for(200e6, 1.0))
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'field_tests', 'results', 'fusion1_s4_s6.json'); json.dump(r, open(out, 'w'), indent=1, default=str); print(json.dumps(r, indent=1, default=str))
