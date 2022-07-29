#!/usr/bin/env bash

set -ex

python manage.py migrate traffic_stops zero
python manage.py migrate traffic_stops

cat traffic_stops/data/agency.csv | psql $DATABASE_URL -c "COPY traffic_stops_agency FROM STDIN CSV HEADER";
cat traffic_stops/data/stop.csv | psql $DATABASE_URL -c "COPY traffic_stops_stop FROM STDIN CSV HEADER";
cat traffic_stops/data/person.csv | psql $DATABASE_URL -c "COPY traffic_stops_person FROM STDIN CSV HEADER";
cat traffic_stops/data/search.csv | psql $DATABASE_URL -c "COPY traffic_stops_search FROM STDIN CSV HEADER";
cat traffic_stops/data/searchbasis.csv | psql $DATABASE_URL -c "COPY traffic_stops_searchbasis FROM STDIN CSV HEADER";
cat traffic_stops/data/contraband.csv | psql $DATABASE_URL -c "COPY traffic_stops_contraband FROM STDIN CSV HEADER";
