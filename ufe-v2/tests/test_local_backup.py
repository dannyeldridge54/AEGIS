import json
from pathlib import Path

import pytest

from aegis.local_backup import backup, restore


@pytest.fixture
def sources(tmp_path):
    repo = tmp_path / "repo"
    run = repo / "ufe-v2" / "cosmos_map" / "runs" / "fixture"
    tile = run / "tiles" / "L0" / "00000.csv.gz"
    tile.parent.mkdir(parents=True)
    tile.write_bytes(b"immutable tile")
    (run / "sweep_state.json").write_text(json.dumps({"level":0,"done":{"0":{"n":1}}}))
    (run / "pending.tmp").write_text("not completed")
    results = repo / "cmb-fit" / "results"
    results.mkdir(parents=True)
    (results / "failed.json").write_text('{"status":"failed"}')
    return repo, tmp_path / "backups"


def test_incremental_backup_full_fixture_restore_and_history(sources):
    repo, destination = sources
    first = backup(repo, destination)
    original = first.read_bytes()
    data = json.loads(original)
    assert data["files"] == 3
    assert data["new_objects"] == 3
    assert len(data["excluded_in_progress_or_locks"]) == 1
    restored = restore(destination, first)
    for name in data["entries"]:
        assert (restored / name).read_bytes() == (repo / name).read_bytes()
    second = backup(repo, destination)
    assert json.loads(second.read_text())["new_objects"] == 0
    (repo / "cmb-fit" / "results" / "failed.json").write_text('{"status":"blocked"}')
    third = backup(repo, destination)
    assert json.loads(third.read_text())["new_objects"] == 1
    assert first.read_bytes() == original
    assert (restore(destination, first) / "cmb-fit" / "results" / "failed.json").read_text() == '{"status":"failed"}'


def test_corrupt_object_blocks_backup_and_restore(sources):
    repo, destination = sources
    manifest = backup(repo, destination)
    entry = next(iter(json.loads(manifest.read_text())["entries"].values()))
    (destination / "objects" / entry["sha256"]).write_bytes(b"broken")
    with pytest.raises(ValueError, match="verification"):
        restore(destination, manifest)
    with pytest.raises(ValueError, match="corrupt"):
        backup(repo, destination)


def test_no_destination_inside_repository(sources):
    repo, _ = sources
    with pytest.raises(ValueError, match="outside"):
        backup(repo, repo / "backups")


def test_missing_completed_tile_does_not_publish_snapshot(sources):
    repo, destination = sources
    next((repo / "ufe-v2").rglob("*.csv.gz")).unlink()
    with pytest.raises(ValueError, match="regular"):
        backup(repo, destination)
    assert not (destination / "snapshots").exists()


def test_restore_rejects_traversal(sources):
    repo, destination = sources
    manifest = backup(repo, destination)
    with pytest.raises(ValueError, match="Invalid restore path"):
        restore(destination, manifest, ["..\\escape" if Path().anchor else "../escape"])
