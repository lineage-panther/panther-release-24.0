import hashlib
from pathlib import Path
import tempfile
import unittest
import zipfile

from scripts.generate_ota_feed import make_feed_entry


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
                "post-sdk-level=36\npost-security-patch-level=2026-10-01\n",
            )
            with self.assertRaisesRegex(ValueError, "not 'panther'"):
                make_feed_entry(package, "24.0-alpha-20261016")

    def test_rejects_incomplete_ota_metadata(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            package = self.make_package(Path(temporary_directory), "pre-device=panther\n")
            with self.assertRaisesRegex(ValueError, "post-timestamp"):
                make_feed_entry(package, "24.0-alpha-20261016")


if __name__ == "__main__":
    unittest.main()
