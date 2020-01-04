FROM python:3.7-slim

WORKDIR /automl

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt