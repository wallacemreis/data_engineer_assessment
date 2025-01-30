with raw_orders as (
    select * from orders
)

select
      id
    , order_id
    , order_date
    , ship_date
    , trim(ship_mode) as ship_mode
    , trim(customer_id) as customer_id
    , trim(customer_name) as customer_name
    , trim(segment) as segment
    , trim(country) as country
    , trim(city) as city
    , trim(state) as state
    , postal_code
    , trim(region) as region
    , trim(product_id) as product_id
    , trim(category) as category
    , trim(sub_category) as sub_category
    , trim(product_name) as product_name
    , sales
    , quantity
    , discount
    , profit
from raw_orders