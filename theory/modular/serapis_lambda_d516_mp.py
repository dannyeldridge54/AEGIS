import mpmath as mp, math
mp.mp.dps=50
MP=mp.mpf('2.435e18'); Vs=mp.mpf(1.5)*mp.pi**2*mp.mpf('2.1e-9')*mp.mpf('0.00323')*MP**4; Lam=mp.mpf('2.5e-47')
def eta(t,N=80):
    q=mp.e**(2j*mp.pi*t); p=mp.mpf(1)
    for n in range(1,N): p*=1-q**n
    return mp.e**(2j*mp.pi*t/24)*p
def E4(t,N=80):
    q=mp.e**(2j*mp.pi*t); return 1+240*mp.fsum(mp.fsum(d**3 for d in range(1,n+1) if n%d==0)*q**n for n in range(1,N))
def jj(t): return E4(t)**3/eta(t)**24
def V(t,a,c):
    b=-mp.mpf(1)/4-a; J=jj(t)
    H=(J-1728)**a*J**b*mp.log(J/1728)**mp.mpf(1.5)+c*J**b
    return abs(H)**2/((2*mp.im(t))**3*abs(eta(t))**12)
for a in (mp.mpf(1)/2, mp.mpf(1)):
    b=-mp.mpf(1)/4-a
    Vpl=V(mp.mpc(0,20),a,0)
    base=abs(mp.mpf(1728)**b)**2/(8*abs(eta(mp.mpc(0,1)))**12)
    c=mp.sqrt(Lam/Vs*Vpl/base)
    V0=V(mp.mpc(0,1),a,c)
    k=mp.sqrt(mp.mpf(1.5)); h=mp.mpf('1e-6')
    Vy=lambda d: V(mp.mpc(0,mp.e**(d/k)),a,c); Vx=lambda d: V(mp.mpc(d/k,1),a,c)
    myy=(Vy(h)-2*V0+Vy(-h))/h**2; mxx=(Vx(h)-2*V0+Vx(-h))/h**2
    sc=Vs/Vpl/MP**4
    print(f"a={float(a)}: c={mp.nstr(c,3)}, S=-ln c={mp.nstr(-mp.log(c),5)}; V(i)/V_pl={mp.nstr(V0/Vpl,3)} (target {mp.nstr(Lam/Vs,3)})")
    for lab,m2 in (("y",myy),("x",mxx)):
        m=mp.sqrt(abs(m2)*sc)*MP
        print(f"   {lab}: curvature {'>0' if m2>0 else '<0'}; m = {mp.nstr(m,3)} GeV")
    # test (1): plateau shape unchanged — relative change of V at y=146 and y=3.24 from the c-term
    for y in (3.242,20):
        print(f"   plateau check y={y}: dV/V from c-term = {mp.nstr(V(mp.mpc(0,y),a,c)/V(mp.mpc(0,y),a,0)-1,3)}")
