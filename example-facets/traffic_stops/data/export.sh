#!/usr/bin/env bash

set -ex

psql postgres://postgres@127.0.0.1:54344/traffic_stops_nc -c "COPY (SELECT * FROM nc_agency WHERE id IN (168, 79)) TO STDOUT csv header" > traffic_stops/data/agency.csv
psql postgres://postgres@127.0.0.1:54344/traffic_stops_nc -c "COPY (SELECT * FROM nc_searchbasis WHERE stop_id IN (SELECT stop_id FROM nc_stop WHERE agency_id IN (168, 79))) TO STDOUT csv header" > traffic_stops/data/searchbasis.csv
psql postgres://postgres@127.0.0.1:54344/traffic_stops_nc -c "COPY (SELECT * FROM nc_contraband WHERE stop_id IN (SELECT stop_id FROM nc_stop WHERE agency_id IN (168, 79))) TO STDOUT csv header" > traffic_stops/data/contraband.csv
psql postgres://postgres@127.0.0.1:54344/traffic_stops_nc -c "COPY (SELECT * FROM nc_search WHERE stop_id IN (SELECT stop_id FROM nc_stop WHERE agency_id IN (168, 79))) TO STDOUT csv header" > traffic_stops/data/search.csv
psql postgres://postgres@127.0.0.1:54344/traffic_stops_nc -c "COPY (SELECT * FROM nc_person WHERE stop_id IN (SELECT stop_id FROM nc_stop WHERE agency_id IN (168, 79))) TO STDOUT csv header" > traffic_stops/data/person.csv
psql postgres://postgres@127.0.0.1:54344/traffic_stops_nc -c "COPY (SELECT * FROM nc_stop WHERE stop_id IN (SELECT stop_id FROM nc_stop WHERE agency_id IN (168, 79))) TO STDOUT csv header" > traffic_stops/data/stop.csv
