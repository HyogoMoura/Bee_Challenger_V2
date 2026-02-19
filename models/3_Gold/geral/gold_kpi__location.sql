{{
    config(
        materialized='incremental',
    )
}}

WITH silver_brew_list as (
    SELECT *
    FROM {{ ref('slv_geral__cleaning') }}
),

breweries_agregate as (
SELECT
    country,
    state_province,
    brewery_type,
    COUNT(*) AS number_of_brewerys
    FROM silver_brew_list
    GROUP BY ALL
    ORDER BY country,state_province,brewery_type
)

select * from breweries_agregate
