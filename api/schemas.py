from pydantic import BaseModel
from typing import List, Optional

class ProductReport(BaseModel):
    product: str
    mentions: int

class ChannelActivity(BaseModel):
    date: str
    message_count: int

class MessageSearchResult(BaseModel):
    message_id: int
    channel_name: str
    message_date: str
    text: Optional[str]

class ImageDetectionResult(BaseModel):
    message_id: int
    channel_name: str
    image_path: str
    detected_object_class: str
    confidence_score: float 