-- dim_customer.sql
-- Dimension: one row per customer with descriptive attributes.
-- Materialized as a table (see dbt_project.yml).

with jobs as (
    select * from {{ ref('stg_jobs_tasks') }}
)

select
    customer                          as customer_key,
    count(distinct job_id)            as lifetime_job_count,
    min(created_at)                   as first_seen_date,
    max(created_at)                   as last_seen_date
from jobs
group by customer
