# JMF2 DEVIATIONS
D1 (2026-11-17, before any JMF2 number): first run crashed (indexing bug in mfms.py: the tensor pair h, h' is 2 complex = 4 floats, sliced as 2). Fix the
slice width (state vector packing only); equations, model, targets and claims unchanged. One rerun.
