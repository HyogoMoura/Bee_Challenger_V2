WITH silver_brew_list as (
    SELECT *
    FROM {{ ref('slv_geral__cleaning') }}
),

snapshot_history as (
SELECT
    country,
    brewery_type,
    COUNT(*) AS brewery_count,
    current_date() AS snapshot_date
FROM silver_brew_list
GROUP BY country, brewery_type
ORDER BY country,brewery_count DESC
)

SELECT * FROM snapshot_history