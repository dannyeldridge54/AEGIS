import mpmath as mp
exec(open('/tmp/claude-0/gh.py').read().split('for v in')[0])
L5, L3, L2 = mp.log(5), mp.log(3), mp.log(2)
CASE = {'h3': (1, 0, -5, 9, 0), 'h1': (1, -7, -20, 0, -mp.mpf(7)/2), 'none': (2, 0, 0, 0, 0)}   # omega, d_L00, d_ln2, d_ln5, d_ln3 (eq. 129 column vectors)
def D2(v, case, sc=0.5, tc=0):
    w, dL, d2, d5, d3 = CASE[case]
    return ((-12*w - 19 + dL)*Lt(0,0,v) + (2*w + 12)*Lt(0,0,2*v) - 3*Lt(1, w-1, v) - 2*Lt(sc, tc, v)
            + (-24*w + 28 + d2)*L2 - (36 + 3*w + d5)*L5 - 18*mp.log(w) + (mp.mpf(29)/2 - 5*w + d3)*L3)
def D3(v, w): return 4*Lt(0,0,v) + 4*Lt(0,0,2*v) - 6*(2-w)*Lt(1,1,v) - 7*L5 + 30*L2 + 6*mp.log(w) - 4*L3
for v in (28.6, 30):
    print(v, 'SU3', [round(float(D3(v,w))/(4*mp.pi),2) for w in (1,1,2)], 'paper -34 -34 -26 | SU2', [round(float(D2(v,c))/(4*mp.pi),2) for c in CASE], 'paper -9 +6 +7')
