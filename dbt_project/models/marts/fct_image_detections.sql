-- models/marts/fct_image_detections.sql

select
    d.message_id,
    m.channel as channel_name,
    m.message_date,
    d.image_path,
    d.detected_object_class,
    d.confidence_score
from {{ source('public', 'raw_image_detections') }} d
left join {{ ref('stg_telegram_messages') }} m
    on d.message_id = m.message_id
