"""D895 (locked PREREG_D895). LH_u AD at rho with the no-thermal yield of D646/D646a. AI-assisted."""
MP=2.435e18; v=174.0; target=8.7e-11
Qs={"median":0.020,"max":0.087}
print("m_nu1 required (eV), n_B/s = (8/23) T2 (2 v^2/m) Q/(4 MP^2):")
for T2 in (1e5,3e5,1e6):
    row=[]
    for k,Q in Qs.items():
        m=2*(8/23)*T2*v**2*Q/(4*MP**2*target)*1e9
        row.append(f"{k} Q: {m:.2e}")
    print(f"  T2={T2:.0e} GeV: "+"; ".join(row))
# Check K: FHY-extrapolated yield at D880's smallest m_nu1 vs no-thermal ceiling (delta=1)
m=4.4e-9; T2=1e5; m32=2.5e5; d=0.1
fhy=1e-11*d*(m32/1e3)*min(1,(T2/1e8)**(1/3))*(m/1e-8)**-1.5
ceil=1.0*T2*(2*v**2/(m*1e-9))/(4*MP**2)*(8/23)
print(f"K: FHY-extrapolated n_B/s={fhy:.2e} (D880 point: m=4.4e-9 eV, T2=1e5, m32=2.5e5, delta=0.1); no-thermal ceiling (delta=1)={ceil:.2e}; FHY/ceiling={fhy/ceil:.0f}")
