import math
ReS = math.sqrt(3)/2; coef = 0.714*0.6*2*0.25*ReS
hits = []; tot = 0
for dc in range(-2, 3):
    for dd in range(-2, 3):
        tot += 1; a = 1/(1/0.1142 + coef*(dc + dd)); z = (a - 0.1180)/0.0009
        if abs(z) <= 2: hits.append((dc, dd, round(a, 5), round(z, 2)))
print('per-unit d(1/alpha_s) = %.4f' % coef)
for h in hits: print('  dk_c %+d dk_d %+d -> alpha_s %.5f z %+.2f' % h)
print('hit fraction %d/%d = %.2f' % (len(hits), tot, len(hits)/tot))
mins = [h for h in hits if abs(h[0]) + abs(h[1]) <= 2]; print('minimal hits (|dk|<=2):', mins)
