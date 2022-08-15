FROM node:18-bullseye-slim as static_files

WORKDIR /code
ENV PATH /code/node_modules/.bin:$PATH
COPY example-facets/package.json example-facets/package-lock.json example-facets/postcss.config.js example-facets/tailwind.config.js /code/
RUN npm install --silent
COPY example-facets/example_project/static example_project/static
COPY example-facets/example_project/templates example_project/templates
COPY example-facets/traffic_stops/templates traffic_stops/templates
COPY example-facets/firearms/templates firearms/templates
COPY src/django_filters_facet/templates /django-filters-facet/src/django_filters_facet/templates
RUN npm run build

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

ENV DJANGO_SETTINGS_MODULE=example_project.settings

FROM base AS package

# While example-project is in /code, the full django-filters-facet repo is
# in /django-filters-facet/ (including tests)
RUN mkdir /django-filters-facet/
WORKDIR /django-filters-facet/
ADD src /django-filters-facet/src/
ADD .pre-commit-config.yaml poetry.lock pyproject.toml setup.cfg setup.py /django-filters-facet/

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

# Build django-filters-facet package
RUN poetry build

CMD ["/bin/bash"]

FROM base AS deploy

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir -p /code/
WORKDIR /code/
ADD ./example-facets /code

# Copy node-built TailwindCSS assets into final image
COPY --from=static_files /code/example_project/static/css/main.css /code/example_project/static/css/main.css

# Copy built django-filters-facet package and install it
COPY --from=package /django-filters-facet/dist /dist
RUN set -ex \
    && pip install /dist/django_filters_facet*.whl

# Create a group and user to run our app
ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
RUN DATABASE_URL='' ENVIRONMENT='' DJANGO_SECRET_KEY='dummy' DOMAIN='' WHITENOISE_ENABLED='True' python manage.py collectstatic --noinput --no-default-ignore

# Tell uWSGI where to find your wsgi file (change this):
ENV UWSGI_WSGI_FILE=example_project/wsgi.py

# Base uWSGI configuration (you shouldn't need to change these):
ENV UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_HTTP_AUTO_CHUNKED=1 UWSGI_HTTP_KEEPALIVE=1 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy UWSGI_IGNORE_SIGPIPE=true UWSGI_IGNORE_WRITE_ERRORS=true UWSGI_DISABLE_WRITE_EXCEPTION=true

# Number of uWSGI workers and threads per worker (customize as needed):
ENV UWSGI_WORKERS=2 UWSGI_THREADS=4

# uWSGI static file serving configuration (customize or comment out if not needed):
ENV UWSGI_STATIC_MAP="/static/=/public/static/" UWSGI_STATIC_EXPIRES_URI="/static/.*\.[a-f0-9]{12,}\.(css|js|png|jpg|jpeg|gif|ico|woff|ttf|otf|svg|scss|map|txt) 315360000"

# Change to a non-root user
USER ${APP_USER}:${APP_USER}

# Uncomment after creating your docker-entrypoint.sh
ENTRYPOINT ["/code/docker-entrypoint.sh"]

# Start uWSGI
CMD ["uwsgi", "--single-interpreter", "--enable-threads", "--show-config"]

FROM package AS dev

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

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir -p /code/
WORKDIR /code/
ADD ./example-facets /code/

CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8000"]
