# syntax=docker/dockerfile:1
FROM mongo
RUN mongod --dbpath data
FROM python:3.11.4-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/