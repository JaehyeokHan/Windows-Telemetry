# -*- coding: cp949 -*-

# JSON parser
# revised 2018. 01. 18.
# Jeahyeok Han (one01h@korea.ac.kr)
# python 2.7

import os
import sys
import json
from pprint import pprint

def json_dataView(jdata, key) :
    try :
        print key, data[key]

    except :
        print "json key error :", key
        


#path = sys.argv[1]
path = "D:\\1. Research\\55. Windows Telemetry\\_on work\\rbs_file_samples\\170811_박송이_15063_Normal\\3"

size = os.path.getsize(path)
rf = os.open(path, os.O_BINARY)
buf = os.read(rf, size)
os.close(rf)

filesize = os.path.getsize(path)

sbuf = buf.split("\n")

print len(sbuf)
njson = 0

for json_chunk in sbuf :
    njson += 1
    try :
        data = json.loads(json_chunk)
        
        print "ver   :", data["ver"]
        print "name  :", data["name"]
        print "time  :", data["time"]
        print "epoch :", data["epoch"]
        print "seqNum:", data["seqNum"]
        print "flags :", data["flags"]
        print "os    :", data["os"]
        print "osVer :", data["osVer"]
        json_dataView(data, "appId")
        json_dataView(data, "appVer")
        print "ext   :", data["ext"]
        
        #print "ext   :", data["ext"]["utc"]
        #print "app   :", data["ext"]["app"]
        #print "os    :", data["ext"]["os"]
        #print "device:", data["ext"]["device"]
        #print "user  :", data["ext"]["user"]
        #print "data  :", data["data"]
        print "--------------------------------"
        
    except :
        if njson == len(sbuf) :
            continue
        else :
            print "[json error : " + str(njson) + " of " + str(len(sbuf)) + "]"
            sys.exit(1)

