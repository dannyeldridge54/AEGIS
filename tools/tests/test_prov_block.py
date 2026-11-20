import io, json
from tools.prov_block import provenance
from tools.janus_astro import settings as H
from tools.lhc import settings as C

def test_provenance_in_every_format():
    P = provenance('Hyperion', {'omega_b': 0.02237}, H.sources(), ['D1191'])
    assert P['version'] and P['created_utc'].endswith('Z') and any('Cooke' in s for s in P['sources'])
    rows = [{'omega_b': 0.02237, 'Yp': 0.247}]
    j = json.loads(H.export(rows, 'json', P)); assert j['provenance']['toolkit'] == 'Hyperion' and j['rows'] == rows
    c = H.export(rows, 'csv', P); assert c.startswith('# toolkit: Hyperion') and 'omega_b,Yp' in c
    e = H.export(rows, 'ecsv', P); assert '#   provenance:' in e and '#     version:' in e
    assert H.export(rows, 'json').startswith('[')          # unchanged without prov

def test_ecsv_reads_in_astropy():
    try: from astropy.table import Table
    except ImportError: return
    P = provenance('Hyperion', {'x': 1}, ['s'], [])
    t = Table.read(H.export([{'a': 1, 'b': 2}], 'ecsv', P), format='ascii.ecsv')
    assert t.meta['provenance']['toolkit'] == 'Hyperion' and len(t) == 1

def test_cern1_scan_prov():
    d = json.loads(C.scan('run3', 'wino', (500,), prov=True)); assert d['provenance']['settings']['run'] == 'run3'
    assert 'name: version' in C.scan('run3', 'wino', (500,), fmt='hepdata', prov=True)

def test_h1b_ecsv_units_and_types():
    try: from astropy.table import Table
    except ImportError: return
    t = Table.read(H.export([{'model': 'x', 'mass_GeV': 700.0, 'sigma_fb': 12.5, 'n': 3}], 'ecsv'), format='ascii.ecsv')
    assert str(t['mass_GeV'].unit) == 'GeV' and t['sigma_fb'].dtype.kind == 'f' and t['n'].dtype.kind == 'i' and t['model'][0] == 'x'

def test_h1b_votable():
    try: from astropy.io.votable import parse_single_table
    except ImportError: return
    x = H.export([{'mass_GeV': 700.0, 'sigma_fb': 12.5}], 'votable', provenance('CERN+1', {}, [], []))
    t = parse_single_table(io.BytesIO(x.encode())).to_table()
    assert str(t['mass_GeV'].unit) == 'GeV' and abs(t['sigma_fb'][0] - 12.5) < 1e-12
