import math
gs=106.75
need={0.102:{10:(0.026,0.088),100:(0.085,0.288),1e3:(0.279,0.937),1e4:(0.910,3.040),1e5:(2.962,9.840)},
      0.321:{10:(0.036,0.123),100:(0.119,0.400),1e3:(0.390,1.298),1e4:(1.266,4.197),1e5:(4.104,13.548)}}   # D447 output
for xi,d in need.items():
    print(f"xi={xi}")
    for m,(l100,l1) in d.items():
        T=m/xi; H=1.66*math.sqrt(gs)*T*T/1.22e19
        lth=(16*math.pi*H/m)**0.25            # Gamma = lam^4 T_h/(16 pi), T_h = m
        print(f"  m={m:.0e}: lambda_th={lth:.2e}; need(100%)={l100}, need(1%)={l1} -> {'THERMAL' if l100>=lth else 'NOT THERMAL'}")
