with
    source_geral as (
    select *
    from {{ source('openbrew', 'breweries_raw') }}
    ),

renamed (
    select
    id as brew_pk
    , name as company_name
    , brewery_type
    , address_1
    , address_2
    , address_3
    , city
    , state_province
    , postal_code
    , longitude
    , latitude
    , phone
    , website_url as website_url
    , state
    , country
    , street
    , extraction_date
    from source_geral
)

select * from renamed