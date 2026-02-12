FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        curl \
        wget \
        unzip \
        sudo \
        ca-certificates \
        procps \
        vim \
        ffmpeg \
        libgl1 \
        libglib2.0-0 \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

RUN python -m pip install --upgrade pip
