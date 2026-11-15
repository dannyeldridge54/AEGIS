import math
V=(2*29.6)**1.5; print(f"volume = {V:.1f}")
band=[]
for gs in (0.05,0.1,0.2,0.5,1.0):
    a=gs**0.25*math.sqrt(math.pi/V); b=gs**0.25/math.sqrt(V)
    if 0.1<=gs<=0.5: band.append(a)
    print(f"g_s={gs}: M_s/M_P = {a:.4f} (sqrt(pi) conv) / {b:.4f} (no sqrt(pi)); M_s = {a*2.435e18:.2e} GeV")
lo,hi=min(band),max(band)
v="CONSISTENT" if lo>=0.03 and hi<=0.1 else ("PARTLY" if hi>=0.03 and lo<=0.1 else "INCONSISTENT")
print(f"band g_s 0.1-0.5: {lo:.4f}-{hi:.4f} vs window 0.03-0.1 -> VERDICT: {v}")
