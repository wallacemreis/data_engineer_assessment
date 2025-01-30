with raw_managers as (
    select manager, region from managers group by 1,2
)
select
    trim(manager) as manager,
    trim(region) as region
from raw_managers
