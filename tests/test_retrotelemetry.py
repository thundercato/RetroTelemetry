import copy
import json
import pathlib
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT / "tools"))

from retrotelemetry import ValidationError, build_manifest, validate_game_definition, write_manifest


class RetroTelemetryManifestTests(unittest.TestCase):
    def test_sonic_definition_validates_and_indexes_its_crc32(self):
        manifest = build_manifest(ROOT, generated_at="2026-07-30T00:00:00Z")
        entry = manifest["hashes"]["crc32"]["F9394E97"]

        self.assertEqual(manifest["game_count"], 51)
        self.assertEqual(entry["game_id"], "mega-drive.sonic-the-hedgehog")
        self.assertEqual(entry["telemetry_layout_id"], "sonic-1-mega-drive-revision-0")
        self.assertEqual(entry["path"], "games/mega-drive/sonic-the-hedgehog.json")

    def test_sonic_properties_have_canonical_ids(self):
        data = json.loads((ROOT / "games" / "mega-drive" / "sonic-the-hedgehog.json").read_text(encoding="utf-8"))
        properties = data["telemetry_layouts"][0]["properties"]

        self.assertTrue(all(item.get("canonical_id") for item in properties))
        self.assertEqual(next(item for item in properties if item["id"] == "rings")["canonical_id"], "player.1.collectable.primary")
        self.assertEqual(next(item for item in properties if item["id"] == "zone")["canonical_id"], "game.level")

    def test_researched_mega_drive_batch_is_experimental_and_traceable(self):
        definitions = sorted((ROOT / "games" / "mega-drive").glob("*.json"))
        experimental = [path for path in definitions if path.name != "sonic-the-hedgehog.json"]

        self.assertEqual(len(experimental), 50)
        for path in experimental:
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["roms"][0]["verification_state"], "experimental")
            self.assertEqual(data["telemetry_layouts"][0]["verification_state"], "experimental")
            self.assertTrue(data["roms"][0]["hashes"]["sha1"])
            self.assertEqual(data["provenance"]["sources"][0]["name"], "Stable-Retro")
            self.assertTrue(all(item["verification_state"] == "experimental" for item in data["telemetry_layouts"][0]["properties"]))

    def test_stable_retro_24_bit_work_ram_is_converted_to_core_ram(self):
        data = json.loads((ROOT / "games" / "mega-drive" / "sonic-the-hedgehog-2.json").read_text(encoding="utf-8"))
        properties = data["telemetry_layouts"][0]["properties"]
        rings = next(item for item in properties if item["id"] == "rings")

        self.assertEqual(rings["source_address"], "0x00FFFE20")
        self.assertEqual(rings["address"], "0xFE20")
        self.assertEqual(rings["memory_domain"], "core_ram")
        self.assertEqual(rings["canonical_id"], "player.1.collectable.primary")

    def test_multiple_hashes_can_reference_one_layout(self):
        data = json.loads((ROOT / "games" / "mega-drive" / "sonic-the-hedgehog.json").read_text(encoding="utf-8"))
        data["roms"][0]["hashes"]["md5"] = ["A" * 32]
        data["roms"][0]["primary_hash"] = {"algorithm": "md5", "value": "A" * 32}

        validate_game_definition(data)

    def test_missing_layout_is_rejected(self):
        data = json.loads((ROOT / "games" / "mega-drive" / "sonic-the-hedgehog.json").read_text(encoding="utf-8"))
        data["roms"][0]["telemetry_layout_id"] = "missing"

        with self.assertRaisesRegex(ValidationError, "missing layout"):
            validate_game_definition(data)

    def test_malformed_hash_is_rejected(self):
        data = json.loads((ROOT / "games" / "mega-drive" / "sonic-the-hedgehog.json").read_text(encoding="utf-8"))
        data["roms"][0]["hashes"]["crc32"] = ["not-a-hash"]

        with self.assertRaisesRegex(ValidationError, "malformed crc32"):
            validate_game_definition(data)

    def test_duplicate_hash_for_conflicting_games_is_rejected(self):
        source = ROOT / "games" / "mega-drive" / "sonic-the-hedgehog.json"
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = pathlib.Path(tmp)
            first_dir = temp_root / "games" / "mega-drive"
            second_dir = temp_root / "games" / "other-system"
            first_dir.mkdir(parents=True)
            second_dir.mkdir(parents=True)
            (first_dir / source.name).write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            conflicting = json.loads(source.read_text(encoding="utf-8"))
            conflicting["game"]["id"] = "other-system.other-game"
            conflicting["game"]["system_id"] = "other-system"
            conflicting["roms"][0]["id"] = "other-rom"
            (second_dir / "other-game.json").write_text(json.dumps(conflicting), encoding="utf-8")

            with self.assertRaisesRegex(ValidationError, "duplicate conflicting crc32 hash"):
                build_manifest(temp_root)

    def test_check_accepts_manifest_when_only_timestamp_differs(self):
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = pathlib.Path(tmp)
            (temp_root / "games" / "mega-drive").mkdir(parents=True)
            source = ROOT / "games" / "mega-drive" / "sonic-the-hedgehog.json"
            (temp_root / "games" / "mega-drive" / source.name).write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            self.assertTrue(write_manifest(temp_root))
            manifest = json.loads((temp_root / "manifest.json").read_text(encoding="utf-8"))
            manifest["generated_at"] = "2000-01-01T00:00:00Z"
            (temp_root / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

            self.assertTrue(write_manifest(temp_root, check=True))


if __name__ == "__main__":
    unittest.main()
