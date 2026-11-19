# (c) Danny Lee Eldridge · AEGIS Community License
"""Smith–Kawano–Malaney (1993) / CF88 fits for the A=7 chain; N_A<sigma v> in cm^3 mol^-1 s^-1."""
import math
def he3ag(T):
    a=T/(1+0.1071*T); t3=T**(1/3)
    return 4.817e6*T**(-2/3)*math.exp(-14.964/t3)*(1+0.0325*t3-1.04e-3*t3**2-2.37e-4*T-8.11e-5*T*t3-4.69e-5*T*t3**2)+5.938e6*a**(5/6)*T**-1.5*math.exp(-12.859/a**(1/3))
def tag(T):
    b=T/(1+0.1378*T); t3=T**(1/3)
    return 3.032e5*T**(-2/3)*math.exp(-8.090/t3)*(1+0.0516*t3+0.0229*t3**2+8.28e-3*T-3.28e-4*T*t3-3.01e-4*T*t3**2)+5.109e5*b**(5/6)*T**-1.5*math.exp(-8.068/b**(1/3))
def be7np(T):
    a=T/(1+13.076*T)
    return 2.675e9*(1-0.560*T**.5+0.179*T-0.0283*T**1.5+2.214e-3*T*T-6.851e-5*T**2.5)+9.391e8*a**1.5*T**-1.5+4.467e7*T**-1.5*math.exp(-0.07486/T)
def li7pa(T):
    a=T/(1+0.759*T); t3=T**(1/3)
    return (1.096e9*T**(-2/3)*math.exp(-8.472/t3)-4.830e8*a**(5/6)*T**-1.5*math.exp(-8.472/a**(1/3))+1.06e10*T**-1.5*math.exp(-30.442/T)
            +1.56e5*T**(-2/3)*math.exp(-8.472/t3-(T/1.696)**2)*(1+0.049*t3-2.498*t3**2+0.860*T+3.518*T*t3+3.08*T*t3**2)+1.55e6*T**-1.5*math.exp(-4.478/T))
