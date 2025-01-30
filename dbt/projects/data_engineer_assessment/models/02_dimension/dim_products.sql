with distinct_products as (
    select
        product_id
      , category
      , sub_category
      , product_name
      , row_number() over (
          partition by product_id 
          order by count(*) desc, product_name desc
      ) as rn
    from {{ ref('stg_orders') }}
    group by 1,2,3,4
)

select
    hash(
        concat(
            lower(trim(product_id)),
            lower(trim(category)),
            lower(trim(sub_category)),
            lower(trim(product_name))
        )
    ) as product_sk
  , product_id
  , category
  , sub_category
  , product_name
from distinct_products
where rn = 1