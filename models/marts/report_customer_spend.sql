-- report_customer_spend.sql
-- Reporting mart: customer level spend, joining the fact to the dimension.

with fct as (
    select * from {{ ref('fct_jobs') }}
),

dim as (
    select * from {{ ref('dim_customer') }}
)

select
    dim.customer_key,
    dim.lifetime_job_count,
    count(distinct fct.job_id)        as jobs_in_period,
    sum(fct.task_count)               as total_tasks,
    round(sum(fct.job_sales_price), 2) as total_sales_price,
    round(sum(fct.total_task_cost), 2) as total_task_cost
from fct
join dim on fct.customer_key = dim.customer_key
group by dim.customer_key, dim.lifetime_job_count
order by total_sales_price desc
