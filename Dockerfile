FROM jlesage/mkvtoolnix

RUN apk update

RUN add-pkg \
        python3 \
        py-pip

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./mkvtoolnix /app/
COPY ./mkvtoolnix/mkvtoolnix.py /usr/local/bin/mkvdelspam
RUN chmod +x /usr/local/bin/mkvdelspam


WORKDIR /app

