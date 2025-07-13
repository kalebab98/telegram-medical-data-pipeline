-- Custom test: No message should have both has_image and has_video as true
select *
from {{ ref('fct_messages') }}
where has_image = true and has_video = true 