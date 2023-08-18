FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
RUN pip3 install --no-cache-dir .
RUN pip3 install --no-cache-dir -e .
CMD user-link
