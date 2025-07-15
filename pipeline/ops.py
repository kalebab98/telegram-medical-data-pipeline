from dagster import op
import subprocess

@op
def scrape_telegram_data():
    print("Running Telegram scraping...")
    subprocess.run(["python", "scrape_telegram.py"], check=True)

@op
def load_raw_to_postgres():
    print("Loading raw data into Postgres...")
    subprocess.run(["python", "load_to_postgres.py"], check=True)

@op
def run_dbt_transformations():
    print("Running dbt transformations...")
    subprocess.run(["dbt", "run"], check=True, cwd="telegram_dbt")
    subprocess.run(["dbt", "test"], check=True, cwd="telegram_dbt")

@op
def run_yolo_enrichment():
    print("Running YOLO enrichment...")
    subprocess.run(["python", "yolo_enrichment.py"], check=True)
    subprocess.run(["python", "load_yolo_detections.py"], check=True) 