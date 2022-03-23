FROM jlesage/mkvtoolnix

RUN apk update

RUN add-pkg \
        python3 \
        py-pip

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./mkv-tools /app/
COPY ./mkv-tools/mkv-tools.py /usr/local/bin/mkv-tools

RUN chmod +x /usr/local/bin/*


WORKDIR /storage

