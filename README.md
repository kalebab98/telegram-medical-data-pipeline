# 📦 Ethiopian Medical Telegram Data Pipeline

This project implements a robust and modular data pipeline that scrapes Telegram messages and media from public channels related to **Ethiopian medical businesses**, enriches the data using **YOLOv8**, exposes analytical insights via a **FastAPI** interface, and orchestrates all components using **Dagster**.

---

## 🔧 Features

* **Telegram Scraper**: Incremental scraping of messages and media (images, videos, audio).
* **YOLOv8 Enrichment**: Detects objects in scraped media (e.g., pills, creams) and stores metadata.
* **FastAPI Analytics API**: Real-time product mentions, activity trends, and message search.
* **Dagster Orchestration**: End-to-end job orchestration with monitoring and scheduling.
* **dbt Integration**: Staging, transformation, and analysis in a warehouse (PostgreSQL).

---

## 🗂️ Directory Structure

```
.
├── scraper/                   # Telegram scraping logic
├── enrichment/                # YOLOv8 image enrichment scripts
├── api/                       # FastAPI application
├── pipeline/                  # Dagster pipeline configuration
├── telegram_dbt/              # dbt models for transformation and analytics
├── data/                      # Raw and enriched data output
├── logs/                      # Logs for scraping and enrichment
└── README.md                  # Project overview (this file)
```

---

## ⚙️ 1. Telegram Data Scraper

Scrapes messages, images, and videos from public Telegram channels.

### ✅ Features

* Incremental scraping with checkpoints
* Partitioned storage by date/channel
* Parallel scraping support
* Keyword and MIME filtering
* Logs progress and errors

### 🚀 Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_SESSION=anon
```

Add channels to `channels.txt`, one per line.

### ▶️ Usage

```bash
python scrape_telegram.py \
  --channels channels.txt \
  --start-date 2024-07-01 \
  --end-date 2024-07-10 \
  --keywords paracetamol cream pill \
  --image-types image/jpeg image/png \
  --parallel
```

---

## 🧠 2. YOLOv8 Image Enrichment

Detects medical objects in scraped images using YOLOv8 and stores results in PostgreSQL.

### ✅ Setup

```bash
pip install ultralytics==8.3.15
```

### ▶️ Run

```bash
python load_yolo_detections.py
# or
python yolo_enrichment.py
```

### ✅ Output Schema: `raw_image_detections`

| Field                   | Description                    |
| ----------------------- | ------------------------------ |
| detection_id            | Primary key                    |
| message_id              | Foreign key to message         |
| image_path              | Path to local image file       |
| detected_object_class   | COCO or mapped medical class   |
| confidence_score        | Detection confidence (0.0–1.0) |
| detection_timestamp     | Time of detection              |

### ✅ dbt Models

* `stg_image_detections.sql`: Staging with confidence filter (≥ 0.5)
* `fct_image_detections.sql`: Fact table linking detections to messages

---

## 🌐 3. FastAPI Analytics API

Provides endpoints to explore insights from Telegram medical data.

### ▶️ Run

```bash
uvicorn api.main:app --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

### 📊 Endpoints

| Endpoint                                          | Description                    |
| ------------------------------------------------- | ------------------------------ |
| `/api/reports/top-products?limit=10`              | Top mentioned medical products |
| `/api/channels/{channel_name}/activity`           | Message counts over time       |
| `/api/search/messages?query=paracetamol&limit=20` | Search messages by keyword     |

---

## ⚙️ 4. Dagster Pipeline Orchestration

End-to-end orchestration with real-time observability and scheduling.

### ✅ Features

* Ops for each step: scraping, loading, dbt, YOLO
* Modular, restartable, and observable
* Web UI for logs, runs, and schedules

### ▶️ Setup

```bash
pip install dagster dagster-webserver
```

### ▶️ Run Dagster UI

```bash
dagster dev
```

Open [http://localhost:3000](http://localhost:3000) to monitor pipeline.

### ✅ Pipeline Flow

```
scrape_telegram_data → load_raw_to_postgres → run_dbt_transformations → run_yolo_enrichment
```

---

## 🧪 5. Testing & Validation

* **Scraper**: Logs errors and saves checkpoints
* **Enrichment**: Confidence score validation (0–1)
* **dbt Tests**:
  * `unique` and `not_null` on `detection_id`
  * `foreign key` on `message_id`
  * Custom test: Valid confidence range
* **FastAPI**: Pydantic schemas ensure input/output validation

---

## 💡 Business Value

* **Product Intelligence**: Track mentions of medical products like paracetamol or creams.
* **Visual Analysis**: Detect object types in media content (e.g., pills, syringes).
* **Channel Insights**: Measure activity and marketing pushes across Telegram channels.
* **Text + Image Fusion**: Answer complex queries like:

  > “How many images of paracetamol were shared last week?”

---

## 🚀 Future Improvements

* NLP-based product/entity extraction
* Real-time dashboards (e.g., with Superset or Metabase)
* Custom YOLO training for domain-specific classes
* Integration with SMS or WhatsApp for omnichannel monitoring

---

## ✅ Quick Start Summary

```bash
# Install all dependencies
pip install -r requirements.txt
pip install ultralytics==8.3.15 dagster dagster-webserver

# Scrape messages & media
python scrape_telegram.py --start-date 2024-07-01 --end-date 2024-07-10 --parallel

# Run YOLO enrichment
python yolo_enrichment.py

# Launch FastAPI
uvicorn api.main:app --reload

# Launch Dagster UI
dagster dev
```

---

## Scrernshots
<img width="1194" height="916" alt="top-products" src="https://github.com/user-attachments/assets/3a4ac2d8-bb4b-4c40-b72d-081161e631a6" />
<img width="1191" height="921" alt="channel-activity" src="https://github.com/user-attachments/assets/0975afe7-62c7-48e3-9855-613f2dc0841e" />
<img width="1206" height="910" alt="search-messages" src="https://github.com/user-attachments/assets/26d31c79-7607-4089-9e0f-eac48b700de2" />
<img width="1911" height="913" alt="Screenshot 2025-07-15 210758" src="https://github.com/user-attachments/assets/987b9664-7f7e-4edf-9802-a83204e908fb" />
<img width="1909" height="901" alt="Screenshot 2025-07-15 210635" src="https://github.com/user-attachments/assets/2994e018-5def-4a13-9214-e0c9c800e560" />
 reach out to the maintainers.
