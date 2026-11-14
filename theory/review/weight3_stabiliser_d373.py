"""D373: a weight-3 stabiliser Y, K ⊃ |Y|²/(T+T̄)³, W ⊃ k Y (T − T_E): V(Y=0) = k²|T − T_E|² exactly (sympy). AI-assisted."""
import sympy as sp
T,Tb,Y,Yb,k,TE=sp.symbols('T Tb Y Yb k T_E')
K=-3*sp.log(T+Tb)+Y*Yb/(T+Tb)**3; W=k*Y*(T-TE); Wb=k*Yb*(Tb-TE); z=[T,Y]; zb=[Tb,Yb]
Kinv=sp.Matrix(2,2,lambda i,j: sp.diff(K,z[i],zb[j])).inv()
DW=[sp.diff(W,z[i])+sp.diff(K,z[i])*W for i in range(2)]; DWb=[sp.diff(Wb,zb[i])+sp.diff(K,zb[i])*Wb for i in range(2)]
V=sp.exp(K)*(sum(Kinv[j,i]*DW[i]*DWb[j] for i in range(2) for j in range(2))-3*W*Wb)
print(sp.factor(sp.simplify(V.subs({Y:0,Yb:0}))))
