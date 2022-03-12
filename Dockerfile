FROM jlesage/mkvtoolnix

RUN apk update

RUN add-pkg \
        python3 \
        py-pip

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./mkvdelspam /app/
COPY ./mkvdelspam/mkvdelspam.py /usr/local/bin/mkvdelspam
RUN chmod +x /usr/local/bin/mkvdelspam


WORKDIR /app

