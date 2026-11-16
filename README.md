<p align="center">
  <img src="docs/brand/panther-logo.png" alt="Panther ROM logo" width="320">
</p>

<h1 align="center">Panther ROM</h1>

<p align="center">
  <a href="https://github.com/lineage-panther/panther-release-24.0/releases"><img alt="Latest release" src="https://img.shields.io/github/v/release/lineage-panther/panther-release-24.0?label=release"></a>
  <img alt="Release status: alpha" src="https://img.shields.io/badge/status-alpha-orange">
  <img alt="Android 17" src="https://img.shields.io/badge/Android-17-green">
  <img alt="Target: Pixel 7 panther" src="https://img.shields.io/badge/device-Pixel%207%20(panther)-blue">
  <a href="https://github.com/lineage-panther/panther-release-24.0/releases"><img alt="Total release downloads" src="https://img.shields.io/github/downloads/lineage-panther/panther-release-24.0/total?label=downloads"></a>
</p>

An unofficial, community-maintained Android 17 / LineageOS 24.0-based build for Google Pixel 7 (`panther`).

This is an independent project. It is not affiliated with or endorsed by LineageOS or Google. Upstream components retain their own copyrights and licenses.

## Source repositories

The build is assembled using this project's [custom manifest](https://github.com/lineage-panther/android_manifests). The manifest references upstream sources, including:

- [LineageOS Android base manifest (`lineage-24.0`)](https://github.com/LineageOS/android/tree/lineage-24.0)
- [Pixel 7 device tree](https://github.com/LineageOS/android_device_google_panther/tree/lineage-24.0)
- [Shared Pixel device tree](https://github.com/LineageOS/android_device_google_pantah/tree/lineage-24.0)
- [Tensor G2 common device tree](https://github.com/LineageOS/android_device_google_gs201/tree/lineage-24.0)
- [Pixel device kernels](https://github.com/LineageOS/android_device_google_pantah-kernels)
- [Proprietary Pixel 7 vendor files](https://github.com/TheMuppets/proprietary_vendor_google_panther/tree/lineage-24.0)

These source repositories are maintained by their respective upstream owners; this project is not affiliated with them.

## Showcase

These screenshots show the ROM running on a Pixel 7. The wallpaper, accent colors, installed apps, and some Quick Settings labels reflect the owner's personal setup and are not defaults guaranteed by the ROM.

| Home screen | Quick Settings |
| --- | --- |
| ![Pixel 7 home screen](docs/showcase/home-screen.jpg) | ![Pixel 7 Quick Settings](docs/showcase/quick-settings.jpg) |

## Status

This release is **alpha**. We estimate it is approximately 90% functional; that is an estimate, not a measured compatibility score. The owner reports daily-driving the October 16, 2026 build. Basic ADB smoke checks confirmed Android 17, completed boot, enforcing SELinux, and running SystemUI and camera services. This does not verify every feature or hardware component; broader ADB and device testing is still needed.

## Build details

- Android version: 17
- OTA build ID (`post-build`): `CP2A.260705.006`
- OTA fingerprint: `google/panther/panther:17/CP2A.260705.006/15641320:user/release-keys`
- Android security patch level: `2026-10-01`

These values come from the release ZIP's OTA metadata. They identify this ROM build and are distinct from the stock firmware, bootloader, or baseband version currently installed on a device.

## Download

See the [24.0 alpha release](https://github.com/lineage-panther/panther-release-24.0/releases/tag/24.0-alpha-20261016) for the ROM ZIP, checksum, and boot images.

See the [installation guide](INSTALL.md) before installing.

Verify the ROM ZIP after downloading it:

```sh
sha256sum -c lineage-24.0-20261016-UNOFFICIAL-panther.zip.sha256sum
```

MindTheGapps is not included. Obtain any additional packages from their respective official sources.

## Release process

Release candidates are built and validated on the owner's local machine, then uploaded as GitHub Release assets only after the build and archive/checksum checks succeed. The weekly build schedule is best-effort: a release is not published when synchronization, compilation, or validation fails.

## Report a bug or request a feature

Use the [issue tracker](https://github.com/lineage-panther/panther-release-24.0/issues/new/choose). Include the release tag, device, installation type, steps to reproduce, and expected and actual behavior. ADB logs are useful; redact serial numbers, account data, tokens, and other private information before attaching them.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a patch.
