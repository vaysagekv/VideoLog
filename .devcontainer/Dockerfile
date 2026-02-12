FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    git \
    curl \
    wget \
    unzip \
    tar \
    ca-certificates \
    procps \
    libgl1 \
    libglib2.0-0 \
    libstdc++6 \
    openssh-client \
    net-tools \
    iproute2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /workspaces/PersonsInaVideo

RUN python -m pip install --upgrade pip
