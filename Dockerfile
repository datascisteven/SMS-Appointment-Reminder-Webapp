FROM python:3.7.4-slim-buster
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
