#!/usr/bin/env python3

import sys
from adb import fastboot, usb_exceptions
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
import base64

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


def sign_token(tok, key_file):
    priv_key = RSA.importKey(open(key_file).read())
    h = SHA256.new(tok)
    signature = PKCS1_v1_5.new(priv_key).sign(h)
    return signature

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

    id = oem_id.id.ljust(2*64, '0')
    print(id)
    dev.Close()


if __name__ == '__main__':
    oem_id = '52473430354d3032333736373036' 
    id = oem_id.ljust(2*64, '0')
    id_raw = base64.b16decode(id, casefold=True)
    # print(id_raw)
    sgn = sign_token(id_raw, 'rsa4096_vbmeta.pem')
    open('sig.bin', 'wb').write(sgn)

