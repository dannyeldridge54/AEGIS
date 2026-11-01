"""Build the UFE release: an arXiv upload (tar.gz of the .tex plus anc/ ancillary files) and a Zenodo folder (PDF,
source, ancillary zip, metadata, SHA-256 sums). Each version builds into its own folder (release_v<N>).

Run from AEGIS/papers after `tectonic torsion_born_ede.tex`:
    python make_release.py            -> release_v3/arxiv/..., release_v3/zenodo/...
"""
import hashlib
import json
import re
import shutil
import tarfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
AEGIS = HERE.parent
FIT = AEGIS / "cmb-fit"
CUBEMIND = Path.home() / "Desktop" / "CubeMind_side_project"
VERSION = "3"
VERSION_NOTE = ("Version 3 adds Planck + ACT + SPT-3G combined tests (the locked model passes its rule; late w0-wa "
                "evolving dark energy fits better), a profile likelihood, a look-elsewhere correction (1.2-1.4 sigma "
                "global), a joint early+late fit (mild), robustness across supernova samples, the potential-power "
                "test, why geometry does not fix the potential or the lock, and a late-time outlook. The Late Twist "
                "grid, its DES-Dovekie check and the Coupled Twist fits are pre-registered; see the repository for "
                "their status.")
OUT = HERE / f"release_v{VERSION}"
TEX = HERE / "torsion_born_ede.tex"
PDF = HERE / "torsion_born_ede.pdf"

# Ancillary files: (source, name inside anc/). Every number in the paper traces to one of these.
ANC = [(FIT / n, n) for n in ("cmbfit_compare.py", "fwidth.py", "width_readback.py", "PREREG_PHASE1.md",
                              "PREREG_PHASE1_DEVIATIONS.md", "PREREGISTRATION_ZEQ.md", "PREREGISTRATION_VERDICT.md",
                              "PREREG_S8.md", "PREREG_N_PACT.md")]
ANC += [(FIT / "axiclass" / "cross_engine_pact.py", "cross_engine_pact.py"),
        (FIT / "results" / "COMPARE.md", "results/COMPARE.md"),
        (FIT / "results" / "cross_engine_pact.json", "results/cross_engine_pact.json")]
ANC += [(p, "results/" + p.name) for p in sorted((FIT / "results").glob("cmp_spt_*.json"))]
ANC += [(p, "results/" + p.name) for p in sorted((FIT / "results").glob("cmp_*_F[0-9]*.json"))
        if p.name.startswith(("cmp_pact_edelock_F", "cmp_edelockP_F"))]
ANC += [(CUBEMIND / n, n) for n in ("floquet_twist.py", "floquet_expanding.py", "PREREGISTRATION_SPT3G_N9.md",
                                    "PREREGISTRATION_SPT3G_DEVIATIONS.md", "SPT3G_RESULTS.md",
                                    "PREREGISTRATION_COMBINED_CMB.md", "COMBINED_CMB_RESULTS.md",
                                    "PREREGISTRATION_POWER_N.md", "PREREGISTRATION_PROFILE_F.md",
                                    "PREREGISTRATION_LOOK_ELSEWHERE.md", "PREREGISTRATION_EARLY_LATE.md",
                                    "PREREGISTRATION_LATE_TWIST.md", "PREREGISTRATION_NULL_PREDICTIONS.md",
                                    "STEP2_RESULT.md", "step2_potential.py", "STEP3B_RESULT.md", "step3b_trigger.py",
                                    "look_elsewhere.py", "PREREGISTRATION_ROBUSTNESS.md", "PREREGISTRATION_DOVEKIE.md",
                                    "PREREGISTRATION_SHARED_F.md", "PREREGISTRATION_LOCK_ATTRACTOR.md",
                                    "PREREGISTRATION_COUPLED_TWIST.md", "PREREGISTRATION_EDGE_SCAN.md",
                                    "PREREGISTRATION_LATE_DOVEKIE_LEE.md", "PREREGISTRATION_HIGH_MASS_CORNER.md",
                                    "EARLY_LATE_RESULTS.md", "ROBUSTNESS_RESULTS.md", "LATE_TWIST_RESULTS.md",
                                    "LATE_TWIST_NULL_MIRROR.md", "LOCK_ATTRACTOR_RESULTS.md", "PROFILE_F_RESULTS.md",
                                    "LOOK_ELSEWHERE_RESULTS.md", "rank_models.py")]
ANC += [(FIT / "results" / n, "results/" + n) for n in ("null_mirror_latetwist.json", "null_mirror_nl.json")]
ANC += [(p, "results/" + p.name) for p in sorted((FIT / "results").glob("cmp_ax_spa_*.json"))]
ANC += [(p, "results/" + p.name) for p in sorted((FIT / "results").glob("cmp_spa_*.json"))]
ANC += [(FIT / "axiclass" / "early_late_spa.py", "early_late_spa.py")]

ABSTRACT_LIMIT = 1920                       # arXiv's limit for the abstract field
HL3_NAME = "Hippocratic License 3.0 (HL3-MIL-SV: core + Military Activities + Mass Surveillance)"
HL3_URL = "https://firstdonoharm.dev/version/3/0/mil-sv.html"
LICENSE_MD = f"""# License

Copyright (c) 2012-2026 Danny Lee Eldridge.

This paper, its source and the files released with it are licensed under the **{HL3_NAME}**.
The full license text is at {HL3_URL}.

**It belongs to all.** To everyone, and to all life: every living thing, any life beyond the Earth we may one day
meet, and even an artificial mind, should one be recognised as a being of its own. No one is meant to hold this
work alone, its author included. It reached this point
only because many people led it here: the scientists whose ideas it builds on, and the teams who built the
telescopes, shared their data and wrote the public codes it uses. It is returned to all of them, and to everyone.

**Free to everyone.** Anyone, of every race, creed, nation and people, without distinction, may read, copy,
check, reuse and build on this work, provided the use respects the human rights the license sets out (including
its prohibition of discrimination) and is not used for military activities or mass surveillance.

It is offered especially to the people who will build the technologies and crafts to come.
"""


def latex_to_text(s):
    """Plain-text abstract for the arXiv form: keep $...$ maths (arXiv renders it), drop text macros."""
    s = re.sub(r"\\Mp", r"M_{\\rm Pl}", s)
    s = s.replace("--", "-").replace("~", " ")
    return re.sub(r"\s+", " ", s).strip()


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    src = TEX.read_text(encoding="utf-8")
    assert PDF.stat().st_mtime >= TEX.stat().st_mtime, "rebuild the PDF first: tectonic torsion_born_ede.tex"
    missing = [str(s) for s, _ in ANC if not s.exists()]
    assert not missing, f"missing ancillary files: {missing}"
    readme = (OUT / "README.md").read_text(encoding="utf-8") if (OUT / "README.md").exists() else None
    if OUT.exists():
        shutil.rmtree(OUT)
    arx, zen = OUT / "arxiv", OUT / "zenodo"
    if readme:
        OUT.mkdir()
        (OUT / "README.md").write_text(readme, encoding="utf-8")
    (arx / "anc").mkdir(parents=True)
    zen.mkdir(parents=True)

    # arXiv: source + anc/, packed as one tar.gz (arXiv builds the PDF itself).
    shutil.copy2(TEX, arx / TEX.name)
    (arx / "anc" / "LICENSE.md").write_text(LICENSE_MD, encoding="utf-8")
    (zen / "LICENSE.md").write_text(LICENSE_MD, encoding="utf-8")
    for s, name in ANC:
        (arx / "anc" / name).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(s, arx / "anc" / name)
    tgz = OUT / f"torsion_born_ede_v{VERSION}_arxiv.tar.gz"
    with tarfile.open(tgz, "w:gz") as t:
        t.add(arx / TEX.name, arcname=TEX.name)
        t.add(arx / "anc", arcname="anc")

    abstract = latex_to_text(re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", src, re.S).group(1))
    assert len(abstract) <= ABSTRACT_LIMIT, f"abstract is {len(abstract)} chars, over {ABSTRACT_LIMIT}"
    title = re.sub(r"\\\\\s*", " ", re.search(r"\\title\{\\textbf\{(.*?)\}\}", src, re.S).group(1))
    title = re.sub(r"\s+", " ", title.replace("--", "-")).strip()
    pages = None
    try:
        import pymupdf
        pages = pymupdf.open(PDF).page_count
    except ImportError:
        pass
    tables = src.count("\\begin{table}")
    (OUT / "ARXIV_FORM.txt").write_text(
        f"Title:\n{title}\n\nAuthors:\nDanny Lee Eldridge\n\n"
        f"Abstract ({len(abstract)} of {ABSTRACT_LIMIT} characters):\n{abstract}\n\n"
        f"Comments:\n{pages} pages, {tables} tables. {VERSION_NOTE} Code, fit outputs and hashed pre-registrations "
        f"in anc/ and at doi:10.5281/zenodo.23847152\n\n"
        "Primary category:\nastro-ph.CO\n\nCross-list:\ngr-qc\n\n"
        "License (arXiv form):\narXiv.org perpetual, non-exclusive license to distribute this article. It only lets "
        f"arXiv host the paper; the paper itself stays under the {HL3_NAME}, {HL3_URL}, as its License section "
        "and anc/LICENSE.md say. (arXiv's Creative Commons options would grant broader rights than HL3.)\n\n"
        f"Upload:\ntorsion_born_ede_v{VERSION}_arxiv.tar.gz (arXiv compiles the .tex; anc/ becomes ancillary files)\n",
        encoding="utf-8")

    # Zenodo: PDF, source, ancillary zip, metadata.
    shutil.copy2(PDF, zen / f"torsion_born_ede_v{VERSION}.pdf")
    shutil.copy2(TEX, zen / f"torsion_born_ede_v{VERSION}.tex")
    with zipfile.ZipFile(zen / f"ancillary_v{VERSION}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for s, name in ANC:
            z.write(s, name)
    meta = {
        "title": title,
        "upload_type": "publication",
        "publication_type": "preprint",
        "version": VERSION,
        "publication_date": "2026-11-01",
        "description": "<p>" + abstract.replace("$", "") + "</p><p>" + VERSION_NOTE + f" ancillary_v{VERSION}.zip "
                       "holds the code, fit outputs and pre-registration files.</p>",
        "creators": [{"name": "Eldridge, Danny Lee", "affiliation": "Independent researcher"}],
        "keywords": ["cosmology", "Hubble tension", "early dark energy", "torsion", "Barbero-Immirzi parameter",
                     "Einstein-Cartan", "SPT-3G", "ACT DR6", "pre-registration", "UFE v2"],
        "related_identifiers": [
            {"identifier": "10.5281/zenodo.23847152", "relation": "isNewVersionOf", "scheme": "doi"},
            {"identifier": "10.5281/zenodo.23838969", "relation": "references", "scheme": "doi"},
            {"identifier": "10.5281/zenodo.23839507", "relation": "references", "scheme": "doi"},
            {"identifier": "https://github.com/dannyeldridge54/AEGIS", "relation": "isSupplementedBy",
             "scheme": "url"},
            {"identifier": "https://github.com/dannyeldridge54/the-twist-torsion-cosmology",
             "relation": "isSupplementedBy", "scheme": "url"}],
        "language": "eng",
        "notes": f"License: {HL3_NAME}, {HL3_URL}. Free to everyone of every race, creed and people, for any use "
                 "that respects human rights; not for military activities or mass surveillance. In the Zenodo "
                 "form, add it as a custom license with this title and link.",
    }
    (zen / ".zenodo.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    files = sorted(p for p in zen.iterdir() if p.is_file() and p.name != "SHA256SUMS.txt")
    (zen / "SHA256SUMS.txt").write_text("".join(f"{sha(p)}  {p.name}\n" for p in files), encoding="utf-8")
    (OUT / "SHA256SUMS.txt").write_text(f"{sha(tgz)}  {tgz.name}\n", encoding="utf-8")
    print(f"arXiv: {tgz.name} ({tgz.stat().st_size // 1024} KiB, {len(ANC)} ancillary files); "
          f"abstract {len(abstract)}/{ABSTRACT_LIMIT} chars; {pages} pages")
    print(f"Zenodo: {', '.join(p.name for p in sorted(zen.iterdir()))}")


if __name__ == "__main__":
    main()
