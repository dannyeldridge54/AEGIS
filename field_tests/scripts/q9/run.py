import numpy as np, json
Ng=3
def solve(gX,boson):
    # unknowns mq, ml, mh, mX ; set mq=1 scale later via nullspace
    # rows: sphaleron, hypercharge, portal
    # hypercharge per generation: 6*(1/6)mq + 3*(2/3)(mq+mh) + 3*(-1/3)(mq-mh) + 2*(-1/2)ml + (-1)(ml-mh) ; Higgs: 2*(1/2)*2*mh
    Yq=Ng*(1+2-1); Yh=Ng*(2+1+1)+2; Yl=Ng*(-1-1)
    A=np.array([[3,1,0,0],[Yq,Yl,Yh,0],[0,1,1,2]],float)
    ns=np.linalg.svd(A)[2][-1]; mq,ml,mh,mX=ns
    mu,md=mq+mh,mq-mh
    B=Ng*(6*mq+3*mu+3*md)/3
    nX=gX*mX*(2 if boson else 1)
    r=nX/B; return dict(nX_over_B=abs(r),m_X_GeV=5.364*0.938272/abs(r),signs_same=bool(np.sign(nX)==np.sign(B)))
o=dict(dirac_fermion=solve(2,False),complex_scalar=solve(1,True))
o['pass']=any(3<=v['m_X_GeV']<=15 for v in o.values() if isinstance(v,dict))
print(json.dumps(o,indent=1)); json.dump(o,open('field_tests/results/q9_klz.json','w'),indent=1)
