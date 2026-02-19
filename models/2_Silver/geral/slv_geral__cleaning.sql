
{{ config(
    materialized='incremental',
    unique_key='brew_pk',
    partition_by=['country']
) }}

with
  geral_brew_list as (
    select *
    from {{ ref('brz_openbrew__geral') }}
  ),

  deduplciate_colunms as (
    select
    brew_pk,
    company_name,
    brewery_type,
    street,
    city,
    country,
    state_province,
    postal_code,
    longitude,
    latitude,
    phone,
    website_url,
    extraction_date
    from geral_brew_list
  ),

  standarization AS (
  select
    brew_pk,
    UPPER(company_name) as company_name,
    UPPER(brewery_type) AS brewery_type ,
    street,
    city,
    country,
    state_province,
    postal_code,
    CAST(longitude AS DOUBLE) as longitude,
    CAST(latitude AS DOUBLE) as latitude,
    phone,
    website_url,
    date_format(extraction_date, 'yyyy/MM/dd') as ext_date
  from deduplciate_colunms
  )

SELECT DISTINCT * FROM standarization

