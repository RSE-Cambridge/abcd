FROM python:3
MAINTAINER Jeffrey Salmond <js947@cam.ac.uk>

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY abcd abcd
COPY abcd.py abcd.py
RUN ls

ENTRYPOINT [ "python", "./abcd.py" ]
