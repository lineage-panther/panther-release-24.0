# Install Panther ROM 24.0 alpha

These are unofficial instructions for the Pixel 7 (`panther`) and the release linked below. Read the full guide before starting. The owner tested the clean-install procedure on one Pixel 7 after installing and booting official Google Android 17 stock firmware. Other devices, firmware versions, and installation paths have not been verified.

The release ZIP identifies itself as Android build `CP2A.260705.006` (`google/panther/panther:17/CP2A.260705.006/15641320:user/release-keys`) with security patch level `2026-10-01`. This is the ROM build ID, not the required starting stock firmware version or the bootloader/baseband version.

Installing this ROM is at your own risk. Back up anything important first. Unlocking the bootloader **WILL** erase user data. Keep the bootloader unlocked after installation; **DO NOT** relock it while running this unofficial build.

## Clean install

### 1. Prepare the phone and computer

- Confirm the device is a Google Pixel 7 (`panther`).
- Install Android SDK Platform-Tools (`adb` and `fastboot`) on the computer and use a reliable USB cable.
- Before flashing, update to and boot the latest official Google Android 17 stock firmware for Pixel 7 (`panther`), or at minimum the release-tested Google build `CP2A.260605.016` or newer. Do not treat an Android 17 custom ROM as proof that the required stock firmware is installed. This stock baseline is a prerequisite; the ROM's OTA payload may replace firmware partitions during installation, as explained below.
- Remove Google accounts from the phone before unlocking to avoid Factory Reset Protection problems.
- Download `boot.img`, `dtbo.img`, `vendor_boot.img`, the ROM ZIP, and its matching `.sha256sum` file from the [24.0 alpha release](https://github.com/lineage-panther/panther-release-24.0/releases/tag/24.0-alpha-20261016). Keep all files together.
- Verify the ROM ZIP before continuing:

  ```sh
  sha256sum -c lineage-24.0-20261016-UNOFFICIAL-panther.zip.sha256sum
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

Open a terminal in the folder containing the three `.img` files. Confirm `fastboot devices` lists the phone, then run:

```sh
fastboot flash boot boot.img
fastboot flash dtbo dtbo.img
fastboot flash vendor_boot vendor_boot.img
fastboot reboot recovery
```

If `fastboot reboot recovery` is not supported by your bootloader, reboot to the bootloader and use the volume and power buttons to select **Recovery mode**.

**OTA payload and firmware note:** The ROM ZIP contains a full A/B OTA payload. Its `payload.bin` includes partition updates for `vendor_kernel_boot`, `vendor_boot`, `dtbo`, `init_boot`, `vbmeta` variants, and firmware components such as bootloader and modem partitions. These are not all separate release downloads: recovery applies the images embedded in the payload according to its OTA/slot metadata. In particular, do not assume that installing the latest stock firmware first means the installed ROM will keep those exact bootloader or baseband versions. The maintainer reports that the installed alpha's bootloader and baseband were older than Google's October stock release.

The maintainer's tested flow did not manually flash a separate `vendor_kernel_boot.img`; the ROM ZIP applies its own copy during sideload. Do not mix in standalone images or firmware from another build, and do not manually switch slots as a troubleshooting step. This unofficial procedure differs from the current [upstream LineageOS Panther installation guide](https://wiki.lineageos.org/devices/panther/install/), which describes flashing a separate `vendor_kernel_boot.img`. The procedure here has only been tested on the maintainer's Pixel 7.

### 4. Format data and sideload the ROM

In Lineage Recovery:

1. Choose **Factory reset** → **Format data / factory reset**, and confirm. This erases internal storage.
2. Return to the main menu and choose **Apply update** → **Apply from ADB**.
3. On the computer, sideload the ROM ZIP:

   ```sh
   adb sideload lineage-24.0-20261016-UNOFFICIAL-panther.zip
   ```

4. If you want Google Apps, obtain an Android 17 `arm64` add-on from its publisher and sideload it now, before the first system boot. Google Apps are not included in this release.
5. In recovery, choose **Reboot system now**. The first boot can take several minutes.

## Updating an existing install

For an existing Panther ROM install, back up important data and use the built-in Updater only when it offers a compatible update for this ROM. Follow its on-device instructions and **DO NOT** factory-reset for a routine update. The release page provides a downloadable ZIP but does not guarantee that an OTA feed is configured or that this release will appear automatically in Updater. If it is not offered, do not flash images or use clean-install steps as an upgrade procedure; ask in the [issue tracker](https://github.com/lineage-panther/panther-release-24.0/issues/new/choose) for release-specific upgrade guidance.
