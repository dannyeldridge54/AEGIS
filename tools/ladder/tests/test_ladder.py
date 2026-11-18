# AEGIS-FP T5S6TQT773EGD5TH · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License)
import importlib.util, pathlib
spec = importlib.util.spec_from_file_location("ladder", pathlib.Path(__file__).resolve().parents[1] / "ladder.py")
L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)

M = {"nodes": [{"id": "a", "status": "assumed", "title": "A"}, {"id": "b", "status": "computed", "title": "B", "depends": ["a"]},
               {"id": "c", "status": "frozen", "title": "C", "depends": ["b"]}, {"id": "x", "status": "open", "title": "X"}]}

def fresh():
    import copy; return copy.deepcopy(M)

def test_update_flags_downstream_and_keeps_frozen():
    m = fresh()
    text = "## D740 note\nMAP: node=a status=corrected touches=[x]\n## D741 other\nMAP: node=c status=killed\n"
    applied, last = L.update(m, text, 739)
    by = {n["id"]: n for n in m["nodes"]}
    assert last == 741 and len(applied) == 2
    assert by["a"]["status"] == "corrected" and "D740" in by["a"]["d"]
    assert by["b"]["flag"].startswith("recheck (D740") and "flag" in by["x"]
    assert by["c"]["status"] == "frozen"            # frozen never overwritten
    assert "flag" not in by["c"]                    # its own MAP line cleared the flag

def test_old_notes_ignored_and_unknown_node_rejected():
    m = fresh()
    applied, last = L.update(m, "## D700\nMAP: node=a status=killed\n", 739)
    assert applied == [] and last == 739
    import pytest
    with pytest.raises(SystemExit):
        L.update(fresh(), "## D745\nMAP: node=zzz status=computed\n", 739)

def test_downstream_transitive():
    assert L.downstream(fresh(), ["a"]) == {"b", "c"}

def test_ripple_no_flags_only_touches():
    m = fresh()
    L.update(m, "## D742\nMAP: node=a status=computed touches=[x] ripple=no\n", 739)
    by = {n["id"]: n for n in m["nodes"]}
    assert "flag" in by["x"] and "flag" not in by["b"]

def test_correction_note_suffix_applied_after_parent():
    m = fresh()
    text = "## D750 note\nMAP: node=a status=estimate ripple=no\n## D750a correction\nMAP: node=a status=computed ripple=no\n"
    applied, last = L.update(m, text, 749)
    by = {n["id"]: n for n in m["nodes"]}
    assert len(applied) == 2 and by["a"]["status"] == "computed" and "D750a" in by["a"]["d"]
    applied, last = L.update(m, text, last)
    assert applied == []          # nothing re-applied on a second run
