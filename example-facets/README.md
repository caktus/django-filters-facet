# example-facets project

This project demos the functionality of django-filters-facet.

## Development Environment

A Dockerfile is provided for convenience. You can run:

```sh
docker compose up -d --build django
```

### VS Code Development Container

If you use VS Code, a `devcontainer.json` file is configured for use with the
[Visual Studio Code Remote -
Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
extension. Simply open the root django-filters-facet folder in VS Code and
select **Reopen in Container**.

## Load example data

Migrate models:

```sh
python manage.py migrate
```

Load individual datasets:

```sh
python manage.py import_films_data
python manage.py import_firearms_data
```

## Traffic stops data

Export (from host machine):

```sh
psql postgres://postgres@127.0.0.1:54344/traffic_stops_nc -f traffic_stops/data/export.sql > traffic_stops/data/stops.csv
```

Import (within Docker container):

```sh
cat traffic_stops/data/stops.csv | psql $DATABASE_URL -c "COPY traffic_stops_stop FROM STDIN CSV HEADER";
```

## Deploy

Build production image:

```
docker build --target deploy -f example-facets/Dockerfile -t facet_deploy --progress=plain .
```

Or create `docker-compose.override.yaml`:

```yaml
version: '3'

services:
  django:
    environment:
      DJANGO_DEBUG: "False"
      WHITENOISE_ENABLED: "True"
    build:
      target: deploy
    command: ["uwsgi", "--show-config"]
```

And run `docker compose build django`.
