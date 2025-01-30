with distinct_customers as (
    select
          customer_id
        , customer_name
        , segment
    from {{ ref('stg_orders') }}
    group by 1, 2, 3
)

select
      hash(
          concat(
              lower(trim(customer_id)),
              lower(trim(customer_name)),
              lower(trim(segment))
          )
      ) as customer_sk
    , customer_id
    , customer_name
    , segment
from distinct_customers