# AEGIS-FP KDK5LKDSSCTR7QKV · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Level 2: the potential on the whole upper half-plane: vacuum finder and masses (Hessian in canonical units)."""
import numpy as np
from scipy.optimize import minimize
from .eisenstein import E_paper
RHO = (0.5, 3**0.5/2)
def V_tau(x, y, C=0.0, lam=1.0, Er=None):
    Er = E_paper(*RHO) if Er is None else Er
    e = lam*(E_paper(x, y)-Er); return e/(e+1)*(1+C*e/lam)
def find_vacuum(V, start):
    r = minimize(lambda v: V(v[0], v[1]), start, method='Nelder-Mead', options={'xatol':1e-10,'fatol':1e-16})
    return r.x, r.fun
def hessian_canonical(V, x, y, h=1e-4, n=1):
    """Hessian of V in canonical fields for K = -n log y: d^2/dphi^2 with dphi = sqrt(n/2) dx/y and sqrt(n/2) dy/y at the point."""
    f = lambda a, b: V(x+a, y+b)
    Hxx = (f(h,0)-2*f(0,0)+f(-h,0))/h**2; Hyy = (f(0,h)-2*f(0,0)+f(0,-h))/h**2
    Hxy = (f(h,h)-f(h,-h)-f(-h,h)+f(-h,-h))/(4*h*h)
    J = y/np.sqrt(n/2)   # d(x,y)/d(phi) at the point
    return np.linalg.eigvalsh(J*J*np.array([[Hxx,Hxy],[Hxy,Hyy]]))
