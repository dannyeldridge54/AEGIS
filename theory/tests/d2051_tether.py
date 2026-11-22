import math
sv, sd, ReS = 20.15, 40.3, math.sqrt(3)/2
a_inv_v4 = sv + 9*ReS; a_inv_new = sd - sv + 9*ReS
xv, xd = 2*math.pi*sv/6, 2*math.pi*sd/12
print('alpha_G^-1: v4 %.3f, tethered %.3f -> %s' % (a_inv_v4, a_inv_new, 'PASS' if abs(a_inv_new - a_inv_v4) <= 0.5 else 'FAIL'))
print('x_v %.4f, x_d %.4f, leak_rel from sigma values = %.2e' % (xv, xd, abs(1/xd - 1/xv)/(1/xv)))
w = 0.0214*xv; lo, hi = math.exp(-w), math.exp(w)
print('allowed A_d/A_v window [%.3f, %.3f] (width x%.2f) contains 1: %s -> %s' % (lo, hi, hi/lo, lo <= 1 <= hi, 'PASS' if lo <= 1 <= hi and hi/lo >= 1.3 else 'FAIL'))
