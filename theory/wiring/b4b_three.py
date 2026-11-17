import sys, os
ext = sys.argv[1]; aeg = os.getcwd()
sys.path.insert(0, aeg)
from tools.janus_astro import bbn
wb = 0.02242; Pt = (bbn.Yp_mass(wb), bbn.DH(wb)*1e5)
os.chdir(ext); sys.path.insert(0, ext)
import PRyM.PRyM_init as I
I.aTid_flag = True; I.compute_bckg_flag = True; I.compute_nTOp_flag = True; I.compute_nTOp_thermal_flag = False
I.save_bckg_flag = I.save_nTOp_flag = I.save_nTOp_thermal_flag = False; I.verbose_flag = False; I.smallnet_flag = True; I.julia_flag = False
import PRyM.PRyM_main as Mn
r = Mn.PRyMclass().PRyMresults(); Pr = (r[3], r[5], r[7]); Lx = (0.24592, 2.4360, 5.699)
out = [f"PRyM Omegabh2 in effect: {I.Omegabh2}",
       f"PRIMAT table: Yp {Pt[0]:.5f} DH {Pt[1]:.4f}", f"PRyMordial:   Yp {Pr[0]:.5f} DH {Pr[1]:.4f} Li {Pr[2]:.4f}", f"LINX:         Yp {Lx[0]:.5f} DH {Lx[1]:.4f} Li {Lx[2]:.4f}"]
ys = [Pt[0], Pr[0], Lx[0]]; ds = [Pt[1], Pr[1], Lx[1]]
s1 = max(ys)-min(ys); s2 = (max(ds)-min(ds))/(sum(ds)/3); s3 = abs(Pr[2]/Lx[2]-1)
ok = s1 <= 1e-3 and s2 <= 0.03 and s3 <= 0.05
out += [f"Yp spread {s1:.5f} (<=0.001) | DH spread {s2:.4f} (<=0.03) | Li rel {s3:.4f} (<=0.05)", "B4b " + ("VALIDATED" if ok else "NOT VALIDATED")]
os.chdir(aeg); open('field_tests/results/b4b_three.txt','w').write("\n".join(out)+"\n"); print("\n".join(out))
