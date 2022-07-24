# FROM node:16-slim as static_files

# WORKDIR /code
# ENV PATH /code/node_modules/.bin:$PATH
# COPY package.json package-lock.json /code/
# RUN npm install --silent
# COPY countertools/static /code/countertools/static/
# RUN npm run build

FROM python:3.10-slim-bullseye as base

# Install packages needed to run your application (not build deps):
#   mime-support -- for mime types when serving static files
#   postgresql-client -- matches RDS version, for running database commands
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.
RUN set -ex \
    && RUN_DEPS=" \
    mime-support \
    postgresql-client-14 \
    ca-certificates \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update \
    && apt-get -y install wget gnupg2 lsb-release \
    # PostgreSQL
    && sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update \
    && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

ADD example-facets/requirements.txt /requirements.txt

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step.
# Correct the path to your production requirements file, if needed.
RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    libpq-dev \
    " \
    && apt-get update \
    && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install --no-cache-dir -r /requirements.txt \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir /code/
WORKDIR /code/
ADD ./example-facets /code/

FROM base AS dev

# Install packages needed to develop your application (not build deps):
#   nodejs -- for Tailwind
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.
RUN set -ex \
    && DEV_DEPS=" \
    nodejs \
    git-core \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update \
    && apt-get -y install wget gnupg2 lsb-release\
    && sh -c 'echo "deb https://deb.nodesource.com/node_16.x $(lsb_release -cs) main" > /etc/apt/sources.list.d/nodesource.list' \
    && wget --quiet -O- https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - \
    && apt-get update \
    && apt-get install -y --no-install-recommends $DEV_DEPS \
    && npm install package.json \
    && rm -rf /var/lib/apt/lists/*

# While example-project is in /code, the full django-filters-facet repo is
# in /django-filters-facet/ (including tests)
RUN mkdir /django-filters-facet/
WORKDIR /django-filters-facet/
ADD . /django-filters-facet/

# Install pytest build deps, then run `pip install`, then remove unneeded build deps all in a single step.
# Correct the path to your production requirements file, if needed.
RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    libpq-dev \
    " \
    && apt-get update \
    && apt-get install -y --no-install-recommends $BUILD_DEPS \
    # add django-filters-facet to example-project site-packges
    && pip install -e . \
    # pytest & django-filters-facet build deps
    && pip install poetry \
    && poetry install \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

ENV DJANGO_SETTINGS_MODULE=example_project.settings.dev

WORKDIR /code/

CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8000"]
