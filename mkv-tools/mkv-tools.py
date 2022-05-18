#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
curl -sL https://raw.githubusercontent.com/jsavargas/python-mkvpropedit/master/mkv-tools/mkv-tools.py -o /usr/local/bin/mkv-tools && chmod +x /usr/local/bin/mkv-tools

'''

import os
import re
import sys
import argparse
import subprocess

__version__ = "VERSION 1.0.15"


def parse_args():
    parser = argparse.ArgumentParser(description="MKV Tools - Delete Spam.")
    parser.add_argument('-V','--version', action='version', version="%(prog)s " + __version__)

                    
    parser.add_argument('-f', '--file', type=str, required=True, help='file mkv to process')
    
    parser.add_argument('-st', '--show-tracks', action='store_true', default=True, help='show tracks from mkv')
    parser.add_argument('-sv', '--show-video-tracks', action='store_true', help='show_video_tracks')
    parser.add_argument('-sm', '--show-movie-name', action='store_true', help='show movie name tag from mkv')
    parser.add_argument('--show-mediainfo', '--mediainfo', action='store_true', help='Show mediainfo file')
    parser.add_argument('--show-fullmediainfo', '--fullmediainfo', action='store_true', help='Show mediainfo --full file')
    parser.add_argument('--pymediainfo', action='store_true', help='Use pymediainfo')
    
    parser.add_argument('--print-args', action='store_true', help='dev use, print arguments')

    parser.add_argument('-smnf', '--set-moviename-filename', action='store_true', help='Set filename to movie name')
    parser.add_argument('-svtf', '--set-videotitle-filename', action='store_true', help='Set filename to video title')
    
    parser.add_argument('-dm', '--delete-movie-name', action='store_true', help='delete movie name')
    parser.add_argument('-dv', '--delete-video-title', action='store_true', help='delete video title')
    parser.add_argument('-da', '--delete-audio-title', action='store_true', help='delete audio title')
    parser.add_argument('-ds', '--delete-subs-title', action='store_true', help='delete subtitle title')
    parser.add_argument('-dat', '--delete-attachment', action='store_true', help='delete attachments')
    parser.add_argument('-dt', '--delete-tracks', action='store_true', help='delete tracks titles')

    parser.add_argument('-dtmn', '--delete-text-movie-name', type=str, help='replace text in movie name')
    parser.add_argument('-dtvt', '--delete-text-video-title', type=str, help='replace text in video title') #TODO get video title y replace string
    parser.add_argument('--delete-text-audio-title', type=str, help='replace text in audio title') #TODO get video title y replace string
    parser.add_argument('--delete-text-subs-title', type=str, help='replace text in subtitle title') #TODO get video title y replace string
    parser.add_argument('--delete-text', type=str, help='replace text in (movie/video/audio/subtitles)') #TODO get video title y replace string


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

def delete_text_audio(track_number=int, text=str,string_delete=str):
    pos_dospuntos=text.find(":")
    _text = line[pos_dospuntos+1:].strip()                         
    if _text != _text.replace(string_delete,'').strip():
        return ' --edit track:a{} --set name="{}" '.format(track_number, _text.replace(string_delete,'').strip())
    else:
        return False
def delete_text_subs(track_number=int, text=str,string_delete=str):
    pos_dospuntos=text.find(":")
    _text = line[pos_dospuntos+1:].strip() 
    if _text != _text.replace(string_delete,'').strip():
        return ' --edit track:s{} --set name="{}" '.format(track_number, _text.replace(string_delete,'').strip())
    else:
        return False

def tools(args, finish=False):

    print("="*30)
    print("PROCESS: ",args.file)


    if args.pymediainfo and ifpymediainfo():
        print("use pymediainfo")
    else:
        
        if not os.path.exists(args.file): 
            print("File not exists")
            exit()

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
        tag_movie_name = ""

        for line in proc.stdout:
            line = line.decode().replace('\n','')
            if line[0:10]=="Movie name":
                if args.show_tracks: print(line )
                elif args.show_movie_name: print(line )
                elif args.delete_text_movie_name: print(line )
                if args.delete_text_movie_name:
                    pos_dospuntos=line.find(":")
                    _tag_movie_name = line[pos_dospuntos+1:].strip()
                    command.append(' --set title="{}" '.format(_tag_movie_name.replace(args.delete_text_movie_name,'').strip()))
                    run = True
                if args.delete_text:
                    pos_dospuntos=line.find(":")
                    _tag_movie_name = line[pos_dospuntos+1:].strip()
                    command.append(" --set title='{}' ".format(_tag_movie_name.replace(args.delete_text,'').strip()))
                    run = True


            if line[:5]=="Cover":
                if args.show_tracks: print(line )

            if line[:11]=="Attachments":
                if args.show_tracks: print(line )

            if line[:5]=="Video":
                #print("")
                video += 1
                head = line
                if args.show_tracks: print(line )

            if line[:5]=="Audio":
                #print("")
                audio +=1
                head = line
                #if args.show_tracks: print(line )
            
            if line[:4]=="Text":
                #print("")
                text +=1
                head = line
                #if args.show_tracks: print(line )
            
            if line[:5]=="Title":
                if text>0:
                    if args.show_tracks: print("{} >> {}".format(head, line) )
                    if args.delete_subs_title or args.delete_tracks:
                        command.append(f'--edit track:s{text} --delete name ')
                        run = True
                    if args.delete_text_subs_title: 
                        resp = delete_text_subs(text,line,args.delete_text_subs_title) 
                        if resp: 
                            command.append(delete_text_subs(text,line,args.delete_text_subs_title) )
                            run = True
                    if args.delete_text: 
                        resp = delete_text_subs(text,line,args.delete_text) 
                        if resp: 
                            command.append(delete_text_subs(text,line,args.delete_text) )
                            run = True
                elif audio>0:
                    if args.show_tracks: print("{} >> {}".format(head, line) )
                    if args.delete_audio_title or args.delete_tracks:
                        command.append(f'--edit track:a{audio} --delete name ')
                        run = True
                    if args.delete_text_audio_title: 
                        resp = delete_text_audio(audio,line,args.delete_text_audio_title) 
                        command.append(delete_text_audio(audio,line,args.delete_text_audio_title) )
                        if resp: 
                            command.append(delete_text_audio(audio,line,args.delete_text) )
                            run = True
                    if args.delete_text: 
                        resp = delete_text_audio(audio,line,args.delete_text)
                        if resp: 
                            command.append(delete_text_audio(audio,line,args.delete_text) )
                            run = True
                elif video>0:
                    if args.show_tracks: print("{} >> {}".format(head, line) )
                    if args.delete_text_video_title:
                        pos_dospuntos=line.find(":")
                        _tag_video_title = line[pos_dospuntos+1:].strip() 
                        
                        command.append(" --edit track:v1 --set name='{}' ".format(_tag_video_title.replace(args.delete_text_video_title,'').strip()))
                        run = True
                    if args.delete_text:
                        pos_dospuntos=line.find(":")
                        _tag_video_title = line[pos_dospuntos+1:].strip() 
                        command.append(' --edit track:v1 --set name="{}" '.format(_tag_video_title.replace(args.delete_text,'').strip()))
                        run = True


            if line[:8]=="Language":
                if args.show_tracks:
                    #print(line )
                    if text>0:
                        print("{} >> {}".format(head, line) )
                    elif audio>0:
                        print("{} >> {}".format(head, line) )
                    elif video>0:
                        print("{} >> {}".format(head, line) )


        newLine()
        if finish: 
            print("\n\n")
            return
        
        if args.set_moviename_filename:
            pattern = re.compile(".mkv", re.IGNORECASE)
            new_name = pattern.sub("", os.path.basename(args.file))
            command.append(' --set title="{}" '.format(new_name))
            run = True
        if args.delete_movie_name or args.delete_tracks:
            command.append(' --delete title ')
            run = True

        if args.set_videotitle_filename:
            pattern = re.compile(".mkv", re.IGNORECASE)
            new_name = pattern.sub("", os.path.basename(args.file))
            command.append(' --edit track:v1 --set name="{}" '.format(new_name))
            run = True
        if args.delete_video_title or args.delete_tracks:
            command.append(' --edit track:v1 --delete name ')
            run = True
        if args.delete_attachment or args.delete_tracks:
            command.append(' --delete-attachment mime-type:image/jpeg --delete-attachment 1 ')
            run = True




        if run:
            mkvpropedit = 'mkvpropedit "{file}" --tags all: {cmd}'.format(file=args.file,cmd="".join(command))
            
            print(" =>",mkvpropedit)
            
            if args.apply: 
                rest = os.system(mkvpropedit)
                if rest == 256: 
                    print(f"Success {rest}")
                    tools(args,finish=True)
                else: print(f"ERROR {rest}")
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

