# Install Panther ROM 24.0 alpha

These are unofficial instructions for the Pixel 7 (`panther`). Read the full guide and the notes for the exact release you are installing. The owner tested the clean-install procedure on one Pixel 7; other devices, firmware versions, and installation paths have not been verified.

The release notes and the project's [current build details](README.md#build-details) identify the exact Android build ID, fingerprint, and security patch level. These ROM values are distinct from the Google stock firmware version required before installation and from the bootloader/baseband versions that may be written by the ROM payload.

Installing this ROM is at your own risk. Back up anything important first. Unlocking the bootloader **WILL** erase user data. Keep the bootloader unlocked after installation; **DO NOT** relock it while running this unofficial build.

## Clean install

### 1. Prepare the phone and computer

- Confirm the device is a Google Pixel 7 (`panther`).
- Install Android SDK Platform-Tools (`adb` and `fastboot`) on the computer and use a reliable USB cable.
- Before flashing, update to and boot the latest official Google Android 17 factory firmware for Pixel 7 (`panther`), or the exact Google firmware version documented as matching the release you are installing. **DO NOT** use an older or unverified firmware baseline, and **DO NOT** treat an Android 17 custom ROM as proof that the required stock firmware is installed. The ROM's OTA payload may replace firmware partitions during installation, as explained below.
- Remove Google accounts from the phone before unlocking to avoid Factory Reset Protection problems.
- Open the [Panther 24.0 releases](https://github.com/lineage-panther/panther-release-24.0/releases) and select the exact pre-release you intend to install. Download its ROM ZIP, matching `.sha256sum`, `boot.img`, `dtbo.img`, `vendor_boot.img`, and `vendor_kernel_boot.img` when that image is attached. Use only images and packages attached to that same release, and keep them together.
- Verify the ROM ZIP before continuing:

  ```sh
  sha256sum -c *.sha256sum
  ```

### 2. Unlock the bootloader if needed

Skip this section if the bootloader is already unlocked. Unlocking erases the phone.

1. In Android, enable Developer options, then enable **OEM unlocking** and **USB debugging**.
2. Connect the phone and run:

   ```sh
   adb devices
   adb reboot bootloader
   fastboot devices
   fastboot flashing unlock
   ```

3. Confirm the unlock on the phone using its buttons. If it reboots, return to the bootloader with **Volume Down + Power**.

### 3. Flash the release images

Open a terminal in the folder containing the images downloaded for this release. Confirm `fastboot devices` lists the phone, then run:

```sh
fastboot flash boot boot.img
fastboot flash dtbo dtbo.img
fastboot flash vendor_boot vendor_boot.img
fastboot reboot recovery
```

If the release includes `vendor_kernel_boot.img`, flash that matching image as well before rebooting to recovery:

```sh
fastboot flash vendor_kernel_boot vendor_kernel_boot.img
```

The first alpha release does not include a standalone `vendor_kernel_boot.img`. Installing that release without this separate image is at your own risk; **DO NOT** substitute an image from another build. Later releases should include and use the matching image when it is provided.

If `fastboot reboot recovery` is not supported by your bootloader, reboot to the bootloader and use the volume and power buttons to select **Recovery mode**.

**OTA payload and firmware note:** The ROM ZIP contains a full A/B OTA payload. Its `payload.bin` includes partition updates for `vendor_kernel_boot`, `vendor_boot`, `dtbo`, `init_boot`, `vbmeta` variants, and firmware components such as bootloader and modem partitions. These are not all separate release downloads: recovery applies the images embedded in the payload according to its OTA/slot metadata. In particular, **DO NOT** assume that installing the latest stock firmware first means the installed ROM will keep those exact bootloader or baseband versions. The tester reports that the installed alpha's bootloader and baseband were older than Google's October stock release.

The ROM ZIP may also update `vendor_kernel_boot` through its OTA payload. The separate image is provided for matching clean-install instructions; never mix it with another release. This unofficial procedure differs from the current [upstream LineageOS Panther installation guide](https://wiki.lineageos.org/devices/panther/install/), which describes flashing a separate `vendor_kernel_boot.img`. The procedure here has only been tested on the tester's Pixel 7.

### 4. Format data and sideload the ROM

In Lineage Recovery:

1. Choose **Factory reset** → **Format data / factory reset**, and confirm. This erases internal storage.
2. Return to the main menu and choose **Apply update** → **Apply from ADB**.
3. On the computer, sideload the ROM ZIP:

   ```sh
   adb sideload "ROM_ZIP_FILENAME.zip"
   ```

4. If you want Google Apps, obtain an Android 17 `arm64` add-on from its publisher and sideload it now, before the first system boot. Google Apps are not included in this ROM.
5. In recovery, choose **Reboot system now**. The first boot can take several minutes.

## Updating an existing install

For an existing Panther ROM install, back up important data. The built-in Updater can check the project's online feed when connected, or import a ZIP already on the phone for an offline update.

### Online update

Open **System updates** and check for updates. An offered weekly build is labeled **ALPHA PRE-RELEASE (UNTESTED)**; compilation is not the same as device testing. Read the corresponding GitHub release notes before installing. The feed advertises the latest candidate only. Routine updates **DO NOT** require a factory reset.

### Offline update from a ZIP

1. Open **System updates**.
2. Choose **Install local update**.
3. Select the ROM ZIP and wait for the Updater to import and verify it.
4. Select the imported update and follow the on-screen installation steps. Reboot when prompted.

This local ZIP import does not require an internet connection. Do not select a package for a different device or build.

### Recovery and older builds

The Updater blocks downgrades by default. Older ZIPs remain on GitHub, but there is no in-app downgrade button, and installing an older build over a newer one is not supported or tested. If recovery or a return to stock is needed, follow the current official Google factory-image instructions for `panther`; this may erase all data. Do not switch slots manually or mix boot, kernel, or firmware images from different releases. Keep a separate backup and do not rely on an older release as a guaranteed rollback.

If an expected update is not offered, do not bypass the Updater's compatibility checks. Use the local ZIP option only for a compatible, non-older Panther build, or ask in the [issue tracker](https://github.com/lineage-panther/panther-release-24.0/issues/new/choose) for release-specific guidance.
