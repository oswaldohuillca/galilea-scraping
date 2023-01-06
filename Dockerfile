
FROM ubuntu:20.04

RUN apt update

RUN apt install python3 -y
RUN apt install python3-pip -y

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /usr/app/src

COPY . .