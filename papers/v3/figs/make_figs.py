"""SERAPIS v3 figures 1-4. Data: field_tests/results (D602, D635/D632, D634) and the D595/D588 background code. AI-assisted."""
import re, math, os, sys, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
R='field_tests/results/'; O='papers/v3/figs/'
plt.rcParams.update({'font.size':10,'figure.dpi':150})
# --- potential functions (same as D588/D602 scripts)
def Ljm(y): q=math.exp(-2*math.pi*y); lj=2*math.pi*y+math.log(1+744*q+196884*q*q); return lj+math.log(abs(1-1728*math.exp(-lj)))
def Iy(y): l=Ljm(y); return (math.log(math.exp(2*(l-math.log(1728)))+1) if l<300 else 2*(l-math.log(1728)))/(4*math.pi)
def I1y(y): l=Ljm(y); return (math.log(math.exp(l-math.log(1728))+1) if l<300 else (l-math.log(1728)))/(4*math.pi)
# Fig 1: potential along imaginary axis
ys=np.exp(np.linspace(math.log(1.0005),math.log(40),600)); e=1.45e-4
P=[ (lambda x:x/(x+1))(Iy(y)**2) for y in ys]; T=[e*I1y(y) for y in ys]
fig,ax=plt.subplots(figsize=(6,3.6))
ax.plot(ys,P,label='plateau  I²/(I²+1)'); ax.plot(ys,np.array(P)+np.array(T),label='two-term, ε = 1.45×10⁻⁴')
ax.axvspan(23.2,24.5,color='0.85',label='CMB scales (y* ≈ 23–24.5)'); ax.axvline(25,ls='--',c='0.4',lw=0.8); ax.text(25.3,0.3,'string-safe\nlimit Im τ ≈ 25',fontsize=8)
ia=ax.inset_axes([0.38,0.12,0.3,0.42]); m=ys>8
ia.plot(ys[m],np.array(P)[m]); ia.plot(ys[m],(np.array(P)+np.array(T))[m]); ia.axvspan(23.2,24.5,color='0.85'); ia.set_xscale('log'); ia.set_title('plateau zoom: the tilt',fontsize=7); ia.tick_params(labelsize=6); from matplotlib.ticker import NullFormatter, FixedLocator, ScalarFormatter; ia.xaxis.set_minor_formatter(NullFormatter()); ia.xaxis.set_major_locator(FixedLocator([10,20,40])); ia.xaxis.set_major_formatter(ScalarFormatter())
ax.set_xscale('log'); ax.set_xlabel('Im τ  (Re τ = 0; vacuum at τ = i)'); ax.set_ylabel('V / V₀'); ax.legend(fontsize=7,loc='upper left'); ax.set_title('SERAPIS potential along the imaginary axis')
fig.tight_layout(); fig.savefig(O+'fig1_potential.pdf'); fig.savefig(O+'fig1_potential.png')
# Fig 2: n_s - r
rows=[l for l in open(R+'eps_window_lowtr_d602.txt') if l.startswith('eps=')]
pts={}
for l in rows:
    m=re.search(r'eps=([\d.e-]+) .*n_s=([\d.]+).*r=([\d.e-]+)',l); pts.setdefault(float(m.group(1)),[]).append((float(m.group(2)),float(m.group(3))))
fig,ax=plt.subplots(figsize=(6,3.8))
for mu,s,lab,c in ((0.9682,0.0032,'CMB (SPA+BK)','tab:blue'),(0.9728,0.0029,'CMB+DESI','tab:orange')):
    for k,a in ((1,0.18),(2,0.08)): ax.axvspan(mu-k*s,mu+k*s,color=c,alpha=a,lw=0)
    ax.plot([],[],c=c,lw=6,alpha=0.3,label=f'{lab}: 1σ, 2σ')
ka=[l for l in open(R+'janus_analytic_d635.txt') if l.startswith('HS-Kairos')]
kp=[(float(re.search(r'n_s=([\d.]+)',l).group(1)),float(re.search(r' r=([\d.e-]+)',l).group(1))) for l in ka]
ax.scatter(*zip(*kp),marker='s',c='k',label='Kairos (ε = 0), N* = 47, 50')
for eps,mk,cc in ((1.3e-4,'o','tab:red'),(1.6e-4,'^','tab:purple')):
    ax.scatter(*zip(*pts[eps]),marker=mk,c=cc,label=f'Chronos, ε = {eps*1e4:.1f}×10⁻⁴ (allowed)')
ax.set_xlabel('n_s'); ax.set_ylabel('r'); ax.set_ylim(2e-4,7e-4); ax.set_xlim(0.955,0.985); ax.legend(fontsize=7,loc='upper left'); ax.set_title('Janus pair against current data (r < 0.034 everywhere here)')
fig.tight_layout(); fig.savefig(O+'fig2_ns_r.pdf'); fig.savefig(O+'fig2_ns_r.png')
# Fig 3: alpha_s vs n_s
fig,ax=plt.subplots(figsize=(6,3.6))
n=np.linspace(0.955,0.98,100); ax.plot(n,-(1-n)**2/2*1e4,'k--',label='plain attractor  −(1−n_s)²/2')
for l in open(R+'janus_analytic_d635.txt'):
    m=re.search(r'^(\S+(?: [\d.e-]+)?) N\*=(\d+): n_s=([\d.]+) .*alpha_exact=([-\d.e]+)',l)
    if m: ax.scatter(float(m.group(3)),float(m.group(4))*1e4,c='k' if m.group(1)=='HS-Kairos' else 'tab:red',marker='s' if m.group(1)=='HS-Kairos' else 'o')
for l in open(R+'rho_running_d634.txt'):
    m=re.search(r'n_s=([\d.]+) alpha_s=([-\d.e]+)',l)
    if m: ax.scatter(float(m.group(1)),float(m.group(2))*1e4,c='tab:green',marker='^')
ax.scatter([],[],c='k',marker='s',label='Kairos'); ax.scatter([],[],c='tab:red',label='Chronos (τ = i), ε = 1.0–1.6×10⁻⁴'); ax.scatter([],[],c='tab:green',marker='^',label='SERAPIS-ρ, ε = 6×10⁻⁵')
ax.set_xlabel('n_s'); ax.set_ylabel('α_s  (×10⁻⁴)'); ax.legend(fontsize=7); ax.set_title('Running signature: 2–3× a plain attractor at the same n_s')
fig.tight_layout(); fig.savefig(O+'fig3_running.pdf'); fig.savefig(O+'fig3_running.png')
# Fig 4: w(N) after inflation (D595 background, eps=1e-4)
src=open('theory/modular/adiabatic_y_d592.py').read(); src=src[:src.index('for R in (10,30,100):')]
g={}; exec(compile(src,'bg','exec'),g)
p,pd,N=g['st']; from scipy.integrate import solve_ivp
sol=g['solve_ivp'](g['rhsB'],[g['ts'],1e14],[p,pd,N],rtol=1e-10,atol=1e-13,events=lambda t,s:s[2]-(g['Ne']+3),max_step=1.0)
NN=sol.y[2]; rho=0.5*sol.y[1]**2+np.array([g['v'](x) for x in sol.y[0]])
Nb=np.linspace(g['Ne']-1,g['Ne']+2.6,73); w=[]
for c in Nb:
    m=(NN>=c-0.25)&(NN<=c+0.25); w.append(-np.polyfit(NN[m],np.log(rho[m]),1)[0]/3-1)
w=np.array(w)
fig,ax=plt.subplots(figsize=(6,3.4)); ax.plot(Nb-g['Ne'],w)
for v,lab in ((0.6,'octic, w = 3/5'),(0,'matter'),(-1/3,'end of inflation')): ax.axhline(v,ls=':',c='0.5'); ax.text(-0.95,v+0.02,lab,fontsize=8)
ax.set_xlabel('e-folds after the end of inflation'); ax.set_ylabel('effective w (0.5 e-fold window)'); ax.set_title('Stiff phase after inflation (two-term, ε = 10⁻⁴)')
fig.tight_layout(); fig.savefig(O+'fig4_w.pdf'); fig.savefig(O+'fig4_w.png'); print('done')
