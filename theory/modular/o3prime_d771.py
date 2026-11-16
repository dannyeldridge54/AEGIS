"""D771 (locked PREREG_D771). AI-assisted."""
ok=False
for nflux in (12,24):
    for no3 in range(0,21,4):
        rem=32-nflux-no3
        if rem<0 or rem%2: continue
        nd3=rem//2; sols=[(N,nd3-3*N) for N in range(0,nd3//3+1)]
        good=[(N,N0) for N,N0 in sols if N-N0>=1]
        for N,N0 in good:
            ne=N-N0; lo,hi=750*ne/4,975*ne/4
            flag=" <- odd flux, O3' present" if (nflux==12 and no3>0) else (" <- all-even flux" if nflux==24 else " <- odd flux, no O3' (not allowed per 2405.18813 App A)")
            print(f"n_flux={nflux} n_O3'={no3} n_D3={nd3}: (N,N0)=({N},{N0}) N_eff={ne} ImS*Imrho={lo:.0f}-{hi:.0f} (half-unit {lo/2:.0f}-{hi/2:.0f}){flag}")
            if (nflux==12 and no3>0 and lo>=150) or (nflux==24 and lo>=150): ok=True
        if not good: print(f"n_flux={nflux} n_O3'={no3} n_D3={nd3}: no N_eff>=1 placement")
print("VERDICT:","P2 SURVIVES (restricted)" if ok else "P2 RETIRED")
