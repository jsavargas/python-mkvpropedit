#!/usr/bin/python3

'''


'''

import os
import re
import sys
import argparse
import subprocess

__version__ = "VERSION 1.0.8"


def parse_args():
    parser = argparse.ArgumentParser(description="MKV Tools - Delete Spam.")
    parser.add_argument('-v','--version', action='version',                    
                    version="%(prog)s " + __version__)

                    
    parser.add_argument('-f', '--file', type=str, required=True, help='file mkv to process')
    
    parser.add_argument('--show_tracks', action='store_true', help='show tracks from mkv')
    parser.add_argument('--show_video_tracks', action='store_true', help='show_video_tracks')
    parser.add_argument('--show_movie_name', action='store_true', help='show movie name tag from mkv')
    parser.add_argument('--show_mediainfo', '--mediainfo', action='store_true', help='Show mediainfo file')
    parser.add_argument('--show_fullmediainfo', '--fullmediainfo', action='store_true', help='Show mediainfo --full file')
    parser.add_argument('--pymediainfo', action='store_true', help='Use pymediainfo')
    
    parser.add_argument('--print_args', action='store_true', help='dev use, print arguments')

    parser.add_argument('-smnf', '--set_moviename_filename', action='store_true', help='Set filename to movie name')
    parser.add_argument('-svtf', '--set_videotitle_filename', action='store_true', help='Set filename to video title')
    
    parser.add_argument('--delete_movie_name', action='store_true', help='delete movie name')
    parser.add_argument('--delete_video_title', action='store_true', help='delete video title')
    parser.add_argument('--delete_attachment', action='store_true', help='delete attachments')

    parser.add_argument('-dtmn', '--delete_text_movie_name', type=str, help='replace text in movie name')
    parser.add_argument('-dtvt', '--delete_text_video_title', type=str, help='replace text in video title') #TODO get video title y replace string
    #parser.add_argument('--replace_movie_name', type=str, help='replace text in movie name')
    #parser.add_argument('--replace_video_title', type=str, help='replace text in video title') #TODO get video title y replace string


    parser.add_argument('--vn', action='store_true', help='Hidde message "requires --apply"')
    parser.add_argument('--apply', action='store_true', help='apply changes')



    args = parser.parse_args()
    return args


def ifpymediainfo():

    try:
        from pymediainfo import MediaInfo
        flag_pymediainfo = True
        return True
    except:
        flag_pymediainfo = False
        return False

def newLine(crlf=1):
    print("\n"*crlf)

def tools(args, finish=False):
    print("="*30)
    print("PROCESS: ",args.file)


    if args.pymediainfo and ifpymediainfo():
        print("use pymediainfo")
    else:
        proc = subprocess.Popen('mediainfo "{mediafile}"'.format(mediafile=args.file), shell=True, stdout=subprocess.PIPE)
    
        if args.show_fullmediainfo: 
            mediaInfo = os.system('mediainfo --full "{mediafile}"'.format(mediafile=args.file))
        if args.show_mediainfo: 
            mediaInfo = os.system('mediainfo "{mediafile}"'.format(mediafile=args.file))

        command = []
        video = 0
        audio = 0
        text = 0
        head = ""
        run = False

        for line in proc.stdout:
            if re.search('^Movie name', line.decode()):
                if args.show_tracks: print(line.decode().replace('\n','') )
                elif args.show_movie_name: print(line.decode().replace('\n','') )
                elif args.delete_text_movie_name: print(line.decode().replace('\n','') )
                if args.delete_text_movie_name:
                    tag_movie_name = line.decode().replace('\n','') 

            
            if re.search('^Video', line.decode()):
                #print("")
                video += 1
                head = line.decode().replace('\n','')
                if args.show_tracks: 
                    print(line.decode().replace('\n','') )

            if re.search('^Audio', line.decode()):
                #print("")
                audio +=1
                head = line.decode().replace('\n','')
                #if args.show_tracks: print(line.decode().replace('\n','') )
            
            if re.search('^Text', line.decode()):
                #print("")
                text +=1
                head = line.decode().replace('\n','')
                #if args.show_tracks: print(line.decode().replace('\n','') )
            
            if re.search('^Title', line.decode()):
                if args.show_tracks: 
                    if text>0:
                        print("{} >> {}".format(head, line.decode().replace('\n','')) )
                    elif audio>0:
                        print("{} >> {}".format(head, line.decode().replace('\n','')) )
                    elif video>0:
                        print("{} >> {}".format(head, line.decode().replace('\n','')) )
                        if args.delete_text_video_title: tag_video_title = line.decode().replace('\n','') 


            if re.search('^Language', line.decode()):
                if args.show_tracks:
                    #print(line.decode().replace('\n','') )
                    if text>0:
                        print("{} >> {}".format(head, line.decode().replace('\n','')) )
                    elif audio>0:
                        print("{} >> {}".format(head, line.decode().replace('\n','')) )
                    elif video>0:
                        print("{} >> {}".format(head, line.decode().replace('\n','')) )


        newLine()
        if finish: 
            print("\n\n")
            return

        if args.set_moviename_filename:
            pattern = re.compile(".mkv", re.IGNORECASE)
            new_name = pattern.sub("", os.path.basename(args.file))

            command.append(' --set title="{}" '.format(new_name))
            run = True

        if args.set_videotitle_filename:
            pattern = re.compile(".mkv", re.IGNORECASE)
            new_name = pattern.sub("", os.path.basename(args.file))

            command.append(' --edit track:v1 --set name="{}" '.format(new_name))
            run = True

        if args.delete_text_movie_name:
            _tag_movie_name = re.sub('^(.+?):\s?', '\1', tag_movie_name)
            command.append(' --set title="{}" '.format(_tag_movie_name.replace(args.delete_text_movie_name,'')))
            run = True
        if args.delete_text_video_title:
            _tag_video_title = re.sub('^(.+?):\s?', '\1', tag_video_title)
            command.append(' --edit track:v1 --set name="{}" '.format(_tag_video_title.replace(args.delete_text_video_title,'')))
            run = True
        if args.delete_movie_name:
            command.append(' --delete title ')
            run = True
        if args.delete_video_title:
            command.append(' --edit track:v1 --delete name ')
            run = True
        if args.delete_attachment:
            command.append(' --delete-attachment mime-type:image/jpeg --delete-attachment 1 ')
            run = True




        if run:
            mkvpropedit = 'mkvpropedit "{file}" --tags all: {cmd}'.format(file=args.file,cmd="".join(command))
            
            print(" =>",mkvpropedit)
            
            if args.apply: 
                rest = os.system(mkvpropedit)
                if rest == 0: 
                    print("Success")
                    tools(args,finish=True)
                else: print("ERROR")
            else:
                if not args.vn:
                    print(" =>"," ***********  requires --apply to apply mkvpropedit changes  ***********")




    return ""




if __name__ == '__main__':

    try:
        args = parse_args()
        
        if args.print_args: print(args)

        tools(args)

    except:
        pass

