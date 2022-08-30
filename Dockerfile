FROM python:3.10-slim-buster as os-deps

ENV PYTHONUNBUFFERED=1
ENV BUILD_DEPS=" \
      build-essential \
      libpq-dev \
    "
ENV DEPS=" \
      postgresql-client-11 \
      git \
      curl \
      vim \
      libcurl4-openssl-dev \
      libssl-dev \
      python-dev \
      gcc \
    "

# Update the image
RUN set -ex \
    && buildDeps="${BUILD_DEPS}" \
    && deps=${DEPS} \
    && apt-get update && apt-get install -y $buildDeps $deps --no-install-recommends

RUN apt install -y netcat --no-install-recommends
## Stage 2: Install Python dependencies
WORKDIR /app

ENV PATH /env/bin:$PATH

ENV PYTHONPATH=/app/

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt
# Purge packages
RUN set -ex \
    && buildDeps="${BUILD_DEPS}" \
    && deps=${DEPS} \
    && apt-get purge -y --auto-remove $buildDeps \
       $(! command -v gpg > /dev/null || echo 'gnupg dirmngr') \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh
COPY . /app/
STOPSIGNAL SIGINT
EXPOSE 8000