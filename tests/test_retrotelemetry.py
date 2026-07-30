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

        self.assertGreaterEqual(manifest["game_count"], 1)
        self.assertEqual(entry["game_id"], "mega-drive.sonic-the-hedgehog")
        self.assertEqual(entry["telemetry_layout_id"], "sonic-1-mega-drive-revision-0")
        self.assertEqual(entry["path"], "games/mega-drive/sonic-the-hedgehog.json")

    def test_mega_drive_experimental_batch_is_present_and_never_claims_verification(self):
        names = {
            "alien-soldier.json", "altered-beast.json", "battletoads.json",
            "castlevania-bloodlines.json", "columns.json", "comix-zone.json",
            "dr-robotniks-mean-bean-machine.json", "dynamite-headdy.json",
            "golden-axe.json", "golden-axe-iii.json", "mega-turrican.json",
            "mortal-kombat-ii.json", "musha.json", "ristar.json",
            "rocket-knight-adventures.json", "shadow-dancer-the-secret-of-shinobi.json",
            "shinobi-iii-return-of-the-ninja-master.json", "sonic-3-and-knuckles.json",
            "sonic-and-knuckles.json", "sonic-the-hedgehog-2.json",
            "sonic-the-hedgehog-3.json", "splatterhouse-2.json",
            "streets-of-rage.json", "streets-of-rage-2.json", "streets-of-rage-3.json",
            "strider.json", "super-hang-on.json", "the-revenge-of-shinobi.json",
            "thunder-force-iv.json", "vectorman.json",
        }
        root = ROOT / "games" / "mega-drive"
        self.assertTrue(all((root / name).is_file() for name in names))
        for name in names:
            data = json.loads((root / name).read_text(encoding="utf-8"))
            self.assertTrue(all(item["verification_state"] == "experimental" for item in data["roms"]))
            for layout in data["telemetry_layouts"]:
                self.assertEqual(layout["verification_state"], "experimental")
                self.assertTrue(all(item["verification_state"] == "experimental" for item in layout["properties"]))

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
