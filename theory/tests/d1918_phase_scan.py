import numpy as np, cmath, math, sys
rho=cmath.exp(1j*math.pi/3); U=lambda e:(rho+e-rho)/(rho+e-rho.conjugate())
uu=U(0.00311*cmath.exp(1j*math.radians(50)))
qQ,qu,qd=np.array([1.5,1,0]),np.array([.5,0,0]),np.array([.5,0,0]); Eu,Ed=qQ[:,None]+qu[None,:],qQ[:,None]+qd[None,:]
data=dict(mu=(5.58e-6,2.69e-3),md=(6.86e-4,1.37e-2),V=(0.2250,0.0410,0.00382)); w3=lambda p,d:max(p/d,d/p)<=3
def score(phi, mag=0.0457):
    ud=U(mag*cmath.exp(1j*math.radians(phi))); rng=np.random.default_rng(21)
    C=lambda: np.exp(rng.uniform(math.log(.5),math.log(2),(3,3)))*np.exp(1j*rng.uniform(0,2*math.pi,(3,3)))
    ok=0; Js=[]
    for _ in range(20000):
        Mu=C()*uu**Eu; Md=C()*ud**Ed; Uu,su,_=np.linalg.svd(Mu); Ud,sd,_=np.linalg.svd(Md)
        V=(Uu.conj().T@Ud)[::-1,::-1]; su,sd=su[::-1],sd[::-1]
        J=abs((V[0,1]*V[1,2]*np.conj(V[0,2])*np.conj(V[1,1])).imag)
        a=[su[0]/su[2],su[1]/su[2],sd[0]/sd[2],sd[1]/sd[2],abs(V[0,1]),abs(V[1,2]),abs(V[0,2])]
        if w3(a[0],data['mu'][0]) and w3(a[1],data['mu'][1]) and w3(a[2],data['md'][0]) and w3(a[3],data['md'][1]) and all(w3(a[4+k],data['V'][k]) for k in range(3)): ok+=1; Js.append(J)
    f7=ok/20000; fJ=float(np.mean([w3(j,3.08e-5) for j in Js])) if Js else 0.0
    return f7,fJ,(f7>=0.05 and fJ>=0.2)
if __name__=='__main__':
    for p in map(float,sys.argv[1:]):
        f7,fJ,b=score(p); print('phi=%6.1f deg  f7=%.1f%%  fJ=%.1f%%  both=%s'%(p,100*f7,100*fJ,b),flush=True)
