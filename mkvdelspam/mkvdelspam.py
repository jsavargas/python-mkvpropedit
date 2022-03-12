#!/usr/bin/python3

from pprint import pprint
from pymediainfo import MediaInfo

import sys
import os



n = len(sys.argv)
if len(sys.argv) < 2:
    exit()

mediafile = sys.argv[1]
print(mediafile)

print("")
print("")

media_info = MediaInfo.parse(mediafile)

command = []
audio = 0
subs = 0

for track in media_info.tracks:

    if track.track_type == "Video":
        print("Bit rate: {t.bit_rate}, Frame rate: {t.frame_rate}, "
              "Format: {t.format}".format(t=track)
        )
    elif track.track_type == "Audio":
        audio += 1
        print("Audio",track.track_type, track.track_id, track.title, track.language)

        command.append(f'--edit track:a{audio} --delete name ')

    elif track.track_type == "Text":
        subs += 1
        print("Audio",track.track_type, track.track_id, track.title, track.language)
        command.append(f'--edit track:s{subs} --delete name ')
command.append(f' --edit track:v1 --delete name ')

print("")
print("")
#print(command)

mkvpropedit = "mkvpropedit --tags all: --delete title --delete-attachment mime-type:image/jpeg --delete-attachment 1 --edit track:v1 --delete name {} '{}'".format("".join(command),mediafile)
print(mkvpropedit)
print(os.system(mkvpropedit))


print("")
#print(os.system(f"mediainfo {mediafile}"))


