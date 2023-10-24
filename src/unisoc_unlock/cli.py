#!/usr/bin/env python3

import os
import sys
from .bundled_adb import fastboot, usb_exceptions
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import base64
import io
import argparse
import importlib.metadata


class OemIdToken:
    # Callback object for fastboot 'get_identifier_token' command

    def __init__(self):
        self.n = 0
        self.id = None

    # Gets passed a FastbootMessage object
    def __call__(self, fb_msg):
        if self.n == 1 and self.id == None and fb_msg.header == b'INFO':
            self.id = fb_msg.message.decode('utf-8').strip()

        self.n += 1


class BootloaderCmd:
    def sign_token(self, tok, key_file):
        priv_key = RSA.importKey(open(key_file).read())
        h = SHA256.new(tok)
        signature = PKCS1_v1_5.new(priv_key).sign(h)
        return signature

    def prepare(self):
        try:
            self.dev = fastboot.FastbootCommands()
            self.dev.ConnectDevice()
        except usb_exceptions.DeviceNotFoundError as e:
            print('No device found: {}'.format(e), file=sys.stderr)
            sys.exit(1)
        except usb_exceptions.CommonUsbError as e:
            print('Could not connect to device: {}'.format(e), file=sys.stderr)
            sys.exit(1)

        oem_id = OemIdToken()
        try:
            self.dev.Oem('get_identifier_token', info_cb=oem_id)
        except Exception as e:
            print(f'Fastboot error: {str(e)}')
            sys.exit(1)

        print(f'OEM ID: {oem_id.id}')
        id = oem_id.id.ljust(2*64, '0')
        id_raw = base64.b16decode(id, casefold=True)
        pemfile = os.path.join(
            os.path.dirname(__file__),
            'rsa4096_vbmeta.pem'
        )
        sgn = self.sign_token(id_raw, pemfile)

        print('Download signature')
        self.dev.Download(io.BytesIO(sgn), source_len=len(sgn))


class BootloaderUnlock(BootloaderCmd):
    def __call__(self):
        print('Preparing to unlock the bootloader')
        self.prepare()

        print('Unlock bootloader, pls follow instructions on device screen')
        self.dev._SimpleCommand(
            b'flashing unlock_bootloader', timeout_ms=60*1000)

        print('Bootloader unlocked.')
        self.dev.Close()


class BootloaderLock(BootloaderCmd):
    def __call__(self):
        print('Preparing to lock the bootloader')
        self.prepare()

        print('Lock bootloader, pls follow instructions on device screen')
        self.dev._SimpleCommand(
            b'flashing lock_bootloader', timeout_ms=60*1000)

        print('Bootloader locked.')
        self.dev.Close()


def main():
    parser = argparse.ArgumentParser(
        description='Lock/Unlock tool for Spreadtrum/Unisoc bootloader'
    )
    parser.add_argument('command',
                        type=str,
                        nargs='?',
                        help='Command (lock|unlock), default=unlock'
                        )
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' +
                        importlib.metadata.version('unisoc-unlock')
                        )

    args = parser.parse_args()

    if args.command == 'lock':
        cmd = BootloaderLock()
    elif args.command in ['unlock', None]:
        cmd = BootloaderUnlock()
    else:
        print(f'Unknown command {args.command}', file=sys.stderr)
        sys.exit(1)

    cmd()


if __name__ == '__main__':
    main()
