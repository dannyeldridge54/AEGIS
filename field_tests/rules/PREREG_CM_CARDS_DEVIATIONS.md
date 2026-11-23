# CM-CARDS DEVIATIONS (written before any fix)
C3 FAILS as locked (2 of 5 spot checks):
- DEV-1 U-238: the card gives 4.4629e9 y (NUBASE2020 as parsed). My goalpost 4.468e9 y is the older ENSDF/Jaffey (1971) value; NUBASE2020
  lists 4.463(3) Gy. Goalpost error (mine, same class as the 14.07 MeV shortcut), not a card error. No change to the card.
- DEV-2 Au: mendeleev stores "[Xe] 4f14 5d10 6s" (a single electron written without the "1"). Fix: normalise a bare trailing subshell
  to "...1" in the card's electron_configuration (format only), keeping the raw string as electron_configuration_raw.
- DEV-3 (found in the summary text, not a goalpost): summary() read ionization energies with int keys; after a JSON round trip the keys are
  strings -> "IE1..3 [None, None, None]". Fix: accept both.
