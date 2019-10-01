### Generate real working Alipay offline code

---

#### 1. Intro
Alipay can generate offline code for people to use, and this feature is based on standard [HOTP](https://tools.ietf.org/html/rfc4226).
After some reverse engineering work, we are able to reproduce the six-num code anywhere, only if you get your own 'SEED'.

(The frida script here is known to works with [Alipay_10.1.62.5549](https://www.apkmirror.com/apk/alipay-com/alipay/alipay-10-1-62-5549-release/alipay-10-1-62-5549-android-apk-download/))


#### 2. How to run

* 1.Get your device rooted, and run [frida-server](https://github.com/frida/frida/releases) with root priv.

* 2.Run `python3 hook.py`, and get your own "INDEX" and "SEED" value.

* 3.Set the `INDEX` and `SEED` value in gen_code.py

* 4.Run `python gen_code.py | qrencode -t utf8`, and enjoy it!

#### 3. Tech Notes

* The string format: `'28' + encrypt(INDEX) + nativeOTP(bytes SEED, timestamp/3, 6)`

* `nativeOTP()` exists in libAPSE.so, generate standard HOTP code

* `INDEX` and `SEED` can be found encrypted in `shared_prefs/MODE_*_SETTING_FILE.xml`, please use `grep -ir SEEDSG .`

* `SEED` has an expiration date(about 30days), and will be revoked right after app logout

* When requesting new `SEED`, it seems only has 20 bytes changed, left 20 bytes unchanged

* `INDEX` seems will not change as `SEED` renew

#### 4. Refer

* https://tools.ietf.org/html/rfc4226

* https://pypi.org/project/pyotp/ 

* https://github.com/frida/frida/releases
