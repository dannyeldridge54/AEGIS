# Neutron ladder: from the D-T plasma to full resonance of the neutron (Prometheus plan, 23 Nov 2026)
Danny 13:13: "each layer, go way deeper, calculate all the next steps ahead, plan the path all the way to full resonance of the neutron, then do that."

The fusion tree (S1-S7, S0) ends where the neutron leaves the plasma: 80% of D-T energy rides on it. Everything downstream (breeding
the fuel, heating the blanket, damaging the wall, activating the plant) is neutron physics, and the neutron's fate in matter is decided
by nuclear RESONANCES: sharp peaks in its cross sections where it briefly forms a compound nucleus. "Full resonance" = we reconstruct those
peaks ourselves from first-principles formulas + evaluated parameters, follow the neutron through them, and close the loop back to the plant.

Every rung runs the Prometheus cycle: ~20 sourced hints -> PREREG lock (+ a held-out check that can fail) -> compute once -> referee ->
DEVIATIONS before any fix -> one rerun -> D-note -> commit/push -> CubeMind tool + queued derivations.

| Rung | What we build | Physics (derived, not fitted) | Data (public) | Goalpost (held-out) |
|---|---|---|---|---|
| N1 birth | thermal neutron spectrum from the plasma | relativistic D-T kinematics + thermal broadening (Brysk; Ballabio 1998) | Bosch-Hale (have) | mean energy shift and FWHM vs Ballabio fits at 5-20 keV; FWHM ~ 177 sqrt(T) keV |
| N2 source | where neutrons are born, wall loading | emissivity = (n_D n_T <sv>) over the profiles; line of sight to the wall | ITER/SPARC profiles (have) | ITER average wall load ~0.5 MW/m2 (500 MW); peak/average |
| N3 nuclear data | cross sections for the blanket materials | ENDF/B-VIII.0 evaluations (processed) | openmc-data-storage/ENDF-B-VIII.0-NNDC (GitHub), NJOY test tapes | thermal values: Li-6(n,t) 940 b, B-10(n,a) 3840 b, H-1 capture 0.332 b |
| N4 resonances | rebuild sigma(E) from resonance parameters | Breit-Wigner (SLBW/MLBW), Reich-Moore R-matrix, penetrabilities and shift factors, potential scattering | ENDF MF2 parameters (NJOY tapes: Fe-56, Ca-40, U-235, Be-9...) | our reconstruction vs the evaluated pointwise curve (<1% away from tiny-sigma dips); Fe-56 1.15 / 27.7 keV peaks |
| N5 Doppler | resonances at temperature | psi-chi / exact kernel broadening (Solbrig) | same | broadened peak height vs analytic psi(x, zeta); U-238 6.67 eV at 300/900 K |
| N6 slowing-down | neutron energy loss | elastic kinematics, lethargy gain xi, (n,2n) / (n,n') thresholds | ENDF | xi (H 1, C 0.158, Fe 0.0353); moderation length checks |
| N7 transport | Monte Carlo neutron transport in a blanket | continuous-energy MC (free-gas, analog + implicit capture), 1-D sphere/slab | N3 data | published benchmark: natural-Li and Li-Pb sphere TBR; FNS/OKTAVIAN measured leakage spectra where available |
| N8 breeding | computed tritium breeding ratio | tallies Li-6(n,t) + Li-7(n,n't); Be/Pb (n,2n) multiplication | N3 + N7 | HCPB / WCLL published TBR (~1.1-1.2); compare with S5's required 1.051 |
| N9 energy | blanket energy multiplication M | kerma + reaction Q-values (exo/endothermic) | ENDF heating | DEMO M ~1.24-1.27 (we used 1.24 as INPUT in S0) -> replace with computed |
| N10 damage | dpa and helium in the first wall | NRT dpa (Norgett-Robinson-Torrens), gas production (n,a)/(n,p) | ENDF MT 444, 103, 107 | ~10 dpa per full-power year per MW/m2 in steel; He ~ 10 appm/dpa (S6 Gilbert values) |
| N11 activation | what the wall becomes | Bateman decay chains | NUBASE2020 + Chronos (have) | Fe-55, Co-60, Mn-54 dominance in steel after shutdown |
| N12 close the loop | plant with its own blanket | computed TBR and M into S0/S5; re-run goal dials | all above | net electricity with self-consistent blanket; tritium self-sufficiency margin |

Order: N1 -> N2 (plasma side, data in hand) ; N3 -> N4 -> N5 (resonances: the heart of "full resonance") ; N6 -> N7 -> N8 -> N9 (transport,
breeding, energy) ; N10 -> N11 (materials) ; N12 closes into the plant and fuel cycle. Each rung's tool goes to CubeMind (calc queue +
cards) when it passes.

Honest limits: no resonance self-shielding in the URR beyond probability tables if needed; 1-D geometry only until N7 passes; nuclear
data are evaluations (themselves fits to measurements) and are labelled DATA.
