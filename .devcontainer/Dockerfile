FROM mcr.microsoft.com/devcontainers/python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libatomic1 \
    libgssapi-krb5-2 \
    net-tools \
    iproute2 \
    locales \
    procps \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /workspaces/PersonsInaVideo

RUN python -m pip install --upgrade pip
