-- psql postgres://postgres@127.0.0.1:54344/traffic_stops_nc -f traffic_stops/data/export.sql > traffic_stops/data/stops.csv
COPY (
    SELECT
        "nc_stop"."stop_id" AS id
        , "nc_stop"."date" AT TIME ZONE 'America/New_York'
        , "nc_stop"."purpose" AS "stop_purpose"
        , "nc_stop"."engage_force"
        , "nc_search"."type" AS "search_type"
        , (CASE WHEN nc_contraband.contraband_id IS NULL THEN false
                ELSE true
           END) AS contraband_found
        , "nc_stop"."officer_id"
        , (CASE WHEN "nc_person"."ethnicity" = 'H' THEN 'H'
                WHEN "nc_person"."ethnicity" = 'N' AND "nc_person"."race" = 'A' THEN 'A'
                WHEN "nc_person"."ethnicity" = 'N' AND "nc_person"."race" = 'B' THEN 'B'
                WHEN "nc_person"."ethnicity" = 'N' AND "nc_person"."race" = 'I' THEN 'I'
                WHEN "nc_person"."ethnicity" = 'N' AND "nc_person"."race" = 'U' THEN 'O'
                WHEN "nc_person"."ethnicity" = 'N' AND "nc_person"."race" = 'W' THEN 'W'
           END) as driver_race
        , "nc_person"."gender" AS driver_gender
    FROM "nc_stop"
    INNER JOIN "nc_person"
        ON ("nc_stop"."stop_id" = "nc_person"."stop_id" AND "nc_person"."type" = 'D')
    LEFT OUTER JOIN "nc_search"
        ON ("nc_stop"."stop_id" = "nc_search"."stop_id")
    LEFT OUTER JOIN "nc_contraband"
        ON ("nc_stop"."stop_id" = "nc_contraband"."stop_id")
    WHERE
        "nc_stop"."agency_id" = 80
    ORDER BY "agency_id", "date" ASC
) TO STDOUT csv header;
