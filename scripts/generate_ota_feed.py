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
BUILD_DETAILS_START = "<!-- BEGIN AUTO-GENERATED BUILD DETAILS -->"
BUILD_DETAILS_END = "<!-- END AUTO-GENERATED BUILD DETAILS -->"


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


def build_details(metadata: dict[str, str]) -> dict[str, str]:
    fingerprints = metadata.get("post-build", "").split("|")
    for fingerprint in fingerprints:
        product, separator, build = fingerprint.partition(":")
        product_parts = product.split("/")
        build_parts = build.split("/")
        if (
            separator
            and product_parts[-1] == DEVICE
            and len(build_parts) >= 2
        ):
            return {
                "android_version": build_parts[0],
                "build_id": build_parts[1],
                "fingerprint": fingerprint,
                "security_patch": metadata["post-security-patch-level"],
            }
    raise ValueError(f"OTA metadata has no {DEVICE} build fingerprint")


def update_build_details(readme: str, metadata: dict[str, str]) -> str:
    if readme.count(BUILD_DETAILS_START) != 1 or readme.count(BUILD_DETAILS_END) != 1:
        raise ValueError("README must contain exactly one auto-generated build details block")

    start = readme.index(BUILD_DETAILS_START)
    end = readme.index(BUILD_DETAILS_END)
    if end < start:
        raise ValueError("README build details markers are out of order")

    details = build_details(metadata)
    replacement = "\n".join(
        (
            BUILD_DETAILS_START,
            f"- Android version: {details['android_version']}",
            f"- OTA build ID (`post-build`): `{details['build_id']}`",
            f"- OTA fingerprint: `{details['fingerprint']}`",
            f"- Android security patch level: `{details['security_patch']}`",
            BUILD_DETAILS_END,
        )
    )
    return readme[:start] + replacement + readme[end + len(BUILD_DETAILS_END):]


def write_text_atomically(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent, delete=False
        ) as output:
            temporary_path = output.name
            output.write(content)
        os.replace(temporary_path, path)
    finally:
        if temporary_path and os.path.exists(temporary_path):
            os.unlink(temporary_path)


def make_feed_entry(
    package: Path, tag: str, metadata: dict[str, str] | None = None
) -> dict[str, object]:
    metadata = metadata if metadata is not None else read_metadata(package)
    required = ("post-timestamp", "pre-device", "post-sdk-level",
                "post-security-patch-level", "post-build")
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
    parser.add_argument(
        "--readme", type=Path, default=Path("README.md"),
        help="README to update (default: README.md)",
    )
    args = parser.parse_args()

    try:
        metadata = read_metadata(args.package)
        entry = make_feed_entry(args.package, args.tag, metadata)
        readme = args.readme.read_text(encoding="utf-8")
        updated_readme = update_build_details(readme, metadata)
        content = json.dumps([entry], indent=2) + "\n"
        write_text_atomically(args.output, content)
        write_text_atomically(args.readme, updated_readme)
    except (OSError, ValueError, zipfile.BadZipFile, KeyError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
