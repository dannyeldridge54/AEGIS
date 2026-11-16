"""D769 (locked PREREG_D769). Two-field SERAPIS-E background. AI-assisted."""
import math
from scipy.special import kv, zeta
from scipy.integrate import solve_ivp
SIG=[0]+[sum(d**-3 for d in range(1,n+1) if n%d==0) for n in range(1,31)]
def Ese(x,y):
    s=2*zeta(4)*y*y+math.pi*zeta(3)/y
    if 2*math.pi*y<700:
        for n in range(1,31): s+=8*math.pi**2*math.sqrt(y)*n**1.5*SIG[n]*kv(1.5,2*math.pi*n*y)*math.cos(2*math.pi*n*x)
    return s
Er=Ese(0.5,math.sqrt(3)/2); C=1.15e-6
def V(x,y): e=Ese(x,y)-Er; return e/(e+1)*(1+C*e)  # DEVIATIONS D1: D692 form
def grads(x,y):
    hx=1e-5; hy=1e-6*max(y,1)
    return (V(x+hx,y)-V(x-hx,y))/(2*hx),(V(x,y+hy)-V(x,y-hy))/(2*hy)
def rhs(N,s):
    x,y,xp,yp=s; v=V(x,y); vx,vy=grads(x,y); eps=(xp*xp+yp*yp)/(4*y*y)
    xpp=(2/y)*xp*yp-(3-eps)*(xp+2*y*y*vx/v)
    ypp=-(xp*xp-yp*yp)/y-(3-eps)*(yp+2*y*y*vy/v)
    return [xp,yp,xpp,ypp]
def end(N,s): x,y,xp,yp=s; return (xp*xp+yp*yp)/(4*y*y)-1
end.terminal=True; end.direction=1
def run(x0):
    y0=25.0; vx,vy=grads(x0,y0); v=V(x0,y0)
    sol=solve_ivp(rhs,[0,2000],[x0,y0,0.0,-2*y0*y0*vy/v],events=end,rtol=1e-11,atol=1e-13,method='DOP853')
    Ne=sol.t_events[0][0]; x,y,_,_=sol.y_events[0][0]; return Ne,x,y
res={}
for x0 in (0.5,0.51,0.49,0.46,0.45,0.44,0.4,0.31,0.3,0.29,0.1):
    res[x0]=run(x0); print(f"x0={x0}: N_total={res[x0][0]:.8f} x_end={res[x0][1]:.5f} y_end={res[x0][2]:.4f}",flush=True)
H=2.3e-6; ys=14.3; dx=math.sqrt(2)*ys*H/(2*math.pi)
d45=(res[0.46][0]-res[0.44][0])/0.02; d30=(res[0.31][0]-res[0.29][0])/0.02; d2=(res[0.51][0]-2*res[0.5][0]+res[0.49][0])/0.01**2
print(f"delta_x={dx:.2e}; dN/dx0 at 0.45={d45:.3e} -> zeta={abs(d45)*dx:.2e}; at 0.3={d30:.3e} -> zeta={abs(d30)*dx:.2e}; d2N/dx2 at 1/2={d2:.3e} -> 2nd-order dN={0.5*abs(d2)*dx*dx:.2e}")
ok=max(abs(d45),abs(d30))*dx<=1e-6 and all(min(abs(r[1]-0.5),abs(r[1]+0.5))<0.05 for k,r in res.items() if 0.29<=k<=0.71)
print("VERDICT:", "PASS" if ok else "FAIL")
