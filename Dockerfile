FROM python:3.8.17-slim

COPY . .

RUN apt-get update && apt-get install -y lshw && \
    pip install --no-cache-dir --upgrade -r requirements.txt
