#!/usr/bin/env python3
"""Generate the Panther Updater feed entry for an uploaded OTA package."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
import zipfile


REPOSITORY = "lineage-panther/panther-release-24.0"
DEVICE = "panther"
BUILD_TYPE = "UNOFFICIAL"
BUILD_VERSION = "24.0 ALPHA PRE-RELEASE (UNTESTED)"


def read_metadata(package: Path) -> dict[str, str]:
    with zipfile.ZipFile(package) as archive:
        metadata = archive.read("META-INF/com/android/metadata").decode("utf-8")

    values: dict[str, str] = {}
    for line in metadata.splitlines():
        if not line or line.startswith("#"):
            continue
        key, separator, value = line.partition("=")
        if not separator or key in values:
            raise ValueError(f"Invalid or duplicate OTA metadata entry: {line!r}")
        values[key] = value
    return values


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as package:
        for chunk in iter(lambda: package.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def make_feed_entry(package: Path, tag: str) -> dict[str, object]:
    metadata = read_metadata(package)
    required = ("post-timestamp", "pre-device", "post-sdk-level",
                "post-security-patch-level")
    missing = [key for key in required if key not in metadata]
    if missing:
        raise ValueError(f"OTA metadata is missing required fields: {', '.join(missing)}")
    if DEVICE not in metadata["pre-device"].split("|"):
        raise ValueError(
            f"OTA package targets {metadata['pre-device']!r}, not {DEVICE!r}"
        )

    try:
        timestamp = int(metadata["post-timestamp"])
        sdk_level = int(metadata["post-sdk-level"])
    except ValueError as error:
        raise ValueError("OTA timestamp and SDK level must be integers") from error
    if timestamp <= 0 or sdk_level <= 0:
        raise ValueError("OTA timestamp and SDK level must be positive")

    url = (
        f"https://github.com/{REPOSITORY}/releases/download/"
        f"{tag}/{package.name}"
    )
    file_entry: dict[str, object] = {
        "filename": package.name,
        "os_patch_level": metadata["post-security-patch-level"],
        "os_sdk_level": sdk_level,
        "sha256": sha256_file(package),
        "size": package.stat().st_size,
        "url": url,
    }
    if "ota-property-files" in metadata:
        file_entry["ota_property_files"] = metadata["ota-property-files"]

    return {
        "datetime": timestamp,
        "files": [file_entry],
        "type": BUILD_TYPE,
        "version": f"{BUILD_VERSION} - {tag}",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path, help="built Panther OTA ZIP")
    parser.add_argument("--tag", required=True, help="GitHub release tag containing the ZIP")
    parser.add_argument(
        "--output", type=Path, default=Path("ota/panther.json"),
        help="feed JSON output path (default: ota/panther.json)",
    )
    args = parser.parse_args()

    try:
        entry = make_feed_entry(args.package, args.tag)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        content = json.dumps([entry], indent=2) + "\n"
        temporary_path: str | None = None
        try:
            with tempfile.NamedTemporaryFile(
                "w", encoding="utf-8", dir=args.output.parent, delete=False
            ) as output:
                temporary_path = output.name
                output.write(content)
            os.replace(temporary_path, args.output)
        finally:
            if temporary_path and os.path.exists(temporary_path):
                os.unlink(temporary_path)
    except (OSError, ValueError, zipfile.BadZipFile, KeyError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
