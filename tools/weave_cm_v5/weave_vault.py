#!/usr/bin/env python3
"""weave_vault v1 (22 Nov 2026): keep CubeMind/AEGIS files safe at rest.
SECURITY COMES FROM VETTED CRYPTO, NOT FROM THE MODEL: AES-256-GCM (authenticated) with a key from scrypt (n=2^17, r=8, p=1)
on Danny's passphrase, typed by Danny at the prompt (never stored, never typed by an AI). Files are compressed first (lzma),
then encrypted. Originals are never deleted. Format: b'WVLT1' | salt(16) | nonce(12) | AES-GCM(ciphertext + tag).
Usage:  python weave_vault.py lock <file> [...]     -> <file>.wvlt
        python weave_vault.py unlock <file.wvlt>    -> restores <name> next to it (refuses to overwrite)
Needs:  pip install cryptography
The Weave 'dials' randomizer (weave_dials_rng.py) is a RESEARCH object only and is never used for keys or nonces here."""
import os, sys, json, lzma, hashlib, getpass
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError:
    sys.exit('weave_vault needs the cryptography package: pip install cryptography')
MAGIC = b'WVLT1'
def _key(pw, salt): return hashlib.scrypt(pw.encode(), salt=salt, n=2**17, r=8, p=1, maxmem=256*2**20, dklen=32)
def lock(path, pw):
    raw = open(path, 'rb').read()
    meta = json.dumps({'name': os.path.basename(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}).encode()
    body = len(meta).to_bytes(4, 'big') + meta + lzma.compress(raw, preset=9)
    salt, nonce = os.urandom(16), os.urandom(12)
    ct = AESGCM(_key(pw, salt)).encrypt(nonce, body, MAGIC)
    out = path + '.wvlt'
    with open(out, 'xb') as f: f.write(MAGIC + salt + nonce + ct)
    return out
def unlock(path, pw):
    blob = open(path, 'rb').read()
    if blob[:5] != MAGIC: raise SystemExit('not a weave_vault file')
    salt, nonce, ct = blob[5:21], blob[21:33], blob[33:]
    body = AESGCM(_key(pw, salt)).decrypt(nonce, ct, MAGIC)      # raises if the passphrase is wrong or the file was altered
    n = int.from_bytes(body[:4], 'big'); meta = json.loads(body[4:4 + n]); raw = lzma.decompress(body[4 + n:])
    if hashlib.sha256(raw).hexdigest() != meta['sha256']: raise SystemExit('integrity check failed')
    out = os.path.join(os.path.dirname(os.path.abspath(path)), meta['name'])
    with open(out, 'xb') as f: f.write(raw)
    return out
if __name__ == '__main__':
    if len(sys.argv) < 3 or sys.argv[1] not in ('lock', 'unlock'): sys.exit(__doc__)
    pw = getpass.getpass('passphrase: ')
    if sys.argv[1] == 'lock' and getpass.getpass('again: ') != pw: sys.exit('passphrases differ')
    for p in sys.argv[2:]: print((lock if sys.argv[1] == 'lock' else unlock)(p, pw))
