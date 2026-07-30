#!/usr/bin/env python3
"""Validate RetroTelemetry definitions and deterministically build manifest.json."""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
GAME_FORMAT = "RetroTelemetry Game Definition"
SCHEMA_VERSION = 1
HASH_PATTERNS = {
    "crc32": re.compile(r"^[0-9A-F]{8}$"),
    "md5": re.compile(r"^[0-9A-F]{32}$"),
    "sha1": re.compile(r"^[0-9A-F]{40}$"),
}
VERIFICATION_STATES = {"verified", "expected", "experimental", "broken", "unverified"}


class ValidationError(ValueError):
    pass


def _load_json(path: Path) -> Dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValidationError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValidationError(f"{path}: definition root must be an object")
    return data


def _normalise_hash(algorithm: str, value: Any) -> str:
    algorithm = str(algorithm or "").lower()
    normalised = str(value or "").strip().upper()
    if algorithm not in HASH_PATTERNS:
        raise ValidationError(f"unsupported hash algorithm: {algorithm}")
    if not HASH_PATTERNS[algorithm].fullmatch(normalised):
        raise ValidationError(f"malformed {algorithm} hash: {value!r}")
    return normalised


def _require_string(container: Dict[str, Any], key: str, context: str) -> str:
    value = container.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{context}: missing or invalid {key}")
    return value.strip()


def validate_game_definition(data: Dict[str, Any], source: str = "definition") -> None:
    if data.get("format") != GAME_FORMAT:
        raise ValidationError(f"{source}: unsupported format")
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ValidationError(f"{source}: unsupported schema_version")
    if not isinstance(data.get("definition_version"), int) or data["definition_version"] < 1:
        raise ValidationError(f"{source}: missing or invalid definition_version")
    game = data.get("game")
    if not isinstance(game, dict):
        raise ValidationError(f"{source}: game must be an object")
    game_id = _require_string(game, "id", source)
    if not re.fullmatch(r"[a-z0-9][a-z0-9.-]*", game_id):
        raise ValidationError(f"{source}: invalid game id {game_id!r}")
    _require_string(game, "title", source)
    _require_string(game, "system_id", source)
    layouts = data.get("telemetry_layouts")
    if not isinstance(layouts, list) or not layouts:
        raise ValidationError(f"{source}: telemetry_layouts must be a non-empty array")
    layout_ids = set()
    for layout in layouts:
        if not isinstance(layout, dict):
            raise ValidationError(f"{source}: layout must be an object")
        layout_id = _require_string(layout, "id", source)
        if layout_id in layout_ids:
            raise ValidationError(f"{source}: duplicate layout id {layout_id}")
        layout_ids.add(layout_id)
        if layout.get("verification_state") not in VERIFICATION_STATES:
            raise ValidationError(f"{source}: invalid layout verification state for {layout_id}")
        properties = layout.get("properties")
        if not isinstance(properties, list):
            raise ValidationError(f"{source}: layout {layout_id} properties must be an array")
        property_ids = set()
        for item in properties:
            if not isinstance(item, dict):
                raise ValidationError(f"{source}: property in {layout_id} must be an object")
            prop_id = _require_string(item, "id", source)
            if prop_id in property_ids:
                raise ValidationError(f"{source}: duplicate property id {prop_id} in {layout_id}")
            property_ids.add(prop_id)
            _require_string(item, "address", source)
            if not isinstance(item.get("length"), int) or item["length"] < 1:
                raise ValidationError(f"{source}: invalid length for {prop_id}")
            _require_string(item, "value_type", source)
            if item.get("verification_state", "unverified") not in VERIFICATION_STATES:
                raise ValidationError(f"{source}: invalid property verification state for {prop_id}")
    roms = data.get("roms")
    if not isinstance(roms, list) or not roms:
        raise ValidationError(f"{source}: roms must be a non-empty array")
    rom_ids = set()
    for rom in roms:
        if not isinstance(rom, dict):
            raise ValidationError(f"{source}: ROM must be an object")
        rom_id = _require_string(rom, "id", source)
        if rom_id in rom_ids:
            raise ValidationError(f"{source}: duplicate ROM id {rom_id}")
        rom_ids.add(rom_id)
        layout_id = _require_string(rom, "telemetry_layout_id", source)
        if layout_id not in layout_ids:
            raise ValidationError(f"{source}: ROM {rom_id} references missing layout {layout_id}")
        if rom.get("verification_state") not in VERIFICATION_STATES:
            raise ValidationError(f"{source}: invalid ROM verification state for {rom_id}")
        hashes = rom.get("hashes")
        if not isinstance(hashes, dict):
            raise ValidationError(f"{source}: ROM {rom_id} hashes must be an object")
        for algorithm, values in hashes.items():
            if algorithm not in HASH_PATTERNS or not isinstance(values, list):
                raise ValidationError(f"{source}: invalid hashes for ROM {rom_id}")
            for value in values:
                _normalise_hash(algorithm, value)
        primary = rom.get("primary_hash")
        if not isinstance(primary, dict):
            raise ValidationError(f"{source}: ROM {rom_id} primary_hash must be an object")
        algorithm = _require_string(primary, "algorithm", source).lower()
        value = _normalise_hash(algorithm, primary.get("value"))
        if value not in [_normalise_hash(algorithm, item) for item in hashes.get(algorithm, [])]:
            raise ValidationError(f"{source}: ROM {rom_id} primary hash must also appear in hashes")
    if not isinstance(data.get("provenance"), dict):
        raise ValidationError(f"{source}: provenance must be an object")


def iter_game_files(root: Path = ROOT) -> Iterable[Path]:
    games = root / "games"
    if games.exists():
        yield from sorted(games.rglob("*.json"))


def load_validated_games(root: Path = ROOT) -> List[Tuple[Path, Dict[str, Any]]]:
    result = []
    game_ids = set()
    for path in iter_game_files(root):
        data = _load_json(path)
        validate_game_definition(data, path.as_posix())
        game_id = data["game"]["id"]
        if game_id in game_ids:
            raise ValidationError(f"duplicate game id: {game_id}")
        game_ids.add(game_id)
        result.append((path, data))
    return result


def build_manifest(root: Path = ROOT, generated_at: str | None = None) -> Dict[str, Any]:
    hash_index: Dict[str, Dict[str, Dict[str, Any]]] = {name: {} for name in HASH_PATTERNS}
    game_count = rom_count = 0
    for path, data in load_validated_games(root):
        game_count += 1
        game = data["game"]
        relative_path = path.relative_to(root).as_posix()
        for rom in data["roms"]:
            rom_count += 1
            entry = {
                "game_id": game["id"],
                "game_title": game["title"],
                "system_id": game["system_id"],
                "rom_id": rom["id"],
                "rom_label": rom.get("label", ""),
                "definition_version": data["definition_version"],
                "path": relative_path,
                "telemetry_layout_id": rom["telemetry_layout_id"],
                "verification_state": rom["verification_state"],
            }
            for algorithm, values in rom["hashes"].items():
                for value in values:
                    normalised = _normalise_hash(algorithm, value)
                    existing = hash_index[algorithm].get(normalised)
                    if existing and (existing["game_id"], existing["rom_id"]) != (entry["game_id"], entry["rom_id"]):
                        raise ValidationError(f"duplicate conflicting {algorithm} hash {normalised}")
                    hash_index[algorithm][normalised] = entry
    return {
        "format": "RetroTelemetry Manifest",
        "schema_version": SCHEMA_VERSION,
        "manifest_version": 1,
        "generated_at": generated_at or dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "game_count": game_count,
        "rom_count": rom_count,
        "hashes": {algorithm: dict(sorted(entries.items())) for algorithm, entries in hash_index.items()},
    }


def _without_timestamp(data: Dict[str, Any]) -> Dict[str, Any]:
    out = copy.deepcopy(data)
    out.pop("generated_at", None)
    return out


def write_manifest(root: Path = ROOT, check: bool = False) -> bool:
    path = root / "manifest.json"
    manifest = build_manifest(root)
    if path.exists():
        existing = _load_json(path)
        if _without_timestamp(existing) == _without_timestamp(manifest):
            return True
    if check:
        return False
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return True


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "generate", "check"))
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            load_validated_games(ROOT)
        elif args.command == "generate":
            write_manifest(ROOT)
        elif args.command == "check" and not write_manifest(ROOT, check=True):
            raise ValidationError("manifest.json is out of date; run: python tools/retrotelemetry.py generate")
    except ValidationError as exc:
        print(f"RetroTelemetry validation failed: {exc}", file=sys.stderr)
        return 1
    print("RetroTelemetry validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
