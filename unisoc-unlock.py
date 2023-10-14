#!/usr/bin/env python3

import sys
from adb import fastboot, usb_exceptions

def info_cb(s):
    print(f'info_cb: {s}')

class OemIdToken:
    def __init__(self):
        self.n = 0
        self.id = None

    # Gets passed a FastbootMessage object
    def __call__(self, fb_msg):
        if self.n == 1 and self.id == None and fb_msg.header == b'INFO':
            self.id = fb_msg.message.decode('utf-8').strip()

        self.n += 1

def main():
    try:
        dev = fastboot.FastbootCommands()
        dev.ConnectDevice()
    except usb_exceptions.DeviceNotFoundError as e:
        print('No device found: {}'.format(e), file=sys.stderr)
        sys.exit(1)
    except usb_exceptions.CommonUsbError as e:
        print('Could not connect to device: {}'.format(e), file=sys.stderr)
        sys.exit(1)

    oem_id = OemIdToken()
    try:
        dev.Oem('get_identifier_token', info_cb=oem_id)
    except Exception as e:
        print(f'Fastboot error {str(e)}')
        sys.exit(1)

    print(oem_id.id)
    dev.Close()


if __name__ == '__main__':
    main()

