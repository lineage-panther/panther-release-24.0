import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

from scripts.generate_ota_feed import make_feed_entry
from scripts.generate_ota_feed import update_build_details


class GenerateOtaFeedTest(unittest.TestCase):
    def make_package(self, directory: Path, metadata: str) -> Path:
        package = directory / "lineage-24.0-UNOFFICIAL-panther.zip"
        with zipfile.ZipFile(package, "w") as archive:
            archive.writestr("META-INF/com/android/metadata", metadata)
            archive.writestr("payload.bin", b"test payload")
        return package

    def test_builds_feed_entry_from_ota_metadata(self):
        metadata = "\n".join(
            (
                "post-timestamp=1792267200",
                "pre-device=panther",
                "post-sdk-level=36",
                "post-security-patch-level=2026-10-01",
                "post-build=google/panther/panther:17/CP2A.260705.006/15641320:user/release-keys",
                "ota-property-files=payload.bin:0:12",
            )
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            package = self.make_package(Path(temporary_directory), metadata)
            entry = make_feed_entry(package, "24.0-alpha-20261016")
            package_digest = hashlib.sha256(package.read_bytes()).hexdigest()
            package_size = package.stat().st_size

        self.assertEqual(entry["datetime"], 1792267200)
        self.assertEqual(entry["type"], "UNOFFICIAL")
        self.assertIn("UNTESTED", entry["version"])
        file_entry = entry["files"][0]
        self.assertEqual(len(entry["files"]), 1)
        self.assertEqual(file_entry["os_sdk_level"], 36)
        self.assertEqual(file_entry["os_patch_level"], "2026-10-01")
        self.assertEqual(file_entry["ota_property_files"], "payload.bin:0:12")
        self.assertEqual(file_entry["sha256"], package_digest)
        self.assertEqual(file_entry["size"], package_size)
        self.assertEqual(
            file_entry["url"],
            "https://github.com/lineage-panther/panther-release-24.0/releases/"
            "download/24.0-alpha-20261016/lineage-24.0-UNOFFICIAL-panther.zip",
        )

    def test_rejects_package_for_another_device(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            package = self.make_package(
                Path(temporary_directory),
                "post-timestamp=1792267200\npre-device=cheetah\n"
                "post-sdk-level=36\npost-security-patch-level=2026-10-01\n"
                "post-build=google/cheetah/cheetah:17/CP2A.260705.006/15641320:user/release-keys\n",
            )
            with self.assertRaisesRegex(ValueError, "not 'panther'"):
                make_feed_entry(package, "24.0-alpha-20261016")

    def test_rejects_incomplete_ota_metadata(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            package = self.make_package(
                Path(temporary_directory),
                "pre-device=panther\npost-build=google/panther/panther:17/build/id:user/release-keys\n",
            )
            with self.assertRaisesRegex(ValueError, "post-timestamp"):
                make_feed_entry(package, "24.0-alpha-20261016")

    def test_updates_only_the_marked_readme_block(self):
        readme = (
            "# Project\n\n## Build details\n\n"
            "<!-- BEGIN AUTO-GENERATED BUILD DETAILS -->\n"
            "- Android version: old\n"
            "- OTA build ID (`post-build`): `old`\n"
            "- OTA fingerprint: `old`\n"
            "- Android security patch level: `old`\n"
            "<!-- END AUTO-GENERATED BUILD DETAILS -->\n\n"
            "Keep this explanation unchanged.\n"
        )
        metadata = {
            "post-build": "google/panther/panther:17/CP2A.260705.006/15641320:user/release-keys",
            "post-security-patch-level": "2026-10-01",
        }

        updated = update_build_details(readme, metadata)

        self.assertIn("- Android version: 17", updated)
        self.assertIn("- OTA build ID (`post-build`): `CP2A.260705.006`", updated)
        self.assertIn(
            "- OTA fingerprint: `google/panther/panther:17/CP2A.260705.006/"
            "15641320:user/release-keys`",
            updated,
        )
        self.assertIn("- Android security patch level: `2026-10-01`", updated)
        self.assertIn("Keep this explanation unchanged.", updated)

    def test_cli_writes_feed_and_refreshes_readme(self):
        metadata = (
            "post-timestamp=1792267200\n"
            "pre-device=panther\n"
            "post-sdk-level=36\n"
            "post-security-patch-level=2026-10-01\n"
            "post-build=google/panther/panther:17/CP2A.260705.006/15641320:user/release-keys\n"
        )
        readme_content = (
            "# Project\n\n## Build details\n\n"
            "<!-- BEGIN AUTO-GENERATED BUILD DETAILS -->\n"
            "- old values\n"
            "<!-- END AUTO-GENERATED BUILD DETAILS -->\n"
        )
        project_root = Path(__file__).resolve().parents[1]

        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            package = self.make_package(directory, metadata)
            readme = directory / "README.md"
            output = directory / "ota" / "panther.json"
            readme.write_text(readme_content, encoding="utf-8")
            subprocess.run(
                [
                    sys.executable,
                    str(project_root / "scripts/generate_ota_feed.py"),
                    str(package),
                    "--tag",
                    "24.0-alpha-20261016",
                    "--output",
                    str(output),
                    "--readme",
                    str(readme),
                ],
                cwd=project_root,
                check=True,
                capture_output=True,
                text=True,
            )

            feed = json.loads(output.read_text(encoding="utf-8"))
            updated_readme = readme.read_text(encoding="utf-8")

        self.assertEqual(len(feed), 1)
        self.assertIn("UNTESTED", feed[0]["version"])
        self.assertIn("- Android version: 17", updated_readme)
        self.assertIn("- OTA build ID (`post-build`): `CP2A.260705.006`", updated_readme)


if __name__ == "__main__":
    unittest.main()
