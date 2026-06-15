-- fct_jobs.sql
-- Fact: one row per job with its measures.
-- Note: sales_price repeats across tasks of a job, so we take the
-- job level value once and sum task level costs.

with tasks as (
    select * from {{ ref('stg_jobs_tasks') }}
)

select
    job_id,
    customer                          as customer_key,
    min(created_at)                   as job_created_at,
    max(pro_reactive)                 as pro_reactive,
    max(open_closed)                  as open_closed,
    count(distinct task_id)           as task_count,
    sum(task_cost)                    as total_task_cost,
    max(sales_price)                  as job_sales_price
from tasks
group by job_id, customer
