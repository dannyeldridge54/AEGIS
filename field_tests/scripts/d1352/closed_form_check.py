import json, numpy as np
R=json.load(open('field_tests/results/D1352_lattice_configs.json'))
worst=(0,0)
for c in R['configs']:
    a=c['three_alpha']/3; N=c['N']
    ye=np.arcsinh(np.sqrt(4/(3*a))); y=np.arccosh(np.cosh(ye)+4*N/(3*a))
    k=2/np.sqrt(6*a)  # dy/dphi
    # V=tanh^2(y/2): V'/V = k*2/sinh y ; V''/V via exact derivative
    eps=0.5*(2*k/np.sinh(y))**2
    t=np.tanh(y/2); sech2=1-t*t
    # d/dphi tanh^2(y/2) = t*sech2*k ; second derivative:
    d2=k*k*0.5*(sech2**2 - 2*t*t*sech2)
    eta=d2/(t*t)
    ns=1-6*eps+2*eta; r=16*eps
    dr=abs(c['r']-r)/r; dn=abs(c['ns']-ns)
    worst=(max(worst[0],dr),max(worst[1],dn))
    print(c['lattice'],N,'closed ns %.5f r %.4g'%(ns,r),'| num ns',c['ns'],'r',c['r'],'| rel dr %.1e dns %.1e'%(dr,dn))
print('worst rel dr %.1e, dns %.1e ->'%worst, 'PASS' if worst[0]<1e-3 and worst[1]<1e-4 else 'FAIL')
