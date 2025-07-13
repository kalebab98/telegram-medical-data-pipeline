-- models/marts/fct_messages.sql
select
    m.message_id,
    m.channel as channel_name,
    date_trunc('day', m.message_date)::date as date_id,
    m.sender_id,
    m.text,
    m.has_image,
    m.has_document,
    m.has_video,
    m.has_audio,
    m.media_type,
    m.local_media_path
from {{ ref('stg_telegram_messages') }} m
