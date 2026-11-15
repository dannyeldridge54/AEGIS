import math, sys, io, contextlib
sys.path.insert(0,'theory/deep')
with contextlib.redirect_stdout(io.StringIO()): import modular_twist_d490 as M
from scipy.optimize import brentq
def nfix(e): return brentq(lambda n:(M.lnV(0.0,n,e,True)-M.lnV(math.log(M.obs(n,e,True)[0]),n,e,True))-math.log(6e-111),150,400,xtol=1e-3)
def ns_of(e): n=nfix(e); return M.obs(n,e,True)[1]-0.9736
e=brentq(ns_of,1e-8,3.04e-7,xtol=1e-11); n=nfix(e); x,ns,r=M.obs(n,e,True)
a=-(M.obs(n,e,True,57.45)[1]-M.obs(n,e,True,56.95)[1])/0.5
print(f"eps={e:.3e}, n={n:.2f}, x*={x:.2e}, n_s={ns:.4f}, r={r:.5f}, alpha_s={a:.2e}; r/(1-ns)^2={r/(1-ns)**2:.2f}; vs Route A r=0.0046")
print("VERDICT:", "VIABLE WITH ONE FIT" if r<0.036 else "NO")
