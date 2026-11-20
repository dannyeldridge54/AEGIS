# (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
"""M1b printable finder chart (20 Nov 2026). Print it, take it to the telescope.
chart(target, field_deg=8, fov_arcmin=(60,), mag_max=None, aperture_mm=None, out='chart.pdf', invert=True)
  target: a catalogue name ('M31', 'Vega', 'Betelgeuse') or (ra_deg, dec_deg).
  Stars: Hipparcos to V = 8 (tools/mapper/data/hip_mag8.csv; d3-celestial, BSD). The faintest plotted star is
  min(8, mag_max or the aperture's rule-of-thumb limit). Messier objects are marked and labelled.
  Gnomonic (tangent-plane) projection about the target, the standard for finder charts: straight lines stay straight.
  North up, EAST LEFT (as on the sky seen from the ground). Eyepiece/finder circles, a scale bar, N/E arrows, a magnitude
  key, title with coordinates, and a provenance footer. PDF and SVG are vector and print at any size; PNG for screens."""
import csv, math, os
import numpy as np
from . import planner
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'hip_mag8.csv')

def stars():
    rows = [r for r in csv.reader(l for l in open(DATA) if not l.startswith('#'))][1:]
    a = np.array([[float(r[1]), float(r[2]), float(r[3])] for r in rows]); return a[:, 0], a[:, 1], a[:, 2]

def resolve(target):
    if isinstance(target, (tuple, list)): return float(target[0]), float(target[1]), f'RA {target[0]:.3f}°, Dec {target[1]:+.3f}°'
    import re
    m = re.fullmatch(r'\s*([-+]?\d+(?:\.\d+)?)\s*[, ]\s*([-+]?\d+(?:\.\d+)?)\s*', str(target))
    if m: return resolve((float(m.group(1)), float(m.group(2))))      # "ra,dec" in degrees
    t = target.strip().lower()
    cat = planner.catalogue()
    for o in cat:                                   # exact id or name first (so 'M3' never matches 'M31')
        n = o['name'].lower()
        if n == t or n.split(' (')[0] == t: return o['ra'], o['dec'], o['name']
    for o in cat:                                   # then common names inside brackets ('orion nebula')
        if '(' in o['name'] and t in o['name'].lower().split(' (', 1)[1]: return o['ra'], o['dec'], o['name']
    raise ValueError(f'{target!r} not in the Sky Map catalogue; give (ra_deg, dec_deg) instead')

def gnomonic(ra, dec, ra0, dec0):
    """Standard tangent-plane projection; returns (xi, eta) in degrees, xi positive to the EAST, and the mask in front."""
    r, d, r0, d0 = map(np.radians, (ra, dec, ra0, dec0))
    c = np.sin(d0)*np.sin(d) + np.cos(d0)*np.cos(d)*np.cos(r - r0)
    xi = np.cos(d)*np.sin(r - r0)/c; eta = (np.cos(d0)*np.sin(d) - np.sin(d0)*np.cos(d)*np.cos(r - r0))/c
    return np.degrees(xi), np.degrees(eta), c > 0

def fmt_ra(ra): h = ra/15; return f'{int(h):02d}h{int(h % 1*60):02d}m{(h*60 % 1)*60:04.1f}s'
def fmt_dec(dec): s = '-' if dec < 0 else '+'; d = abs(dec); return f'{s}{int(d):02d}°{int(d % 1*60):02d}′{(d*60 % 1)*60:02.0f}″'

def chart(target, field_deg=8.0, fov_arcmin=(60.0,), mag_max=None, aperture_mm=None, out='chart.pdf', invert=True):
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    ra0, dec0, name = resolve(target)
    lim = min(8.0, mag_max if mag_max is not None else (planner.mag_limit(aperture_mm) if aperture_mm else 8.0))
    sra, sdec, smag = stars(); keep = smag <= lim
    x, y, front = gnomonic(sra[keep], sdec[keep], ra0, dec0); m = smag[keep]
    h = field_deg/2; sel = front & (np.abs(x) <= h) & (np.abs(y) <= h); x, y, m = x[sel], y[sel], m[sel]
    fg, bg = ('black', 'white') if invert else ('white', 'black')
    fig, ax = plt.subplots(figsize=(8.27, 8.6)); fig.patch.set_facecolor(bg); ax.set_facecolor(bg)
    size = lambda mag: 1.5*(lim + 1.2 - np.asarray(mag))**2.2
    ax.scatter(-x, y, s=size(m), c=fg, edgecolors=bg, linewidths=0.4, zorder=3)    # minus: east to the LEFT
    for o in planner.catalogue(('messier',)):
        ox, oy, f = gnomonic(np.array([o['ra']]), np.array([o['dec']]), ra0, dec0)
        if f[0] and abs(ox[0]) <= h and abs(oy[0]) <= h:
            ax.add_patch(plt.Circle((-ox[0], oy[0]), field_deg/60, fill=False, ec='tab:red', lw=1.2, zorder=4))
            ax.annotate(o['name'].split(' (')[0], (-ox[0], oy[0]), xytext=(6, 6), textcoords='offset points', color='tab:red', fontsize=9, zorder=5)
    for fv in fov_arcmin:
        ax.add_patch(plt.Circle((0, 0), fv/120, fill=False, ec='tab:blue', lw=1.0, ls='--', zorder=2))
        ax.annotate(f"{fv:g}′ field", (fv/170, -fv/170), xytext=(4, -4), textcoords='offset points', ha='left', va='top', color='tab:blue', fontsize=8)
    ax.plot([-0.25*h, 0.25*h], [0, 0], color='tab:blue', lw=0.6); ax.plot([0, 0], [-0.25*h, 0.25*h], color='tab:blue', lw=0.6)
    # orientation arrows (top-right) and scale bar (bottom-left)
    ax.annotate('', (0.8*h, 0.95*h), (0.8*h, 0.75*h), arrowprops=dict(arrowstyle='->', color=fg)); ax.text(0.8*h, 0.97*h, 'N', color=fg, ha='center', va='bottom')
    ax.annotate('', (0.6*h, 0.75*h), (0.8*h, 0.75*h), arrowprops=dict(arrowstyle='->', color=fg)); ax.text(0.58*h, 0.75*h, 'E', color=fg, ha='right', va='center')
    bar = 1.0 if field_deg >= 4 else 0.25
    ax.plot([-0.95*h, -0.95*h + bar], [-0.95*h]*2, color=fg, lw=2); ax.text(-0.95*h + bar/2, -0.93*h, f'{bar:g}°', color=fg, ha='center', va='bottom', fontsize=9)
    keymags = [k for k in range(int(math.floor(np.min(m) if len(m) else 0)), int(lim) + 1) if k >= 0][:8]
    for i, k in enumerate(keymags):
        ax.scatter([0.95*h - i*0.09*h], [-0.95*h], s=size(k), c=fg, edgecolors=bg, linewidths=0.4); ax.text(0.95*h - i*0.09*h, -0.9*h, str(k), color=fg, ha='center', fontsize=7)
    ax.set_xlim(-h, h); ax.set_ylim(-h, h); ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_color(fg)
    ax.set_title(f'{name}   {fmt_ra(ra0)}  {fmt_dec(dec0)} (J2000)\nfield {field_deg:g}° · stars to V {lim:.1f} ({len(m)} shown) · north up, east left', color=fg, fontsize=11)
    try: from tools.prov_block import version; v = version()
    except Exception: v = 'unknown'
    fig.text(0.5, 0.015, f'AEGIS Mapper finder chart · Hipparcos stars via d3-celestial (BSD) · code {v}', ha='center', color='gray', fontsize=7)
    fig.savefig(out, facecolor=bg, bbox_inches='tight'); plt.close(fig)
    return dict(target=name, ra=ra0, dec=dec0, field_deg=field_deg, mag_limit=lim, n_stars=int(len(m)), out=out)
