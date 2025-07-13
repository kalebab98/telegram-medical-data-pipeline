# 🧩 Task 2: PostgreSQL & dbt - Telegram Data Pipeline

This module handles **loading**, **transforming**, and **analyzing** Telegram channel data scraped from Ethiopian medical businesses. Raw JSON data is ingested into PostgreSQL and modeled using `dbt` to enable analytics and machine learning integrations.

---

## ⚙️ Pipeline Overview


- **Source**: Scraped Telegram messages and media
- **Storage**: PostgreSQL 15
- **Transformation**: dbt (Data Build Tool)
- **ML Integration**: YOLOv8 image detection

---

## 🗃️ Database Schema

### Tables

- `raw_telegram_messages`: Stores original messages in structured + JSONB format
- `raw_image_detections`: YOLOv8 object detection results

```sql
CREATE TABLE raw_telegram_messages (...);
CREATE TABLE raw_image_detections (...);

telegram_dbt/
├── models/
│   ├── staging/ → Clean raw inputs
│   └── marts/   → Final dimensional models
├── tests/
└── dbt_project.yml
