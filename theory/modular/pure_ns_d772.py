"""D772 (locked PREREG_D772). AI-assisted."""
best=0
for no3 in range(4,29,4):
    nd3=(32-no3)//2
    good=[(N,nd3-3*N) for N in range(nd3//3+1) if N-(nd3-3*N)>=1]
    if not good: print(f"n_O3'={no3} n_D3={nd3}: none"); continue
    for N,N0 in good:
        ne=N-N0; best=max(best,ne)
        print(f"n_O3'={no3} n_D3={nd3}: (N,N0)=({N},{N0}) N_eff={ne} ImS*Imrho={750*ne/4:.0f}-{975*ne/4:.0f}")
print("VERDICT:","VIABLE-ARITHMETIC" if best>=2 else "NOT VIABLE", f"(max N_eff={best})")
