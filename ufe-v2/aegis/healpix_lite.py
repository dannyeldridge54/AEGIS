"""Minimal HEALPix (nested scheme) for the AEGIS sky sweep — pure Python, no healpy needed.

Gaia DR3 source_id encodes the star's HEALPix level-12 nested pixel: source_id // 2**35.
So a level-L tile i covers exactly source_id in [i * 2**(35 + 2*(12-L)), (i+1) * 2**(35 + 2*(12-L)) - 1]
(Gaia DR3 documentation, "source_id"). Algorithms follow Gorski et al. 2005 (ApJ 622, 759).
"""
import math

_JRLL = (2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4)
_JPLL = (1, 3, 5, 7, 0, 2, 4, 6, 1, 3, 5, 7)


def _compress(v):
    """Keep every other bit (bits 0, 2, 4, ...) and pack them."""
    r = 0
    for i in range(16):
        r |= ((v >> (2 * i)) & 1) << i
    return r


def _spread(v):
    r = 0
    for i in range(16):
        r |= ((v >> i) & 1) << (2 * i)
    return r


def pix2ang_nest(nside, ipix):
    """Centre of a nested pixel -> (theta, phi) in radians (theta = colatitude)."""
    npface = nside * nside
    face, ipf = divmod(ipix, npface)
    ix, iy = _compress(ipf), _compress(ipf >> 1)
    jr = _JRLL[face] * nside - ix - iy - 1
    if jr < nside:
        nr = jr; z = 1 - nr * nr / (3.0 * npface); kshift = 0
    elif jr > 3 * nside:
        nr = 4 * nside - jr; z = nr * nr / (3.0 * npface) - 1; kshift = 0
    else:
        nr = nside; z = (2 * nside - jr) * 2.0 / (3.0 * nside); kshift = (jr - nside) & 1
    jp = (_JPLL[face] * nr + ix - iy + 1 + kshift) // 2
    if jp > 4 * nside:
        jp -= 4 * nside
    if jp < 1:
        jp += 4 * nside
    phi = (jp - (kshift + 1) * 0.5) * (math.pi / 2 / nr)
    return math.acos(max(-1.0, min(1.0, z))), phi


def ang2pix_nest(nside, theta, phi):
    z = math.cos(theta); za = abs(z); tt = (phi % (2 * math.pi)) / (math.pi / 2)
    if za <= 2.0 / 3.0:
        t1 = nside * (0.5 + tt); t2 = nside * z * 0.75
        jp = int(t1 - t2); jm = int(t1 + t2)
        ifp = jp // nside; ifm = jm // nside
        face = (ifp | 4) if ifp == ifm else (ifp if ifp < ifm else ifm + 8)
        ix = jm & (nside - 1); iy = nside - (jp & (nside - 1)) - 1
    else:
        ntt = min(3, int(tt)); tp = tt - ntt; tmp = nside * math.sqrt(3 * (1 - za))
        jp = min(nside - 1, int(tp * tmp)); jm = min(nside - 1, int((1 - tp) * tmp))
        if z >= 0:
            face = ntt; ix = nside - jm - 1; iy = nside - jp - 1
        else:
            face = ntt + 8; ix = jp; iy = jm
    return face * nside * nside + _spread(ix) + (_spread(iy) << 1)


def tile_center_radec(level, tile):
    theta, phi = pix2ang_nest(2 ** level, tile)
    return math.degrees(phi) % 360.0, 90.0 - math.degrees(theta)


def tile_source_id_range(level, tile):
    shift = 35 + 2 * (12 - level)
    return tile << shift, ((tile + 1) << shift) - 1


def n_tiles(level):
    return 12 * 4 ** level
