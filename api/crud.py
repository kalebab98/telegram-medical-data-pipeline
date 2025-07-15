from .database import get_db_conn
from .schemas import ProductReport, ChannelActivity, MessageSearchResult, ImageDetectionResult
from typing import List

def get_top_products(limit: int = 10) -> List[ProductReport]:
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('''
        select word as product, count(*) as mentions
        from (
            select unnest(string_to_array(lower(text), ' ')) as word
            from fct_messages
            where text is not null
        ) t
        group by word
        order by mentions desc
        limit %s
    ''', (limit,))
    results = [ProductReport(product=row[0], mentions=row[1]) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return results

def get_channel_activity(channel_name: str) -> List[ChannelActivity]:
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('''
        select date_id::text as date, count(*) as message_count
        from fct_messages
        where channel_name = %s
        group by date_id
        order by date_id
    ''', (channel_name,))
    results = [ChannelActivity(date=row[0], message_count=row[1]) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return results

def search_messages(query: str, limit: int = 20) -> List[MessageSearchResult]:
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('''
        select message_id, channel_name, message_date::text, text
        from fct_messages
        where text ilike %s
        order by message_date desc
        limit %s
    ''', (f'%{query}%', limit))
    results = [MessageSearchResult(message_id=row[0], channel_name=row[1], message_date=row[2], text=row[3]) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return results

def get_image_detections(message_id: int) -> List[ImageDetectionResult]:
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('''
        select d.message_id, m.channel as channel_name, d.image_path, d.detected_object_class, d.confidence_score
        from fct_image_detections d
        left join fct_messages m on d.message_id = m.message_id
        where d.message_id = %s
    ''', (message_id,))
    results = [ImageDetectionResult(message_id=row[0], channel_name=row[1], image_path=row[2], detected_object_class=row[3], confidence_score=row[4]) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return results 