FROM python:3.12.0-slim

#install dependencies
RUN apt update && apt install -y --no-install-recommends\
    curl \
    redis-tools \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

#install pip
RUN pip install --upgrade pip

#packages management
RUN pip install pip-autoremove pipdeptree

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app