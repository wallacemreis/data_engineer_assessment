with 
enriched_orders as (
    select
          o.*
        , m.manager_id
        , l.location_id
        , c.customer_sk
    from {{ ref('stg_orders') }} o
    
    left join {{ ref('dim_managers') }} m
        on lower(trim(o.region)) = lower(trim(m.region))
        
    left join {{ ref('dim_location') }} l
        on lower(trim(o.country)) = lower(trim(l.country))
        and lower(trim(o.city)) = lower(trim(l.city))
        and lower(trim(o.state)) = lower(trim(l.state))
        and o.postal_code = l.postal_code
        and lower(trim(o.region)) = lower(trim(l.region))
        
    left join {{ ref('dim_customers') }} c
        on lower(trim(o.customer_id)) = lower(trim(c.customer_id))
),
raw_fact as (
    select
          o.order_id
        , o.order_date
        , o.ship_date
        , o.ship_mode
        , o.manager_id  -- Foreign key to dim_managers
        , o.location_id -- Foreign key to dim_location
        , o.customer_sk -- Foreign key to dim_customers
        , sum(o.sales) as sales
        , sum(o.quantity) as quantity
        , sum(o.profit) as profit
        , avg(datediff('day', o.order_date, o.ship_date)) as avg_delivery_time
    from enriched_orders o
    group by 1,2,3,4,5,6,7
),
enriched_fact as (
    select 
          rf.*
        , case when r.returned is not null 
            then true 
            else false 
          end as is_return_order
        , case when r.returned is null 
            then rf.sales 
            else 0 
          end as adjusted_sales
        , case when r.returned is null 
            then rf.profit 
            else 0 
          end as adjusted_profit
    from raw_fact rf
    left join {{ ref('stg_returns') }} r
        on lower(trim(r.order_id)) = lower(trim(rf.order_id))
)
select
      ef.*
    , case when adjusted_sales > 0 
        then adjusted_profit / adjusted_sales 
        else 0 
      end as profit_margin
from enriched_fact ef