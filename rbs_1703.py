# -*- coding: cp949 -*-

# rbs parser for version 1703 rbs files

# 2018. 01. 17
# Jeahyeok Han (one01h@korea.ac.kr)
# python 2.7

import os
import sys
import struct
import zlib, base64
import datetime, time

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

    print "ftype : " + fh_buf[40:52].encode("hex")
    print "ser.  : " + fh_buf[52:53].encode("hex")


# Print log block header structure
def LogBlockPrint(lbh_buf) :
    nblock = 0
    startOffset_logblock = 53 # file header size
        
    while(True) :
        nblock += 1
        if (lbh_buf[startOffset_logblock] == '\x00' and lbh_buf[startOffset_logblock+1] == '\x00'):
            print "[Break Point #1]"
            break
        print nblock, hex(startOffset_logblock)
        
        print "log ID: " + lbh_buf[startOffset_logblock:startOffset_logblock+12].encode("hex")
        
        block_idx     = strLT2int(lbh_buf[startOffset_logblock+12:startOffset_logblock+16])
        encoded_size  = strLT2int(lbh_buf[startOffset_logblock+16:startOffset_logblock+20])
        
        print "blkidx: " + str(block_idx)
        print "endsiz: " + str(encoded_size)
        
        print "uknow1: " + lbh_buf[startOffset_logblock+20:startOffset_logblock+24].encode("hex")
        
        deflated_size = strLT2int(lbh_buf[startOffset_logblock+24:startOffset_logblock+28])
        print "dflsiz: " + str(deflated_size)
        
        print "uknow2: " + lbh_buf[startOffset_logblock+28:startOffset_logblock+34].encode("hex")

        # Base 64 decode
        '''
        tmp1 = lbh_buf[startOffset_logblock + 34:startOffset_logblock + 34 + encoded_size]
        decoded = base64.b64decode( tmp1 )
        print decoded
        '''

        # Inflate
        '''
        tmp2 = lbh_buf[startOffset_logblock + 34 + encoded_size:startOffset_logblock + 34 + encoded_size+deflated_size]
        inflated = deflateData(tmp2)
        print inflated
        '''

        startOffset_logblock = startOffset_logblock + 34 + encoded_size + deflated_size
        if (len(lbh_buf) < startOffset_logblock) :
            print "[Break Point #2]"
            break
        print "-----------------------"


# Save log block header information
def SaveLogBlockInfo(lbh_buf, fsize) :
    OutputFileName = "LogBlocks_Info_1703.csv"
    print len(lbh_buf)
    
    nblock = 0
    startOffset_logblock = 53 # file header size

    f = open(OutputFileName, 'w')
    f.write("#, Telemetry log ID, Block index, Encoded size, unknown1, Deflated size, unknown2, start_offset\n")
    
    while(True) :
        nblock += 1
        if (lbh_buf[startOffset_logblock] == '\x00' and lbh_buf[startOffset_logblock+1] == '\x00'): break
        
        f.write(str(nblock)+",")
        f.write(lbh_buf[startOffset_logblock:startOffset_logblock+12].encode("hex")+",")
        
        block_idx     = strLT2int(lbh_buf[startOffset_logblock+12:startOffset_logblock+16])
        encoded_size  = strLT2int(lbh_buf[startOffset_logblock+16:startOffset_logblock+20])
        f.write(str(block_idx)+",")
        f.write(str(encoded_size)+",")

        f.write(lbh_buf[startOffset_logblock+20:startOffset_logblock+24].encode("hex")+",")
        
        deflated_size = strLT2int(lbh_buf[startOffset_logblock+24:startOffset_logblock+28])
        f.write(str(deflated_size)+",")
        
        f.write(lbh_buf[startOffset_logblock+28:startOffset_logblock+34].encode("hex")+",")
        f.write(str(startOffset_logblock)+",")
        
        startOffset_logblock = startOffset_logblock + 34 + encoded_size + deflated_size
        if fsize < startOffset_logblock : break
        
        print startOffset_logblock

    f.close()


# deflate
def deflateData(d_buf):
    return zlib.decompress(d_buf , -zlib.MAX_WBITS)    


#######################################################

# main function

FilePath = "D:\\1. Research\\55. Windows Telemetry\\_on work\\code\\test\\Events_Normal.rbs"

# file open & data read
filesize = os.path.getsize(FilePath)

rf = os.open(FilePath, os.O_BINARY)
buf = os.read(rf, filesize)
os.close(rf)



# ***** file header *****
print " [ File header ]"
FileHeaderPrint(buf)
print "========================\n"



# ***** log block *****

print " [ Log block header ]"
LogBlockPrint(buf)
#SaveLogBlockInfo(buf, filesize)




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
