-- models/marts/dim_dates.sql
with dates as (
    select distinct date_trunc('day', message_date) as date
    from {{ ref('stg_telegram_messages') }}
)
select
    date::date as date_id,
    extract(year from date) as year,
    extract(month from date) as month,
    extract(day from date) as day,
    extract(dow from date) as day_of_week,
    extract(week from date) as week
from dates
