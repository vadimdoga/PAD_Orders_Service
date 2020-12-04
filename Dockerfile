FROM python:3.8-slim

WORKDIR /orders_service

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV APP_ENVIRONMENT=production
