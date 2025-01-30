with 
unique_locations as (
    select
          country
        , city
        , state
        , postal_code
        , region
    from {{ ref('stg_orders') }}
    group by 1,2,3,4,5
)
select
      hash(concat(country, city, state, postal_code, region)) as location_id
    , country
    , city
    , state
    , postal_code
    , region
from unique_locations