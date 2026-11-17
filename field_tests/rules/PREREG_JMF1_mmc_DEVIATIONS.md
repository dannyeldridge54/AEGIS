# JMF1 DEVIATIONS
D1 (2026-11-17, before any JMF1 number was read): the first run crashed in MY output parser for R = 1 (no CSV line found in MMC stdout); no Janus or MMC
number was printed. Fix: locate the CSV data line as the line right after the header line that starts with "phi0001" (column positions from that header:
ns, r by name), and if MMC fails, record its last 5 stdout lines for that R and continue. Model, claims and tolerances unchanged.
D2 (same day, after D1's rerun printed only MMC's stdout tails, no comparison computed): with num_inflaton = 2 MMC does not echo the CSV row to stdout
(it did for the 10-field default). The exact r is therefore taken from MMC's printed lines as r = (r/n_t)·n_t (both "exact" values, first number on each
line). n_s parsing unchanged. Claims unchanged.
