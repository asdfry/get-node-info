FROM python:3.8.17-slim

USER root

COPY . .

RUN apt-get update && apt-get install -y lshw infiniband-diags && \
    pip install --no-cache-dir --upgrade -r requirements.txt
