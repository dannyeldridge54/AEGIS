"""PREREG_BBHLTILT.md"""
import json, math, os
MP = 2.435e18; H = 5.765e12; ys = 55.64; gs = 1/ys; z3 = 1.2020569031595942
rows = []
for chi in (20, 50, 100, 200):
    for w in (1.0, 2/3):
        for C in (6.8e-7, 8.0e-7, 9.37e-7):
            V = chi*w/(4*(2*math.pi)**3*C); xi = -chi*z3/(2*(2*math.pi)**3)
            Ms = gs*MP/math.sqrt(4*math.pi*V); Mkk = gs*MP/V**(2/3)
            rows.append(dict(chi=chi, w=w, C=C, vol=V, Ms=Ms, Ms_H=Ms/H, Mkk=Mkk, Mkk_H=Mkk/H,
                             xihat_over_vol=abs(xi)*ys**1.5/V, vol_over_y15=V/ys**1.5,
                             closes=bool(Ms > Mkk > H and Mkk/H >= 1.5 and abs(xi)*ys**1.5/V < 0.1 and V > 10*ys**1.5)))
os.makedirs('field_tests/results/BBHLTILT', exist_ok=True); json.dump(rows, open('field_tests/results/BBHLTILT/rows.json', 'w'), indent=1)
for r in rows: print('chi=%-3d w=%.2f C=%.2e vol=%.2e Ms=%.2e(%.1fH) Mkk=%.2e(%.1fH) xi/V=%.1e V/y^1.5=%.0f %s'%(r['chi'],r['w'],r['C'],r['vol'],r['Ms'],r['Ms_H'],r['Mkk'],r['Mkk_H'],r['xihat_over_vol'],r['vol_over_y15'],'CLOSES' if r['closes'] else ''))
