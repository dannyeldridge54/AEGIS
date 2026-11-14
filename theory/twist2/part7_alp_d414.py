"""D414 (locked PREREG_D414_PART7): Part 7 (birefringence axion, baseline = separate light axion, not dark energy). AI-assisted.
Field a = f θ, V = m² f² (1 − cos θ); frozen until H ≈ m (matter era), then oscillates. Matter era: a_osc³ = Ω_m H0²/m², so today's
energy share Ω_a ≈ (1/6) f² θ_i² Ω_m (M_P = 1) for m ≫ H0; for m ≲ H0 it is still rolling and Ω_a ≈ (1/6)(m/H0)² f² θ_i².
β = 0.42° (c_γ/2π) Δθ with Δθ ≈ θ_i for m ≫ H0 (oscillation amplitude today ≪ θ_i), ≈ θ_i (m/H0)²/6 … for m ≲ H0 (estimate)."""
import math
Om, H0eV, Hrec = 0.31, 1.45e-33, 3.39e-29
print("window: field must still be frozen at recombination (m < H_rec = %.1e eV) and move by today (m ≳ H0 = %.1e eV)" % (Hrec, H0eV))
print(" m/H0     m[eV]      θ_i   Δθ     c_γ for β=0.261°   Ω_a (f=0.01)  Ω_a (f=0.1)  Ω_a (f=1)")
for mr in (0.5, 2, 10, 100, 1e3, 1e4):
    for th in (1.0, 2.5):
        dth = th if mr >= 2 else th * min(1.0, mr**2 / 6)
        c = 0.261 / (0.42 / (2 * math.pi) * dth)
        Oa = (lambda f: (1/6) * f*f * th*th * Om) if mr >= 2 else (lambda f: (1/6) * mr*mr * f*f * th*th)
        print(f"{mr:7.1f}  {mr*H0eV:.1e}  {th:4.1f}  {dth:5.3f}   {c:6.2f}            {Oa(0.01):.1e}       {Oa(0.1):.1e}      {Oa(1.0):.1e}")
