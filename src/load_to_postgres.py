import os
import json
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

RAW_DATA_DIR = 'data/raw/telegram_messages'

# Load environment variables
load_dotenv()
DB_HOST = os.getenv('PGHOST', 'localhost')
DB_PORT = os.getenv('PGPORT', '5432')
DB_NAME = os.getenv('PGDATABASE', 'telegram_data')
DB_USER = os.getenv('PGUSER', 'postgres')
DB_PASS = os.getenv('PGPASSWORD', 'postgres')

CREATE_TABLE_SQL = '''
CREATE TABLE IF NOT EXISTS raw_telegram_messages (
    id BIGINT,
    channel TEXT,
    message_date TIMESTAMP,
    sender_id BIGINT,
    text TEXT,
    has_image BOOLEAN,
    has_document BOOLEAN,
    has_video BOOLEAN,
    has_audio BOOLEAN,
    media_type TEXT,
    local_media_path TEXT,
    raw_json JSONB
);
'''

INSERT_SQL = '''
INSERT INTO raw_telegram_messages (
    id, channel, message_date, sender_id, text, has_image, has_document, has_video, has_audio, media_type, local_media_path, raw_json
) VALUES %s
ON CONFLICT DO NOTHING;
'''

def get_all_json_files():
    for date_dir in os.listdir(RAW_DATA_DIR):
        date_path = os.path.join(RAW_DATA_DIR, date_dir)
        if not os.path.isdir(date_path):
            continue
        for file in os.listdir(date_path):
            if file.endswith('.json'):
                yield date_dir, file, os.path.join(date_path, file)

def main():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cur = conn.cursor()
    cur.execute(CREATE_TABLE_SQL)
    conn.commit()

    all_rows = []
    for date_dir, file, path in get_all_json_files():
        channel = file.replace('.json', '')
        with open(path, 'r', encoding='utf-8') as f:
            messages = json.load(f)
            for msg in messages:
                all_rows.append((
                    msg.get('id'),
                    channel,
                    msg.get('date'),
                    msg.get('sender_id'),
                    msg.get('text'),
                    msg.get('has_image'),
                    msg.get('has_document'),
                    msg.get('has_video'),
                    msg.get('has_audio'),
                    msg.get('media_type'),
                    msg.get('local_media_path'),
                    json.dumps(msg)
                ))
    if all_rows:
        execute_values(cur, INSERT_SQL, all_rows)
        conn.commit()
        print(f"Inserted {len(all_rows)} messages into raw_telegram_messages.")
    else:
        print("No messages found to insert.")
    cur.close()
    conn.close()

if __name__ == '__main__':
    main() 