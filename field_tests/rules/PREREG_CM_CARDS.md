# PREREG CM-CARDS (23 Nov 2026 12:22 CT) — cards for CubeMind: formula cards for the fusion tasks + a full card for every element
Danny 12:19 "see how it's performing ... optimize it and make it go faster"; 12:20 "give it the cards for all the elements, all the known
data points, everything it's going to need ... a full breakdown of each element, as far as it can reach."

## Baseline (DATA, PC 18:17-18:20 UTC)
First 3 fusion queue tasks (fusion_sigmav): 0/3 pass, 0/3 formula_ok; ~39 s between derives (qwen3:8b, derive + self-check call).
Cause found: (a) the derive prompt prepends up to 7,000 characters of WEAVE_FACTS (cosmology) to every task, fusion included;
(b) the tasks are closed-book: the model must recall Bosch-Hale coefficients it does not know, so it invents formulas.

## Build
1. tools/fusion/fusion_cards.py: CARDS[tool] = the formula, constants and units the engine uses (open book). The task then measures
   substitution and arithmetic, not recall. nuclide_lookup and element_cooling are lookups/tables: their card points to the element card.
2. tools/fusion/element_cards.py -> element_cards.json: one card per element Z=1..118 joining (i) mendeleev 1.4.0 (atomic weight,
   configuration, all ionization energies, radii, electronegativities, thermal data, abundances, oxidation states, discovery, uses),
   (ii) NUBASE2020 (every known nuclide of that Z: mass excess, half-life, decay modes, stability), with binding energy per nucleon
   computed from the mass excess, (iii) OPEN-ADAS cooling (24 elements) where present. Every field carries its source.
3. New tools element_card (full breakdown) and element_property (one field) in fusion_cm.
4. PC learn loop: for fusion/element tools, the derive prompt uses the tool's card instead of WEAVE_FACTS (no change for other tools).

## Goalposts (locked)
C1 every element Z=1..118 has a card; every NUBASE nuclide is placed on exactly one card (count equals the catalogue).
C2 binding energy per nucleon from the card: Fe-56 within 0.01 MeV of 8.790, Ni-62 8.7945, He-4 7.074 (AME2020 values).
C3 card values equal the source for 5 spot checks (Ar IE1 15.7596 eV; Fe weight 55.845; U-238 t1/2 4.468e9 y; H-3 12.32 y; Au config [Xe] 4f14 5d10 6s1).
S1 speed: median spacing between consecutive fusion derives on the PC <= 25 s (baseline ~39 s), over the next 8 fusion derives.
A1 accuracy: >= 50% pass on the next 8 graded fusion derives from formula-derivable tools (baseline 0/3).
Honesty: open book changes what is measured (method + arithmetic, not memory). Reported as such. One rerun only; fixes via DEVIATIONS.
