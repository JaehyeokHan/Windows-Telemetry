# ZLIB decompressor
# revised 2018. 01. 17.
# Jeahyeok Han (one01h@korea.ac.kr)
# python 2.7

import os
import sys
import base64, zlib
import bz2


def decode_base64_and_inflate( b64string ):
    decoded_data = base64.b64decode( b64string )
    return zlib.decompress( decoded_data , -15)

def deflate_and_base64_encode( string_val ):
    zlibbed_str = zlib.compress( string_val )
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode( compressed_string )


### file ###
#path = sys.argv[1]
path = "D:\\1. Research\\55. Windows Telemetry\\_on work\\code\\1"

size = os.path.getsize(path)
rf = os.open(path, os.O_BINARY)
buf = os.read(rf, size)
os.close(rf)

'''
#decode_base64
print buf
print ""
print buf[20:-4]
print ""
decoded = base64.b64decode( buf )
print decoded

### deflate


zlibbed_str = zlib.compress( buf )
compressed = zlibbed_str[2:-4]
print zlibbed_str[0:2].encode("hex")
print zlibbed_str[-4:].encode("hex")
wf = os.open(path+"_deflated", os.O_CREAT|os.O_RDWR)
os.write(wf, )
os.close(wf)
'''


### inflate

decompressed = zlib.decompress(buf , -zlib.MAX_WBITS)
wf = os.open(path+"_inflated", os.O_CREAT|os.O_RDWR)
os.write(wf, decompressed)
os.close(wf)


# Signature
# 0x789C , 0x78DA , 0x7801
