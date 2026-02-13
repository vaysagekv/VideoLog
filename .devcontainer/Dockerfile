ARG VARIANT="3.11-bookworm"
FROM mcr.microsoft.com/devcontainers/python:${VARIANT}

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /workspaces/PersonsInaVideo

RUN python -m pip install --upgrade pip
