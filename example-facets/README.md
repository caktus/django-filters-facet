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
