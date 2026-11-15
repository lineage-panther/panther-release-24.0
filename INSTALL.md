# Install Panther ROM 24.0 alpha

These are unofficial instructions for the Pixel 7 (`panther`) and the release linked below. Read the full guide before starting. The owner tested the clean-install procedure on one Pixel 7 after installing and booting official Google Android 17 stock firmware. Other devices, firmware versions, and installation paths have not been verified.

Installing this ROM is at your own risk. Back up anything important first. Unlocking the bootloader **WILL** erase user data. Keep the bootloader unlocked after installation; **DO NOT** relock it while running this unofficial build.

## Clean install

### 1. Prepare the phone and computer

- Confirm the device is a Google Pixel 7 (`panther`).
- Install Android SDK Platform-Tools (`adb` and `fastboot`) on the computer and use a reliable USB cable.
- Update to and boot Google's official Android 17 stock firmware, build `CP2A.260605.016` or newer. The ROM was built against Android 17 firmware; **DO NOT** downgrade firmware for this install.
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

**Important partition note:** This release does not include `vendor_kernel_boot.img`. The owner-tested install left the `vendor_kernel_boot` partition from the official Android 17 stock firmware in place. Do not substitute an image from a different release or firmware. The current [upstream LineageOS Panther installation guide](https://wiki.lineageos.org/devices/panther/install/) includes an additional `vendor_kernel_boot.img` flash step; that is not the tested procedure documented here. If you are not on the specified Google Android 17 stock firmware, stop rather than guessing which partition image to use.

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
