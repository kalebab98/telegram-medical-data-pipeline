## 🛠️ Task 4: Analytical API with FastAPI

### ✅ Status
⏳ In Progress / ✔️ Completed (update as appropriate)

### 🎯 Deliverables
- Developed a FastAPI application to expose analytical insights from the data warehouse.
- Endpoints answer key business questions for stakeholders:
  - Top mentioned medical products and drugs
  - Channel activity and posting trends
  - Search for messages by keyword
- Utilizes Pydantic schemas for data validation and clear API documentation.
- Interactive API docs available at `/docs` (Swagger UI).
- **See screenshots below for example usage and responses.**

### 📊 Example Insights & API Outputs

#### Top Mentioned Products (Sample Output)
```json
[
  { "product": "paracetamol", "mentions": 200 },
  { "product": "amoxicillin", "mentions": 180 }
  // ...
]
```
*Note: Further text cleaning and product extraction can improve these results by filtering out stopwords and non-product terms.*

#### Channel Activity Over Time (Sample Output)
```json
[
  { "date": "2025-06-18", "message_count": 20 },
  { "date": "2025-06-19", "message_count": 26 },
  { "date": "2025-06-20", "message_count": 25 }
  // ...
]
```
*Business Insight: Posting activity trends can reveal marketing pushes, product launches, or seasonal demand.*

#### Example Message Search Result
```json
[
  {
    "message_id": 172045,
    "channel_name": "tikvahpharma",
    "message_date": "2025-07-08",
    "text": "**Tikvah Sales\n(Pharma Import)**\n\n#AMYN ..."
  },
  {
    "message_id": 53019,
    "channel_name": "PharmacyHubEthiopia",
    "message_date": "2025-07-08",
    "text": "Import\n\nNew arrival ..."
  }
  // ...
]
```
*Business Insight: Stakeholders can search for specific products, price updates, or availability across all channels in real time.*

### 💡 Business Value
- **Product Mentions:** Identify trending drugs and products in the Ethiopian market.
- **Price & Availability:** Track how prices and stock levels change across channels and over time.
- **Channel Analysis:** Discover which channels are most active and which share the most visual content.
- **Text & Image Fusion:** Combine YOLOv8 image detections with message text for richer analytics (e.g., "How many images of paracetamol were posted last week?").

### 🚀 Execution Instructions
1. Start the FastAPI server:
   ```bash
   uvicorn api.main:app --reload
   ```
2. Access the interactive API docs at [http://localhost:8000/docs](http://localhost:8000/docs)
3. Try out endpoints for real-time analytics and insights. 

#### API Endpoints

- **GET /api/reports/top-products?limit=10**
  - Returns the most frequently mentioned products.
  - **Query Parameters:** `limit` (int, default 10)
- **GET /api/channels/{channel_name}/activity**
  - Returns posting activity for a specific channel.
  - **Path Parameter:** `channel_name` (str)
- **GET /api/search/messages?query=paracetamol&limit=20**
  - Searches for messages containing a specific keyword.
  - **Query Parameters:** `query` (str), `limit` (int, default 20)

### 🖼️ FastAPI Swagger UI Screenshots
<img width="1194" height="916" alt="top-products" src="https://github.com/user-attachments/assets/6c8bba03-fe31-46c2-95e9-fab3c705a97d" />
<img width="1191" height="921" alt="channel-activity" src="https://github.com/user-attachments/assets/6641b9e2-6456-4baf-b05a-3c39c30c84c1" />
<img width="1206" height="910" alt="search-messages" src="https://github.com/user-attachments/assets/bb6339c0-d99d-4b1c-ae78-fd96de865979" />
