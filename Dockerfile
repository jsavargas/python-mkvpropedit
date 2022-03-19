FROM jlesage/mkvtoolnix

RUN apk update

RUN add-pkg \
        python3 \
        py-pip

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./mkvdelspam /app/
COPY ./mkvdelspam/mkvdelspam.py /usr/local/bin/mkvdelspam
COPY ./mkvdelspam/show-tracks.py /usr/local/bin/show-tracks
COPY ./mkv-tools/mkv-tools.py /usr/local/bin/mkv-tools

RUN chmod +x /usr/local/bin/*


WORKDIR /storage

