import os
import csv
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

CSV_FILE = 'yolo_detections.csv'

# Load environment variables
load_dotenv()
DB_HOST = os.getenv('PGHOST', 'localhost')
DB_PORT = os.getenv('PGPORT', '5432')
DB_NAME = os.getenv('PGDATABASE', 'telegram_data')
DB_USER = os.getenv('PGUSER', 'postgres')
DB_PASS = os.getenv('PGPASSWORD', 'postgres')

CREATE_TABLE_SQL = '''
CREATE TABLE IF NOT EXISTS raw_image_detections (
    message_id BIGINT,
    image_path TEXT,
    detected_object_class TEXT,
    confidence_score FLOAT
);
'''

INSERT_SQL = '''
INSERT INTO raw_image_detections (
    message_id, image_path, detected_object_class, confidence_score
) VALUES %s
ON CONFLICT DO NOTHING;
'''

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

    rows = []
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append((
                int(row['message_id']),
                row['image_path'],
                row['detected_object_class'],
                float(row['confidence_score'])
            ))
    if rows:
        execute_values(cur, INSERT_SQL, rows)
        conn.commit()
        print(f"Inserted {len(rows)} detections into raw_image_detections.")
    else:
        print("No detections found to insert.")
    cur.close()
    conn.close()

if __name__ == '__main__':
    main() 