# -*- coding: cp949 -*-

# rbs parser for version 1511 rbs files

# 2018. 01. 18
# Jeahyeok Han (one01h@korea.ac.kr)
# python 2.7

import os
import sys
import struct
import datetime, time
import zlib
import base64

# ************* functions  *************

# covert binary data(little-endian)to intiger
def strLT2int(t_str) :
    x = 0
    for i in range(len(t_str)-1, -1, -1):
        #(DBG) print i, t_str[i].encode("hex"), x
        x = x*16*16 + int(t_str[i].encode("hex"), 16)
    return x

# Print file header structure
def FileHeaderPrint(fh_buf) :
    print fh_buf[:8]
    print "time  : " + fh_buf[8:16].encode("hex")

    offset1 = strLT2int(fh_buf[16:20])
    offset2 = strLT2int(fh_buf[20:24])
    print "offst1: " + str(offset1)
    print "offst2: " + str(offset2)

    size1 = strLT2int(fh_buf[24:28])
    size2 = strLT2int(fh_buf[28:32])
    print "size1 : " + str(size1)
    print "size2 : " + str(size2)

    index1 = strLT2int(fh_buf[32:36])
    index2 = strLT2int(fh_buf[36:40])
    print "index1: " + str(index1)
    print "index2: " + str(index2)

    print "ser.  : " + fh_buf[40:42].encode("hex")


# Print log block header structure
def LogBlockPrint(lbh_buf) :
    nblock = 0
    startOffset_logblock = 42
        
    while(True) :
        nblock += 1
        if (lbh_buf[startOffset_logblock] == '\x00' and lbh_buf[startOffset_logblock+1] == '\x00'): break
        print "log ID: " + lbh_buf[startOffset_logblock:startOffset_logblock+4].encode("hex")

        block_idx     = strLT2int(lbh_buf[startOffset_logblock+ 4:startOffset_logblock+ 8])
        encoded_size  = strLT2int(lbh_buf[startOffset_logblock+ 8:startOffset_logblock+12])
        deflated_size = strLT2int(lbh_buf[startOffset_logblock+12:startOffset_logblock+16])
        print "blkidx: " + str(block_idx)
        print "endsiz: " + str(encoded_size)
        print "dflsiz: " + str(deflated_size)
        
        print "unknow: " + lbh_buf[startOffset_logblock+16:startOffset_logblock+22].encode("hex")

        startOffset_logblock = startOffset_logblock + 22 + encoded_size + deflated_size
        if len(lbh_buf) < startOffset_logblock : break
        print "-----------------------"


# Save log block header information
def SaveLogBlockInfo(lbh_buf) :
    OutputFileName = "LogBlocks_Info_1511.csv"
    print len(lbh_buf)
    
    nblock = 0
    startOffset_logblock = 42

    f = open(OutputFileName, 'w')
    f.write("#, Telemetry log ID, Block index, Encoded size, Deflated size, unknown, startOffset\n")
    
    while(True) :
        nblock += 1
        if (lbh_buf[startOffset_logblock] == '\x00' and lbh_buf[startOffset_logblock+1] == '\x00' and lbh_buf[startOffset_logblock+2] == '\x00' and lbh_buf[startOffset_logblock+3] == '\x00'):
            print "[Break Point #1]"
            break
        
        f.write(str(nblock)+",")
        f.write(lbh_buf[startOffset_logblock:startOffset_logblock+4].encode("hex")+",")
        
        block_idx     = strLT2int(lbh_buf[startOffset_logblock+ 4:startOffset_logblock+ 8])
        encoded_size  = strLT2int(lbh_buf[startOffset_logblock+ 8:startOffset_logblock+12])
        deflated_size = strLT2int(lbh_buf[startOffset_logblock+12:startOffset_logblock+16])
        
        f.write(str(block_idx)+",")
        f.write(str(encoded_size)+",")
        f.write(str(deflated_size)+",")
        
        f.write(lbh_buf[startOffset_logblock+16:startOffset_logblock+22].encode("hex")+",")
        f.write(str(startOffset_logblock)+"\n")
        
        startOffset_logblock = startOffset_logblock + 22 + encoded_size + deflated_size
        if len(lbh_buf) < startOffset_logblock :
            print "[Break Point #2]"
            break
        print startOffset_logblock


    f.close()


#######################################################

# main function

FilePath = "D:\\1. Research\\55. Windows Telemetry\\_on work\\rbs_file_samples\\1511 ver\\Diagnosis_170424\\events00.rbs"

# file open & data read
filesize = os.path.getsize(FilePath)

rf = os.open(FilePath, os.O_BINARY)
buf = os.read(rf, filesize)
os.close(rf)



# ***** file header *****
print " [ File header ]"
FileHeaderPrint(buf)
print "-----------------------"



# ***** log block *****

print " [ Log block header ]"
#LogBlockPrint(buf)
SaveLogBlockInfo(buf)




'''
file.seek(offset, from_what)
offset: 얼마나 옮길 것인지
from_what: 어디를 기준으로 할 것인지
0: os.SEEK_SET, 파일의 시작
1: os.SEEK_CUR, 현재 위치
2: os.SEEK_END, 파일의 끝


rf = open(enfile, 'r')
data = rf.read();
rf.close();


#encoded=base64.encodestring(txt)
decoded = base64.decodestring(encoded)

wf = open(defile, 'wb')
wf.write(decoded)

#print(decoded)


string = "U29mdHdhcmVcXE1pY3Jvc29mdFxcV2luZG93c1xcQ3VycmVudFZlcnNpb25cXFJ1bg=="


#encoded=base64.encodestring(txt)
decoded = base64.decodestring(string)

print "%s --> %s" %(string, decoded)
'''
