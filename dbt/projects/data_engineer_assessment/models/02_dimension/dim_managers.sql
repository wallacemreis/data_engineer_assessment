with 
raw_managers_orders as (
  select 
    'unknow' as manager
   , region 
  from 
    {{ ref('stg_orders') }}
  group by 1,2 
),
raw_dim_managers as (
    select * from {{ ref('stg_managers') }}
    union
    select * from raw_managers_orders
)
select 
    hash(concat(manager, '-', region)) as manager_id
  , * 
from {{ ref('stg_managers') }} 