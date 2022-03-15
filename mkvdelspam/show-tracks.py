#!/usr/bin/python3


try:
    from pymediainfo import MediaInfo
    flag_pymediainfo = True
except:
    #print("NO pymediainfo ")
    flag_pymediainfo = False


import subprocess
import sys
import os
import re


n = len(sys.argv)
if len(sys.argv) < 2:
    exit()

mediafile = sys.argv[1]



if flag_pymediainfo:
    media_info = MediaInfo.parse(mediafile)

    command = []
    audio = 0
    subs = 0

    print(mediafile)
    for track in media_info.tracks:

        if track.track_type == "Video":
            print("Bit rate: {t.bit_rate}, Frame rate: {t.frame_rate}, "
                "Format: {t.format}".format(t=track)
            )
        elif track.track_type == "Audio":
            audio += 1
            print("Audio",track.track_type, track.track_id, track.title, track.language)
        elif track.track_type == "Text":
            subs += 1
            print("Audio",track.track_type, track.track_id, track.title, track.language)

    print("")
    print("")
else:

    print("*" *80)
    print("*" *80)

    proc = subprocess.Popen('mediainfo "{mediafile}"'.format(mediafile=mediafile), shell=True, stdout=subprocess.PIPE)

    command = []
    audio = 0
    subs = 0

    print(mediafile)
    for line in proc.stdout:
        #print(line)
        if re.search('^Audio', line.decode()):
            print(line.decode().replace('\n','') )
        if re.search('^Text', line.decode()):
            print(line.decode().replace('\n','') )
        if re.search('^Title', line.decode()):
            print(line.decode().replace('\n','') )
        if re.search('^Language', line.decode()):
            print(line.decode().replace('\n','') )

    print("\n")



