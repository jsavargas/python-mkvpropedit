FROM jlesage/mkvtoolnix

RUN apk update

RUN add-pkg \
        python3 \
        py-pip

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

WORKDIR /app

