FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

RUN apt-get update && apt-get install -y locales locales-all
ENV LC_ALL=ru_RU.UTF-8
ENV LANG=ru_RU.UTF-8
ENV LANGUAGE=ru_RU.UTF-8

RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-rus
