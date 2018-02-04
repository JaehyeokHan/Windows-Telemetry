# -*- coding: cp949 -*-

# Time converter
# revised 2018. 01. 22.
# Jeahyeok Han (one01h@korea.ac.kr)
# python 2.7

import os
import sys
import datetime, time


# covert binary data(little-endian)to intiger
def strLT2int(t_str) :
    x = 0
    for i in range(len(t_str)-1, -1, -1):
        #(DBG) print i, t_str[i].encode("hex"), x
        x = x*16*16 + int(t_str[i].encode("hex"), 16)
    return x


def allfiles(path):
    res = []

    for root, dirs, files in os.walk(path):
        rootpath = os.path.join(os.path.abspath(path), root)

        for file in files:
            filepath = os.path.join(rootpath, file)
            fname, ext = os.path.splitext(filepath)
            if ext == ".rbs" : # append only rbs file
                res.append(filepath)

    return res

DirPath = "D:\\1. Research\\55. Windows Telemetry\\_on work\\rbs_file_samples"
files = allfiles(DirPath)
i=0

# file data read
for n in range(0, len(files)) :
    i += 1
    rf = os.open(files[n], os.O_BINARY)
    buf = os.read(rf, 53)
    os.close(rf)
    print n

    #print buf[:8]
    
    t = strLT2int(buf[8:16])
    d = datetime.datetime.fromtimestamp(float(t)/float(100000000))
    print d.strftime('%Y-%m-%d %H:%M:%S')
    d.fromordinal

    if i == 3 : break

    print ''
    
