import sys; sys.path.insert(0,'/tmp/claude-0/referee/indep'); sys.path.insert(0,'/home/claude/aegis/cmb-fit')
import numpy as np
from thread import wtable
from rt_planck_fit import rt_wtable
h=0.68; Om=0.30; Or=2.4728e-5*(1+0.2271*3.044)/h**2
for ui in (0.013,0.109,0.173):
    a,w,VL=wtable(ui,Om,Or); r=rt_wtable(ui,Om,Or); ar,wr=np.asarray(r[0]),np.asarray(r[1])
    sel=(a>=1e-3)&(a<=1); wi=np.interp(a[sel],ar[np.argsort(ar)],wr[np.argsort(ar)])
    d=np.abs(w[sel]-wi)
    print('ui',ui,'w0 mine %.4f rt %.4f'%(w[-1],np.interp(1.0,ar[np.argsort(ar)],wr[np.argsort(ar)])),'max|dw| %.2e at a=%.3f'%(d.max(),a[sel][d.argmax()]),'VL',round(VL,4),'min w mine %.4f'%w.min(), 'rt a-range',ar.min(),ar.max(),len(ar))
