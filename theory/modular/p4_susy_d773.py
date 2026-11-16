"""D773 (locked PREREG_D773). AI-assisted."""
import sympy as sp, itertools
S,t1,t2,t3=sp.symbols('S t1 t2 t3')
def susy(W,vars_):
    eqs=[W]+[sp.diff(W,v) for v in vars_]
    return sp.solve(eqs,vars_,dict=True)
# K4
W1=(t3-S)*(2*t1*t2+3); sol=susy(W1,[S,t1,t2,t3]); print("K4 Model I solutions:",sol)
# (1) P4
c,d=2,3
W4=-S*(c*t2*t3+d); sol4=susy(W4,[S,t2,t3]); print("P4 solutions:",sol4)
def admissible(sol):
    ok=[]
    for s in sol:
        if all(v in s for v in (S,)) and all(sp.im(sp.N(s[v]))>0 for v in s if not s[v].free_symbols):
            ok.append(s)
    return ok
print("P4 admissible (all Im>0):",admissible(sol4))
# (2) general tau1-free W  -- DEVIATIONS D1: exact reduction + numpy grid check
import numpy as np
R=range(-3,4); found=0; tried=0
for f in itertools.product(R,repeat=4):
    fa=np.array(f,float)
    for h in itertools.product(R,repeat=4):
        if not any(f) and not any(h): continue
        tried+=1; ha=np.array(h,float)
        # coefficients of P = A + B t2 + C t3 + D t2 t3, each = f - S h  (mons order 1,t2,t3,t2t3)
        A,B,C,D=[(fa[k],-ha[k]) for k in range(4)]
        def mul(p,q): return (p[0]*q[0], p[0]*q[1]+p[1]*q[0], p[1]*q[1])
        Q=np.array(mul(A,D))-np.array(mul(B,C))   # q0 + q1 S + q2 S^2
        if abs(Q[2])>0:
            disc=Q[1]**2-4*Q[2]*Q[0]
            if abs(disc)>1e-12: continue
            S0=-Q[1]/(2*Q[2])+0j
        else: continue
        Dv=D[0]+D[1]*S0
        if abs(Dv)<1e-12: continue
        t2=-(C[0]+C[1]*S0)/Dv; t3=-(B[0]+B[1]*S0)/Dv
        if S0.imag>1e-9 and t2.imag>1e-9 and t3.imag>1e-9: found+=1; print("ADMISSIBLE:",f,h,S0,t2,t3)
print(f"tau1-free flux vectors tried={tried}, admissible SUSY Minkowski vacua found={found}")
print("VERDICT:", ("P4 RETIRED" if not admissible(sol4) else "P4 OK"), "|", ("tau1-free flux CP source: NONE in range -> reopen explicit CP (P1)" if found==0 else "tau1-free admissible vacua EXIST"))
