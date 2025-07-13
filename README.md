# Telegram Data Scraper

This tool scrapes messages and media (images, videos, audio) from public Telegram channels relevant to Ethiopian medical businesses. It is designed for robust, incremental, and configurable data collection as part of a modern data pipeline.

## Features
- **Incremental scraping**: Only new messages are scraped on each run (checkpointed per channel).
- **Partitioned storage**: Messages and media are saved in date- and channel-based folders.
- **Image & media downloading**: Downloads images, videos, and audio, with deduplication and MIME type filtering.
- **Robust logging**: Logs scraping progress, errors, and summary statistics.
- **Configurable**: Channel list, date range, keywords, and media types are all configurable.
- **Parallel scraping**: Optionally scrape multiple channels in parallel.
- **Message filtering**: Optionally filter messages by keywords.

## Setup
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure Telegram API credentials**
   - Create a `.env` file with:
     ```env
     TELEGRAM_API_ID=your_api_id
     TELEGRAM_API_HASH=your_api_hash
     TELEGRAM_SESSION=anon
     ```
3. **Prepare channel list**
   - Edit `channels.txt` and add one Telegram channel URL per line.

## Usage
Run the scraper with your desired options. Example:

```bash
python scrape_telegram.py \
  --channels channels.txt \
  --start-date 2024-07-01 \
  --end-date 2024-07-10 \
  --keywords paracetamol cream pill \
  --image-types image/jpeg image/png \
  --parallel
```

### Arguments
- `--channels`: Path to the channel list file (default: `channels.txt`)
- `--start-date`: Start date for scraping (format: YYYY-MM-DD)
- `--end-date`: End date for scraping (format: YYYY-MM-DD)
- `--keywords`: (Optional) Only scrape messages containing these keywords
- `--image-types`: (Optional) Only download images of these MIME types
- `--parallel`: (Optional) Enable parallel scraping of channels

## Output
- **Messages**: `data/raw/telegram_messages/YYYY-MM-DD/channel_name.json`
- **Images/Media**: `data/raw/telegram_images/YYYY-MM-DD/channel_name/`
- **Checkpoints**: `data/raw/checkpoints/channel_name.json`
- **Logs**: `logs/scraping.log`

## Notes
- The scraper is robust to interruptions and can be resumed at any time.
- Make sure your Telegram API credentials are valid and you have access to the listed channels.
- For large numbers of channels, use `--parallel` with care to avoid Telegram rate limits.

--- 