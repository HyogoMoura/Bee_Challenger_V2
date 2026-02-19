{{config(severity='warn')}}

SELECT *
FROM {{ source('openbrew', 'breweries_raw') }}
WHERE country IS NULL