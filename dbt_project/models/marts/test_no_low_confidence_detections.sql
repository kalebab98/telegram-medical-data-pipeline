-- models/marts/test_no_low_confidence_detections.sql
select *
from {{ ref('fct_image_detections') }}
where confidence_score < 0.1
