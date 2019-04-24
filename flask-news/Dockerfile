FROM python:3.7-stretch
ADD . /code
WORKDIR /code
RUN apt-get install -y gcc libc-dev zlib1g-dev libjpeg-dev libxml2-dev
RUN pip install -r requirements.txt
CMD ["python", "app.py"]

