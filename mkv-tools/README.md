# mkv-tools

```
mkvpropedit --tags all: --delete title --edit track:a1 --delete name --edit track:a2 --delete name --edit track:s1 --delete name --edit track:s2 --delete name --edit track:s3 --delete name --edit track:s4 --delete name --edit track:s5 --delete name --edit track:s6 --delete name --edit track:s7 --delete name --edit track:s8 --delete name --edit track:s9 --delete name --edit track:s10 --delete name --edit track:s11 --delete name --edit track:s12 --delete name --edit track:s13 --delete name --edit track:s14 --delete name --edit track:s15 --delete name --edit track:s16 --delete name --edit track:s17 --delete name --edit track:s18 --delete name --edit track:s19 --delete name --edit track:s20 --delete name --edit track:s21 --delete name --edit track:s22 --delete name --edit track:s23 --delete name --edit track:s24 --delete name --edit track:s25 --delete name --edit track:s26 --delete name --edit track:s27 --delete name --edit track:s28 --delete name --edit track:s29 --delete name --edit track:s30 --delete name --edit track:s31 --delete name --edit track:s32 --delete name --edit track:s33 --delete name  --edit track:v1 --delete name --delete-attachment 1  /tmp/File.mkv


```

## mkv-tools -h

```
usage: mkv-tools [-h] [-v] -f FILE [--show_tracks] [--show_video_tracks] [--show_movie_name] 
                 [--show_mediainfo] [--show_fullmediainfo] [--pymediainfo] [--print_args] [-smnf] 
                 [-svtf] [--delete_movie_name] [--delete_video_title] [--delete_attachment] 
                 [-dtmn DELETE_TEXT_MOVIE_NAME] [-dtvt DELETE_TEXT_VIDEO_TITLE] [--vn] [--apply]

MKV Tools - Delete Spam.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -f FILE, --file FILE  file mkv to process
  --show_tracks         show tracks from mkv
  --show_video_tracks   show_video_tracks
  --show_movie_name     show movie name tag from mkv
  --show_mediainfo, --mediainfo
                        Show mediainfo file
  --show_fullmediainfo, --fullmediainfo
                        Show mediainfo --full file
  --pymediainfo         Use pymediainfo
  --print_args          dev use, print arguments
  -smnf, --set_moviename_filename
                        Set filename to movie name
  -svtf, --set_videotitle_filename
                        Set filename to video title
  --delete_movie_name   require mkvpropedit* delete movie name
  --delete_video_title  require mkvpropedit* delete video title
  --delete_attachment   require mkvpropedit* delete attachments
  -dtmn DELETE_TEXT_MOVIE_NAME, --delete_text_movie_name DELETE_TEXT_MOVIE_NAME
                        require mkvpropedit* replace text in movie name
  -dtvt DELETE_TEXT_VIDEO_TITLE, --delete_text_video_title DELETE_TEXT_VIDEO_TITLE
                        require mkvpropedit* replace text in video title
  --vn                  Hidde message "requires --apply"
  --apply               require mkvpropedit* apply changes


```

```bash

curl -L https://raw.githubusercontent.com/jsavargas/python-mkvpropedit/master/mkv-tools/mkv-tools.py -o /usr/local/bin/mkv-tools && chmod +x /usr/local/bin/mkv-tools

mkv-tools -h
mkv-tools -f file.mkv




find /path/files/ -iname "*mkv" -exec mkv-tools -f "{}" \;

```

## MODO DE USO DOCKER


```bash

docker-compose run --rm mkvpropedit sh

docker run --rm -it -v "$(pwd):/storage" jsavargas/mkvpropedit:latest sh
docker run --rm -it -v "$(pwd):/storage" jsavargas/mkvpropedit:latest find /tmp -iname "*.mkv" -exec mkv-tools -f "{}" \;
 ```

## **Requirements:**
- python3
- mediainfo
- mkvtoolnix

## **Changelog:**

**v1.0.11 (22/03/2022/):**
- Update mkv-tools.py

**v1.0.10 (22/03/2022/):**
- Update mkv-tools.py
- Added show Cover 
- Added show Attachments 
- Added delete text in (movie/video/audio/subtitles)
- Fixed bugs
- Added more bugs to fix later (?)

**v1.0.9 (21/03/2022/):**
- Update mkv-tools.py
- Added delete audio titile 
- Added delete subtitles title 
- Added delete all tracks title 
- Added delete text in audio titile
- Added delete text in subtitles titile
- Fixed bugs
- Added more bugs to fix later (?)

**v1.0.8 (21/03/2022/):**
- Update mkv-tools.py
- Added delete movie name 
- Added delete video title 
- Added delete attachments 
- Added delete text in movie name
- Added delete text in video title
- Fixed bugs

**v1.0.7 (20/03/2022/):**
- Update mkv-tools.py
- Fixed bugs
- Added more bugs to fix later
- Support for versions without pymediainfo

