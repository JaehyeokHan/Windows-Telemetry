# -*- coding: cp949 -*-

# rbs parser

# 2018. 01. 15
# Jeahyeok Han (one01h@korea.ac.kr)
# python 2.7

import os
import sys

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
print len(files)

f = open("headers.csv", 'w')

# file data read
for n in range(0, len(files)) :
    rf = os.open(files[n], os.O_BINARY)
    buf = os.read(rf, 53)
    os.close(rf)

    print n
    f.write(str(n) + ", ")
    
    #print files[n],
    f.write(files[n] + ", ")

    filesize = os.path.getsize(files[n])
    f.write(str(filesize) + ", ")
    
    #print buf[:8],
    f.write(buf[:8] + ", ")
    
    for i in buf[8:] :
        #print i.encode("hex"),
        f.write(i.encode("hex") + ", ")

    #print ''
    f.write('\n')         

f.close()
