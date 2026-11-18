# Provenance: how AEGIS work is marked

Every AEGIS release carries several independent authorship marks, so that copying can be shown even after a copy has been edited.

1. **Timestamped hashes.** `provenance/MANIFEST.txt` lists the SHA-256 of every file and a Merkle root. Git commits and Zenodo DOIs timestamp it publicly.
2. **Keyed stamps.** Source files, papers and docs carry an `AEGIS-FP` tag computed with a secret key held only by the author. Nobody else can forge a valid tag, and the author can verify any tag.
3. **Hidden marks.** Further marks are placed throughout the code and data. They don't change any scientific result, and their locations aren't published.
4. **Code fingerprints.** The author holds a private fingerprint database of the code (winnowing, the method behind MOSS). It recognises copied code after variables are renamed, comments are removed and files are reformatted.

The tool is `tools/provenance/fingerprint.py`, and the method is open. The key, the list of hidden-mark locations and the fingerprint database are private.

Free use is under the AEGIS Community License. Business use needs the AEGIS Commercial License (see `LICENSE`).
