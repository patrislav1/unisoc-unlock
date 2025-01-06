# unisoc-unlock

This is a tool to lock/unlock a Unisoc / Spreadtrum (SPD) Android bootloader using its Identifier Token.

It is a port of a WebUSB based tool ([[0]](#references), original [[1]](#references)) to Python. The WebUSB based tool does not work on Linux for some reason.
There is also a custom fastboot binary in circulation [[2]](#references) which implements a custom command for unlocking the bootloader.
`unisoc-unlock` implements the same functionality, but without resorting to a custom fastboot binary. Since it is a pure Python solution it should be able to run on any platform running Python.

## Disclaimer

I could only test this tool with a **Unisoc T618** (on a Anbernic RG405M). The leaked key `rsa4096_vbmeta.pem` may or may not work with other Unisoc chipsets. YMMV.

If you receive a `FastbootRemoteFailure` and/or error messages such as `Unlock bootloader fail`, check the model of your Unisoc chipset and please don't open an issue
if your chipset is not the above mentioned T618. Since I don't have any other Unisoc based device, I have no way of porting this tool to other chipsets. Presumably
they have a different bootloader key and there is no way to make this tool work until that key is leaked as well.

TL;DR: *please don't create issues related to other Unisoc chipsets than the T618*

If you manage to make this tool work on other chipsets, feel free to open a PR.

## python-adb

`unisoc-unlock` is implemented with python-adb [[3]](#references). Since python-adb is abandoned and
requires some tweaking to work with the Unisoc, it is not referenced as dependency, but bundled instead.

## Installation

Install with pip:
```bash
pip3 install unisoc-unlock
```

## Usage

```
usage: unisoc_unlock [-h] [--version] [command]

Lock/Unlock tool for Spreadtrum/Unisoc bootloader

positional arguments:
  command     Command (lock|unlock), default=unlock

options:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
```

* Reboot device into fastboot mode
```
adb reboot bootloader
```

* Wait for 'fastboot mode' to show up on the device screen

* Run the python script
```
python3 -m unisoc_unlock unlock  # To unlock the bootloader
python3 -m unisoc_unlock lock    # To re-lock the bootloader
```

* Confirm unlocking on the device

  Note: on the RG405M, the text on the device screen will ask for 'volume down' button to confirm unlock,
  but the home/back button has to be pressed instead!

## Troubleshooting

### Permission issues (`LIBUSB_ERROR_ACCESS` or similar)

Use one of these workarounds:

* Install udev rules to make the fastboot device user-accessible
* If that is not an option, find the fastboot device file with `lsusb` and `chmod a+rw` it to make it world accessible
* If that also doesn't work, run unisoc-unlock as root

### `FastbootRemoteFailure`, `Unlock bootloader fail` etc.

Your device is probably not supported. See also [Disclaimer](#disclaimer)

## References

[0] https://github.com/turtleletortue/turtleletortue.github.io

[1] https://github.com/unisoc-android/unisoc-android.github.io

[2] https://www.hovatek.com/forum/thread-32287.html

[3] https://github.com/google/python-adb
