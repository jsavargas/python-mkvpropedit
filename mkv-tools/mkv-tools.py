#!/usr/bin/python3


import os
import re
import sys
import argparse
import subprocess



def parse_args():
    parser = argparse.ArgumentParser(description="MKV Tools - Delete Spam.")
    parser.add_argument('-f', '--file', type=str, required=True, help='file mkv to process')
    parser.add_argument('--show_video_tracks', type=bool, help='the id of destination. Team Drive id or publicly shared folder id')
    parser.add_argument('--show_tracks', action='store_true', help='the id of destination. Team Drive id or publicly shared folder id')
    parser.add_argument('--show_movie_name', action='store_true', help='the id of destination. Team Drive id or publicly shared folder id')
    parser.add_argument('--show_mediainfo', action='store_true', help='the id of destination. Team Drive id or publicly shared folder id')
    parser.add_argument('--show_fullmediainfo', action='store_true', help='the id of destination. Team Drive id or publicly shared folder id')
    parser.add_argument('--pymediainfo', action='store_true', help='the id of destination. Team Drive id or publicly shared folder id')
    



    args = parser.parse_args()
    return args


def ifpymediainfo():

    try:
        from pymediainfo import MediaInfo
        flag_pymediainfo = True
        return True
    except:
        #print("NO pymediainfo ")
        flag_pymediainfo = False
        return False


def tools(args):
    print(args.file)


    if args.pymediainfo and ifpymediainfo():
        print("use pymediainfo")
    else:
        proc = subprocess.Popen('mediainfo "{mediafile}"'.format(mediafile=args.file), shell=True, stdout=subprocess.PIPE)
    
        if args.show_fullmediainfo: 
            mediaInfo = os.system('mediainfo --full "{mediafile}"'.format(mediafile=args.file))
        if args.show_mediainfo: 
            mediaInfo = os.system('mediainfo "{mediafile}"'.format(mediafile=args.file))

        for line in proc.stdout:
            #print(line)
            if re.search('^Movie name', line.decode()):
                if args.show_tracks: print(line.decode().replace('\n','') )
                elif args.show_movie_name: print(line.decode().replace('\n','') )
            
            if re.search('^Audio', line.decode()):
                if args.show_tracks: print(line.decode().replace('\n','') )
            
            if re.search('^Text', line.decode()):
                if args.show_tracks: print(line.decode().replace('\n','') )
            
            if re.search('^Title', line.decode()):
                if args.show_tracks: print(line.decode().replace('\n','') )
            
            if re.search('^Language', line.decode()):
                if args.show_tracks:print(line.decode().replace('\n','') )





    return ""
    exit()

def old():
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

        print("")
        print("")



if __name__ == '__main__':

    try:
        args = parse_args()
        #print(args)

        tools(args)

    except:
        pass

