"""D533 (locked PREREG_D533_PARITY_NP). AI-assisted."""
import math
ai=26.0; Ms=3.5e14; msq=1e4
lam4=math.sqrt(1e-27*(msq/100)**2)          # max lambda from dim-4
lam5=Ms/1e24                                  # max lambda from dim-5
d4=2*math.pi*ai/(-math.log(lam4)); d5=2*math.pi*ai/(-math.log(lam5))
print(f"dim-4: lambda_np < {lam4:.2e} -> delta_GS <= {d4:.2f}")
print(f"dim-5: lambda_np < {lam5:.2e} -> delta_GS <= {d5:.2f}")
dm=min(d4,d5); print(f"combined delta_GS,max = {dm:.2f}  ->  {'PASS' if dm>=1 else 'FAIL'}")
for d in (1,2,3,5): print(f"  delta_GS={d}: lambda_np = {math.exp(-2*math.pi*ai/d):.1e}")
