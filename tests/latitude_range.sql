{{config(severity='warn')}}
SELECT *
FROM {{ source('openbrew', 'breweries_raw') }}
WHERE latitude < -90 OR latitude > 90 and latitude is not null