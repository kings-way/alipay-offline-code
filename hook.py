#!/usr/bin/env python3

# this code known to works with Alipay 10.1.62.5549

import sys
import frida

package = 'com.eg.android.AlipayGphone'
session = frida.get_usb_device().attach(package)
def on_message(message, data):
    print(message)

hook_code = '''
Java.perform(function (){
    var class_APSE = Java.use("com.alipay.mobile.security.senative.APSE")
    class_APSE.nativeHOTPSafe.implementation = \
            function(arg4, arg5, arg6, arg8){

            send("SEED bytes:" + JSON.stringify(arg5))
            //send("Timestamp/3:" + arg6)
            //send("HOTP Length:" + arg8)

            var ret = this.nativeHOTPSafe(arg4, arg5, arg6, arg8)
            //send("HOTP Result:" + JSON.stringify(ret.otp))
            return ret
        }
})'''

hook_code2 = '''
Java.perform(function (){
    var class_utils = Java.use("com.alipay.mobile.security.otp.service.utils.GenerateOtpHelper")
    class_utils.b.implementation = \
        function(arg8){
            //send("arg8:" + arg8)
            send("INDEX:" + arg8.substr(2,10))
            var ret = this.b(arg8)
            send("Result:" + JSON.stringify(ret))
            return ret
        }
})'''

script = session.create_script(hook_code)
script2 = session.create_script(hook_code2)
script.on('message', on_message)
script2.on('message', on_message)
script.load()
script2.load()
sys.stdin.read()
