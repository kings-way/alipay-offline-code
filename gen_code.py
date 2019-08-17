#!/usr/bin/env python3

import sys
import time
import pyotp
import base64

INDEX = "0123456789"
SEED_BYTES = [0,1,2,3,4,5,6,7,8,9]  # shall be 40 bytes long



# Notes:
# Format: '28' + encrypt(INDEX) + nativeOTP(bytes SEED, timestamp/3, 6)
# 1. nativeOTP exists in libAPSE.so, generate standard HOTP code
# 2. INDEX and SEED can be found encrypted in shared_prefs/MODE_*_SETTING_FILE.xml, please use `grep -ir SEEDSG .`
# 3. SEED has an expiration date, and will not usable after account logout
# 4. New SEED seems only has 20 bytes changed, left 20 bytes unchanged
# 5. INDEX seems will not change as SEED

def base32_seed():
    global SEED_BYTES
    tmp = []
    for i in SEED_BYTES:
        tmp.append(i&0xff)
    SEED_BYTES = base64.b32encode(bytearray(tmp))
    # bytes() works differently between Py2/Py3, bytearray() works fine

def encrypt_Index(OTP):
    ret = []
    for i in range(len(INDEX)):
        ret.append(str(((ord(INDEX[i]) - 48) * 107 + ord(OTP[i%6]) - 48) % 10))
    return ''.join(ret)

def get_OTP():
    hotp = pyotp.HOTP(SEED_BYTES)
    timestamp = int(time.time() / 3)
    return hotp.at(timestamp)


base32_seed()

if __name__ == '__main__':
    OTP = get_OTP()
    index = encrypt_Index(OTP)
    result = "28" + index + OTP
    sys.stdout.write(result)
