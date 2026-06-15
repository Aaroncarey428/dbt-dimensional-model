-- stg_jobs_tasks.sql
-- Staging layer: clean and standardize the raw seed data.
-- Materialized as a view (see dbt_project.yml).

with source as (
    select * from {{ ref('raw_jobs_tasks') }}
),

cleaned as (
    select
        cast(job_id as integer)              as job_id,
        cast(task_id as integer)             as task_id,
        trim(customer)                       as customer,
        city,
        job_type,

        -- Classify every job as Proactive or Reactive.
        case
            when job_type in ('Preventive', 'Inspection', 'Planned')
                then 'Proactive'
            else 'Reactive'
        end                                  as pro_reactive,

        -- Normalize status into a simple open or closed grouping.
        case when status = 'Closed' then 'Closed' else 'Open' end as open_closed,

        status                               as detailed_status,
        cast(created_at as date)             as created_at,
        coalesce(cast(task_cost as double), 0) as task_cost,
        cast(sales_price as double)          as sales_price
    from source
)

select * from cleaned
