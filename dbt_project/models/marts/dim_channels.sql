-- models/marts/dim_channels.sql
select
    channel as channel_name,
    min(message_date) as first_message_date,
    max(message_date) as last_message_date,
    count(*) as total_messages
from {{ ref('stg_telegram_messages') }}
group by channel
