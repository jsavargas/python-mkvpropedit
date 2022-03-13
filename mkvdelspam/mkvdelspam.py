#!/usr/bin/python3


try:
    from pymediainfo import MediaInfo
    flag_pymediainfo = True
except:
    print("NO pymediainfo ")
    flag_pymediainfo = False


import subprocess
import sys
import os
import re


n = len(sys.argv)
if len(sys.argv) < 2:
    exit()

mediafile = sys.argv[1]
print(mediafile)

print("")
print("")


if flag_pymediainfo:
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
    command.append(' --edit track:v1 --delete name ')

    print("")
    print("")
    #print(command)

    mkvpropedit = 'mkvpropedit --tags all: --delete title --delete-attachment mime-type:image/jpeg --delete-attachment 1  {} "{}"'.format("".join(command),mediafile)
    print(mkvpropedit)
    print(os.system(mkvpropedit))


    print("")
    #print(os.system(f"mediainfo {mediafile}"))
else:
    mediaInfo = os.system('mediainfo "{mediafile}"'.format(mediafile=mediafile))
    print("mediaInfo",mediaInfo)

    print("*" *80)
    print("*" *80)

    proc = subprocess.Popen('mediainfo "{mediafile}"'.format(mediafile=mediafile), shell=True, stdout=subprocess.PIPE)

    command = []
    audio = 0
    subs = 0

    for line in proc.stdout:
        #print(line)
        if re.search('^Audio', line.decode()):
            audio += 1
            print(line.decode().replace('\n','') )
            command.append(f'--edit track:a{audio} --delete name ')
            #          command.append(f'--edit track:a{audio} --set name="Español" ')
        if re.search('^Text', line.decode()):
            subs += 1
            print(line.decode().replace('\n','') )
            command.append(f'--edit track:s{subs} --delete name ')
        if re.search('^Title', line.decode()):
            print(line.decode().replace('\n','') )
        if re.search('^Language', line.decode()):
            print(line.decode().replace('\n','') )

    print("\n" *2)


    command.append(' --edit track:v1 --delete name ')
    mkvpropedit = 'mkvpropedit --tags all: --delete title --delete-attachment mime-type:image/jpeg --delete-attachment 1 {} "{}"'.format("".join(command),mediafile)

    print(mkvpropedit)

    print(os.system(mkvpropedit))

