FROM python:3.6

ENV PYTHONBUFFERED 1

RUN mkdir /code

WORKDIR /code


RUN apt-get update \
    && apt-get -y install curl \
	locate

ADD requirements.txt /code/

RUN pip install -r requirements.txt

ADD . /code/