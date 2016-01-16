FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/

#Running celery as root is insecure
#Hence adding new user
RUN adduser --disabled-password --gecos '' worker

RUN apt-get update
RUN apt-get install enchant -y
