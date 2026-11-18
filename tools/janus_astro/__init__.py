# AEGIS-FP 6QIZ4WHFJ3LJIN4C · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""Janus-Astro: fast, validated astrophysics toolbox (track X). Same pattern as the Janus String Calculator:
each quantity has a fast route and an independent second route (exact solution, numerical integration or a
reference code: astropy constants, colossus), with locked validation batteries. Constants from scipy.constants
and IAU 2015 nominal values (astropy as referee). AI-assisted; see ROADMAP.md."""
from . import const, stars, compact, gw, halos, binaries
