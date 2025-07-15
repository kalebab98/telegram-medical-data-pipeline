# 🛠️ Task 5: Pipeline Orchestration with Dagster

## Overview
This module implements robust, observable, and schedulable orchestration for the end-to-end Telegram data pipeline using Dagster. Each major step—scraping, loading, transformation, and enrichment—is modularized as a Dagster op and combined into a single job for seamless execution and monitoring.

## Features
- **Modular Dagster ops** for each pipeline step:
  - Scrape Telegram data
  - Load raw data to Postgres
  - Run dbt transformations
  - Run YOLO enrichment
- **End-to-end job orchestration** via `full_pipeline`
- **UI monitoring** and real-time logs via Dagster webserver
- **Easy scheduling** for automated, recurring runs

## Code Structure
```
pipeline/
├── __init__.py         # Package marker
├── ops.py              # Dagster ops for each pipeline step
├── jobs.py             # Dagster job combining all ops
└── repository.py       # Dagster repository registration
```

## Setup & Execution
1. **Install dependencies:**
   ```bash
   pip install dagster dagster-webserver
   ```
2. **Launch Dagster UI:**
   ```bash
   dagster dev
   ```
   - Access the UI at http://localhost:3000
3. **Run the pipeline:**
   - Trigger the `full_pipeline` job from the UI or CLI.
   - Monitor logs and step outputs in real time.
4. **(Optional) Add a schedule:**
   - Use Dagster’s scheduling features to run the pipeline automatically (e.g., daily).

## Example Job Flow
1. `scrape_telegram_data` → 2. `load_raw_to_postgres` → 3. `run_dbt_transformations` → 4. `run_yolo_enrichment`

## Business Value
- **Reliability:** Ensures the pipeline is robust and observable.
- **Automation:** Enables hands-off, scheduled data updates and enrichment.
- **Transparency:** Visual interface for monitoring and debugging.
- **Scalability:** Modular design for easy extension.

## Notes
- All steps are logged and can be retried individually.
- The orchestration layer is decoupled from business logic for maintainability.
- Local-development friendly, but extensible for production. 

## Screenshots


<img width="1911" height="913" alt="Screenshot 2025-07-15 210758" src="https://github.com/user-attachments/assets/6ab8243e-40b1-46d2-be53-465c56ff4128" />
<img width="1909" height="901" alt="Screenshot 2025-07-15 210635" src="https://github.com/user-attachments/assets/4d92c31e-c962-4463-9c67-1c5921576414" />
