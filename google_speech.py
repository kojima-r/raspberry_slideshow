#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import urllib2
import json
import commands

apikey = "AIzaSyAAw0dvpQixKKnR9A1TROk5iah2BmMrEVE"


def stt_google_wav(filename):
    base, ext = os.path.splitext(filename)
    sox_command_template = "sox %s -r 16000 %s.flac"
    command = sox_command_template % (filename, base)
    status, output = commands.getstatusoutput(command)
    if status:
        print output
        return
    f = open(base + '.flac', 'rb')
    flac_cont = f.read()
    f.close()

    googl_speech_url = 'https://www.google.com/speech-api/v2/recognize?xjerr=1&client=chromium&lang=ja-JP&maxresults=10&pfilter=0&xjerr=1&key=' + apikey
    hrs = {
        "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7",
        'Content-type': 'audio/x-flac; rate=16000'
    }
    req = urllib2.Request(googl_speech_url, data=flac_cont, headers=hrs)
    p = urllib2.urlopen(req)

    raw = p.read()
    print 'raw: ', raw
    p.close()

    jsonunits = raw.split(os.linesep)
    res = ""

    for unit in jsonunits:
        if not unit:
            continue
        obj = json.loads(unit)
        alternatives = obj['result']

        if len(alternatives) > 0:
            breakflag = False
            for obj in alternatives:
                results = obj['alternative']
                for result in results:
                    res = result['transcript']
                    breakflag = True
                    break
                if breakflag:
                    break
    return res

if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('-o', '--outputfile', type=str, default="transcript.txt")
    parser.add_argument('inputfile',nargs=None ,type=str)
    args = parser.parse_args()
    
    result=stt_google_wav(args.inputfile)
    print "-----"
    print result
    fp=open(args.outputfile,"w")
    fp.write(result.encode('utf-8'))
    fp.close
