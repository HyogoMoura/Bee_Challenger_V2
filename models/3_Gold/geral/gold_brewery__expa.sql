WITH silver_brew_list as (
    SELECT *
    FROM {{ ref('slv_geral__cleaning') }}
),


feature_ml_expansion as (
SELECT
    country,
    COUNT(*) AS brewery_density,
    COUNT(DISTINCT brewery_type) AS type_diversity,
    AVG(latitude) AS avg_lat,
    AVG(longitude) AS avg_long
FROM silver_brew_list
WHERE latitude IS NOT NULL AND longitude IS NOT NULL
GROUP BY country
ORDER BY type_diversity DESC,brewery_density DESC
)

SELECT * FROM feature_ml_expansion