FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN apt-get update \
    && apt-get -y install curl \
	libxml2-utils \
	locate

ADD requirements.txt /code/

RUN pip install -r requirements.txt

ADD . /code/
