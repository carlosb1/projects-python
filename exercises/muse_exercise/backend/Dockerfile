FROM ubuntu:latest
ADD . /server
WORKDIR /server
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
RUN apt-get update 
RUN apt-get install -y gcc libc-dev zlib1g-dev libjpeg-dev libxml2-dev ffmpeg python3 python3-pip
RUN pip3 install pipenv --upgrade
RUN export LC_ALL=C.UTF-8 && export LANG=C.UTF-8
RUN pipenv install --deploy --ignore-pipfile
CMD ./run.sh

