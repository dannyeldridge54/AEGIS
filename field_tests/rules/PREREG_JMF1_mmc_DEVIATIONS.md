# JMF1 DEVIATIONS
D1 (2026-11-17, before any JMF1 number was read): the first run crashed in MY output parser for R = 1 (no CSV line found in MMC stdout); no Janus or MMC
number was printed. Fix: locate the CSV data line as the line right after the header line that starts with "phi0001" (column positions from that header:
ns, r by name), and if MMC fails, record its last 5 stdout lines for that R and continue. Model, claims and tolerances unchanged.
