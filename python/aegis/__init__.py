"""
AEGIS — Autonomous Engine for Generalized Iterative Solving
UFE (Unified Field Equation) Cosmology Framework

Discovers spacetime torsion via dual-engine optimization against
real observational data (Pantheon+, DESI BAO, Cosmic Chronometers, RSD).
"""

__version__ = "1.0.0"
__author__ = "Danny Eldridge"

from aegis.physics import (
    torsion_hubble,
    torsion_hubble_evolving,
    comoving_distance,
    comoving_distance_evolving,
    luminosity_distance,
    growth_factor,
)
from aegis.constants import (
    H0_PLANCK, OMEGA_M0, OMEGA_R0, SIGMA8_0, RS_PLANCK, C_LIGHT,
)
