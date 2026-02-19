{{config(severity='warn')}}
SELECT *
FROM {{ source('openbrew', 'breweries_raw') }}
WHERE longitude < -180 OR longitude > 180 and longitude is not null