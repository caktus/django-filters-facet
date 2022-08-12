# example-facets project

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
