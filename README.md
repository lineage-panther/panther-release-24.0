# Panther ROM

An unofficial, community-maintained Android 17 / LineageOS 24.0-based build for Google Pixel 7 (`panther`).

This is an independent project. It is not affiliated with or endorsed by LineageOS or Google. Upstream components retain their own copyrights and licenses.

## Status

This release is **alpha**. The developer estimates it is approximately 90% functional; that is an estimate, not a measured compatibility score. The developer reports daily-driving the October 16, 2026 build. Basic ADB smoke checks confirmed Android 17, completed boot, enforcing SELinux, and running SystemUI and camera services. This does not verify every feature or hardware component; broader ADB and device testing is still needed.

## Download

See the [24.0 alpha release](https://github.com/lineage-panther/panther-release-24.0/releases/tag/24.0-alpha-20261016) for the ROM ZIP, checksum, and boot images.

Verify the ROM ZIP after downloading it:

```sh
sha256sum -c lineage-24.0-20261016-UNOFFICIAL-panther.zip.sha256sum
```

MindTheGapps is not included. Obtain any additional packages from their respective official sources.

## Report a bug or request a feature

Use the [issue tracker](https://github.com/lineage-panther/panther-release-24.0/issues/new/choose). Include the release tag, device, installation type, steps to reproduce, and expected and actual behavior. ADB logs are useful; redact serial numbers, account data, tokens, and other private information before attaching them.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a patch.
