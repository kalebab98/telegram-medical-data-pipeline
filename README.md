## 🛠️ Task 3: Data Enrichment with YOLOv8

### ✅ Status
✔️ Completed

### 🎯 Deliverables

#### ✅ YOLOv8 Processing
- **Script:** `load_yolo_detections.py` (or `yolo_enrichment.py`)
  - Uses YOLOv8 (`yolov8n.pt`) to detect and classify objects in images scraped from Telegram channels (e.g., pills, creams, syringes).
  - Maps COCO classes to relevant medical categories.
  - Logs enrichment process and results for traceability.

#### ✅ Storage
- **Table:** `raw_image_detections` (or similar)
  - `detection_id` (PRIMARY KEY)
  - `message_id` (FOREIGN KEY to messages)
  - `image_path`
  - `detected_object_class`
  - `confidence_score`
  - `detection_timestamp`

#### ✅ dbt Integration
- **Staging Model:** `stg_image_detections.sql` (confidence >= 0.5)
- **Fact Table:** `fct_image_detections.sql` links detections to messages for analysis.
- **Analysis:** Enables queries like object counts per channel, detection trends, and visual content insights.

#### ✅ Testing
- **dbt Tests:**
  - `unique` and `not_null` for `detection_id`.
  - `relationships` for `message_id` foreign key.
  - **Custom Test:** Ensures confidence scores are within valid range (e.g., 0.0–1.0).

#### ✅ Documentation
- **dbt Docs:**
  - Updated with new staging and mart models for image detections.
  - Describes enrichment logic and analytical use cases.


### 💡 Business Value
- **Product Mentions:** Identify trending drugs and products in the Ethiopian market.
- **Price & Availability:** Track how prices and stock levels change across channels and over time.
- **Channel Analysis:** Discover which channels are most active and which share the most visual content.
- **Text & Image Fusion:** Combine YOLOv8 image detections with message text for richer analytics (e.g., "How many images of paracetamol were posted last week?").

### 🚀 Next Steps
- Improve product extraction with NLP and stopword filtering.
- Build dashboards for real-time monitoring.
- Expand enrichment to include more object classes or custom-trained models.

### 🚀 Execution Instructions

1. **Install YOLOv8 dependencies:**
   ```bash
   pip install ultralytics==8.3.15
   ```
2. **Run the enrichment script:**
   ```bash
   python load_yolo_detections.py
   # or
   python yolo_enrichment.py
   ```
3. **Verify enrichment results:**
   - Check the `raw_image_detections` table in PostgreSQL:
     ```sql
     SELECT * FROM raw_image_detections LIMIT 5;
     ```
   - Review logs for errors or summary statistics.
4. **Run dbt models:**
   ```bash
   dbt run --project-dir telegram_dbt
   dbt test --project-dir telegram_dbt
   ```
5. **Generate and serve dbt docs:**
   ```bash
   dbt docs generate --project-dir telegram_dbt
   dbt docs serve --project-dir telegram_dbt
   ```

### 📝 Notes
- YOLOv8 model (`yolov8n.pt`) can be swapped for a custom-trained medical model if available.
- Enrichment pipeline is modular and can be extended for new object classes or improved accuracy.
- Analytical queries (e.g., object counts per channel) are enabled via dbt marts and analysis scripts.
- All enrichment and transformation steps are logged for reproducibility and debugging. 
