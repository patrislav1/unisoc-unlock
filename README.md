# unisoc-unlock

This is a tool to lock/unlock a Unisoc / Spreadtrum (SPD) Android bootloader using its Identifier Token.

It is a port of a WebUSB based tool [1] to Python. The WebUSB based tool does not work on Linux for some reason.
There is also a custom fastboot binary in circulation [2] which implements a custom command for unlocking the bootloader.
`unisoc-unlock` implements the same functionality, but without resorting to a custom fastboot binary. Since it is a pure Python solution it should be able to run on any platform running Python.

## python-adb

`unisoc-unlock` is implemented with python-adb [3]. Since python-adb is abandoned and
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

## References

[1] https://github.com/turtleletortue/turtleletortue.github.io

[2] https://www.hovatek.com/forum/thread-32287.html

[3] https://github.com/google/python-adb
