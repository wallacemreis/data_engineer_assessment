with raw_returns as (
    select * from returns
)

select
    trim(order_id) as order_id,
    lower(trim(returned)) as returned
from raw_returns
group by 1,2