# Geometry guide for CubeMind's models (how to look for things)

Read this before you sort anything. It explains the shapes the field is built on, in plain words.

## 1. The torus and its shape
Many models in this field curl extra dimensions into small donut shapes (tori). A torus is made from a flat grid of points (a lattice)
with opposite edges glued. The SHAPE of the grid is one complex number, written U or tau. Its real part slides the rows sideways; its
imaginary part sets how tall the cells are compared with how wide.
- **rho = e^(i pi/3) = 1/2 + 0.866i** is the HEXAGONAL grid (cells are equilateral triangles). It is the most symmetric shape: it looks the
  same after turning by 60 degrees. Anything about hexagons, triangles, 60 or 120 degree turns, the number 3, SU(3), or "Z3" points to rho.
- **i = 0 + 1i** is the SQUARE grid. It looks the same after turning by 90 degrees. Squares, 90 degrees, the number 2, "Z2", point to i.
- **the cusp (i times infinity)** is a grid stretched without limit: the torus becomes a long thin tube. Words like "decompactification",
  "large volume", "weak coupling limit", "asymptotic", point to the cusp.

## 2. The modular group: the same shape seen many ways
Different grids can describe the same torus (you can redraw the same grid with different cells). The rules that redraw it form the
MODULAR GROUP. Because of it, every shape has copies all over the upper half-plane. Draw the basic tile (|x| <= 1/2 and |tau| >= 1);
the group copies it again and again, smaller and smaller toward the real axis. This is the fractal: a result at rho holds at every copy of rho.
Only three places are special: rho, i and the cusp. A potential that respects the group always has a flat spot (zero slope) at rho and at i.

## 3. Eisenstein series: a sum over every point of the grid
E_s(tau) adds up 1/|distance|^(2s) over every grid point (except the origin), times a height factor. It measures the shape of the grid.
Its number s is its WEIGHT. Each weight has a fixed "Laplace number" s(s-1): weight 2 gives 2, weight 3/2 gives 3/4.
SERAPIS-E uses weight 2. The Weave and YFORK2 use weight 3/2. Different weights mean different fields: never treat them as one.

## 4. Orbifolds: tori folded by turning
Six extra dimensions = three tori. An ORBIFOLD folds them by turning each torus.
- **T6/(Z2 x Z2)** (SERAPIS-E): turns by 180 degrees. Any grid shape is allowed, so the shape U is free to move.
- **Z6-II** (the Weave): turns by 60, 120 and 180 degrees. A grid can only survive a 60 or 120 degree turn if it is hexagonal, so two of
  the three tori are FROZEN at rho. This is why rho keeps appearing: the geometry forces it.
These two foldings are different. Nobody has yet found one construction that contains both. That is the main open gap.

## 5. Where things sit in CubeMind
**Rings:** R1 SERAPIS-E (U, weight 2) · R2 Weave/YFORK2 (S or tau, weight 3/2) · R3 late thread (dark energy, the field phi) ·
R4 matter (dust, radiation, growth, lensing, perturbations) · R5 bridges and limits (couplings between rings, bounds like fifth forces,
BBN, moduli). Anything not about the field goes to "outside".
**Side:** left = early universe (inflation, n_s, r) · centre = pure mathematics and geometry · right = late universe (dark energy, today).
**Layers (inside to outside):** torus, pyramid, turnover, cube, fold, dilaton, forces, cosmology, late universe.

## 6. How to look (do this for every item)
1. Ask: which SHAPE does it talk about? hexagon -> rho; square -> i; stretched/large volume -> cusp; a measured number -> data; a limit -> bound.
2. Ask: which WEIGHT or function? weight 2 -> R1; weight 3/2 -> R2; none -> decide by topic.
3. Ask: which FOLDING? Z2xZ2 -> R1; Z6 or Z6-II or hexagonal freezing -> R2.
4. Ask: early or late universe, or pure maths? That is the side.
5. Ask: how far from the centre? Geometry of the torus is inside (torus, pyramid); forces and cosmology are outside.
6. Only link two things if the computer proposed the link AND you can say in one sentence why they connect.
7. If you are not sure, say "unsure". Never guess a ring to fill a gap.
