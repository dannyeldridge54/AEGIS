"""D662 (locked PREREG_D662_I_LIFTS): non-R centre (t=0, g=0), eta^-2 rule. AI-assisted."""
import itertools
from fractions import Fraction as Fr
F=['Q','U','D','L','E','Hu','Hd']
W_ok=[('Q','Hu','U'),('Q','Hd','D'),('L','Hd','E'),('Hu','Hd'),('L','Hu','L','Hu')]
W_no=[('L','Hu'),('U','D','D'),('L','Q','D'),('L','L','E')]   # D660: dim-4 only
K_no=[(('Q','Q'),('U','E')),(('Q','L'),('U','D'))]
