with source as (
    select
        id,
        channel,
        message_date,
        sender_id,
        text,
        has_image,
        has_document,
        has_video,
        has_audio,
        media_type,
        local_media_path,
        raw_json
    from {{ source('public', 'raw_telegram_messages') }}
)

select
    id as message_id,
    channel,
    message_date,
    sender_id,
    text,
    has_image,
    has_document,
    has_video,
    has_audio,
    media_type,
    local_media_path
from source
