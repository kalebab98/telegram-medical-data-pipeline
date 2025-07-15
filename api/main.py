from fastapi import FastAPI, Query, Path
from typing import List, Optional
import psycopg2
import os
from dotenv import load_dotenv
from .schemas import ProductReport, ChannelActivity, MessageSearchResult

load_dotenv()

DB_HOST = os.getenv('PGHOST', 'localhost')
DB_PORT = os.getenv('PGPORT', '5432')
DB_NAME = os.getenv('PGDATABASE', 'telegram_data')
DB_USER = os.getenv('PGUSER', 'postgres')
DB_PASS = os.getenv('PGPASSWORD', 'kaleb1234')

app = FastAPI()

def get_db_conn():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.get("/api/reports/top-products", response_model=List[ProductReport])
def top_products(limit: int = Query(10, gt=0, le=100)):
    # Example: count most mentioned products (by word frequency in messages)
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

@app.get("/api/channels/{channel_name}/activity", response_model=List[ChannelActivity])
def channel_activity(channel_name: str):
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

@app.get("/api/search/messages", response_model=List[MessageSearchResult])
def search_messages(query: str = Query(..., min_length=1, max_length=100), limit: int = Query(20, gt=0, le=100)):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('''
        select message_id, channel_name, date_id::text, text
        from fct_messages
        where text ilike %s
        order by date_id desc
        limit %s
    ''', (f'%{query}%', limit))
    results = [MessageSearchResult(message_id=row[0], channel_name=row[1], message_date=row[2], text=row[3]) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return results 