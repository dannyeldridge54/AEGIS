"""Verified incremental local backups; never restore over live evidence."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import uuid


SOURCES = (Path("ufe-v2") / "cosmos_map", Path("cmb-fit") / "results")


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def stamp():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "_" + uuid.uuid4().hex[:8]


def regular(path):
    if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
        raise ValueError(f"Links are not backup sources: {path}")
    if not path.is_file():
        raise ValueError(f"Not a regular backup file: {path}")


@contextmanager
def lock(destination):
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "backup.lock").open("a+b") as stream:
        if os.name == "nt":
            import msvcrt
            stream.seek(0)
            if not stream.read(1):
                stream.write(b"0")
                stream.flush()
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            if os.name == "nt":
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def store(path, destination):
    regular(path)
    objects = destination / "objects"
    objects.mkdir(exist_ok=True)
    for _ in range(3):
        before = path.stat()
        key = digest(path)
        after = path.stat()
        if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
            continue
        blob = objects / key
        if blob.exists():
            if digest(blob) != key:
                raise ValueError(f"Backup object corrupt: {blob}")
            return {"sha256": key, "bytes": after.st_size}, False
        if shutil.disk_usage(destination).free < after.st_size + 1024**3:
            raise RuntimeError("Backup capacity below required file size plus 1 GiB reserve")
        with tempfile.NamedTemporaryFile(dir=objects, suffix=".partial", delete=False) as stream:
            temporary = Path(stream.name)
        try:
            shutil.copyfile(path, temporary)
            final = path.stat()
            if ((after.st_size, after.st_mtime_ns) != (final.st_size, final.st_mtime_ns)
                    or digest(temporary) != key):
                continue
            temporary.replace(blob)
            return {"sha256": key, "bytes": after.st_size}, True
        finally:
            temporary.unlink(missing_ok=True)
    raise RuntimeError(f"Source kept changing during backup: {path}")


def backup(repo, destination):
    repo, destination = Path(repo).resolve(), Path(destination).resolve()
    if repo == destination or repo in destination.parents or destination in repo.parents:
        raise ValueError("Backup destination must be outside the repository")
    with lock(destination):
        paths = []
        excluded = []
        for relative in SOURCES:
            source = repo / relative
            if not source.is_dir():
                raise FileNotFoundError(f"Required backup source absent: {source}")
            for parent, directories, files in os.walk(source, followlinks=False):
                parent = Path(parent)
                for name in directories:
                    directory = parent / name
                    if directory.is_symlink() or (hasattr(directory, "is_junction") and directory.is_junction()):
                        raise ValueError(f"Linked backup directory: {directory}")
                for name in files:
                    path = parent / name
                    if name.endswith((".tmp", ".lock", ".partial")):
                        excluded.append(str(path.relative_to(repo)))
                    else:
                        paths.append(path)
        # Capture sweep state before its immutable completed tile files.
        paths.sort(key=lambda p: (p.name != "sweep_state.json", str(p)))
        required = sum(p.stat().st_size for p in paths)
        if not (destination / "objects").exists() and shutil.disk_usage(destination).free < required + 1024**3:
            raise RuntimeError("Insufficient initial backup capacity plus 1 GiB reserve")
        entries, copied = {}, 0
        known_paths = set(paths)
        for path in paths:
            entry, created = store(path, destination)
            entries[str(path.relative_to(repo))] = entry
            copied += int(created)
            if path.name == "sweep_state.json":
                state = json.loads((destination / "objects" / entry["sha256"]).read_text(encoding="utf-8"))
                for tile in state["done"]:
                    tile_path = path.parent / "tiles" / f"L{state['level']}" / f"{int(tile):05d}.csv.gz"
                    if tile_path not in known_paths:
                        paths.append(tile_path)
                        known_paths.add(tile_path)
        for name, entry in entries.items():
            if Path(name).name == "sweep_state.json":
                state = json.loads((destination / "objects" / entry["sha256"]).read_text(encoding="utf-8"))
                for tile in state["done"]:
                    expected = str(Path(name).parent / "tiles" / f"L{state['level']}" / f"{int(tile):05d}.csv.gz")
                    if expected not in entries:
                        raise ValueError(f"Snapshot lacks a completed tile: {expected}")
        manifest = {
            "created_utc": datetime.now(timezone.utc).isoformat(), "repo": str(repo),
            "entries": entries, "excluded_in_progress_or_locks": excluded,
            "new_objects": copied, "files": len(entries),
            "logical_bytes": sum(e["bytes"] for e in entries.values()),
            "limitations": [
                "Local copy does not protect against drive failure.",
                "File-consistent snapshots, not a transactional snapshot of active fits.",
                "In-progress temporary files are excluded; completed sweep state references are checked.",
                "Source captured at file-read time; acquisition continues.",
            ],
        }
        folder = destination / "snapshots"
        folder.mkdir(exist_ok=True)
        output = folder / f"{stamp()}.json"
        with output.open("x", encoding="utf-8") as stream:
            json.dump(manifest, stream, indent=2)
        return output


def restore(destination, manifest_path, selected=None):
    """Verify and restore a manifest into a new destination-owned restore folder."""
    destination = Path(destination).resolve()
    manifest_path = Path(manifest_path).resolve()
    if manifest_path.parent != destination / "snapshots":
        raise ValueError("Restore manifest must be in this backup's snapshots directory")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries = manifest["entries"]
    names = list(entries) if selected is None else list(selected)
    folder = destination / "restore-checks" / stamp()
    folder.mkdir(parents=True, exist_ok=False)
    for name in names:
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts or name not in entries:
            raise ValueError(f"Invalid restore path: {name}")
        entry = entries[name]
        key = entry["sha256"]
        if len(key) != 64 or any(c not in "0123456789abcdef" for c in key):
            raise ValueError("Invalid backup object identifier")
        source = destination / "objects" / key
        regular(source)
        if source.stat().st_size != entry["bytes"] or digest(source) != key:
            raise ValueError(f"Backup object verification failed: {source}")
        target = folder / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if digest(target) != key:
            raise ValueError(f"Restore verification failed: {target}")
    return folder


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--restore-check", action="store_true")
    args = parser.parse_args()
    manifest = backup(args.repo, args.destination)
    result = json.loads(manifest.read_text(encoding="utf-8"))
    print(json.dumps({"manifest": str(manifest), "files": result["files"],
                      "new_objects": result["new_objects"], "logical_bytes": result["logical_bytes"]}))
    if args.restore_check:
        names = result["entries"]
        selected = [n for n in names if Path(n).name == "sweep_state.json"]
        selected += next(([n] for n in names if n.endswith(".csv.gz")), [])
        selected += next(([n] for n in names if n.startswith(str(Path("cmb-fit") / "results"))), [])
        restored = restore(args.destination, manifest, selected)
        with (restored / "verification.json").open("x", encoding="utf-8") as stream:
            json.dump({"manifest": str(manifest), "verified_files": selected}, stream, indent=2)
        print(f"Restore check verified {len(selected)} files: {restored}")


if __name__ == "__main__":
    main()
