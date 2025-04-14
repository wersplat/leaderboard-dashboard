# 🔍 OCR Backend – DiscordStatBot (v2.0)

This module powers the OCR and stat extraction pipeline for DiscordStatBot. It uses FastAPI to receive box score images, runs OCR using Tesseract, parses player stat lines, and normalizes the data for export and leaderboard tracking.

---

## 🧠 Responsibilities

- Accept images via `/ocr` POST endpoint
- Extract raw text with `ocr_engine.py`
- Parse text into structured stats using `parser.py`
- Normalize names and calculate MVPs with `normalizer.py`
- Deduplicate using a stat hash
- Index each game to `games_index.json`
- Save backups to JSON and CSV
- Push clean data to Google Sheets

---

## 📦 Modules

- `app.py` – FastAPI server and `/ocr` route
- `ocr_engine.py` – Image processing and Tesseract OCR
- `parser.py` – Converts OCR text into game stats
- `normalizer.py` – Cleans names, stats, and resolves MVP
- `dedup.py` – Prevents duplicate uploads
- `indexer.py` – Tracks game metadata in `games_index.json`

---

## 🔁 Data Flow

1. Image uploaded from Discord or dashboard
2. `/ocr` route runs OCR → parse → normalize
3. Hash checked for duplicates
4. Valid game saved as JSON/CSV
5. Game indexed and pushed to Sheets

---

## 🔧 Requirements

- `pytesseract`
- `Pillow`
- `FastAPI`
- `python-multipart`
- Tesseract must be installed and in your PATH

---

## 🔗 Consumed By

- 📥 `dashboard/upload.py` for manual review + confirm
- 🤖 `bot/commands.py` and `admin.py` for Discord flow
- 📊 `dashboard/leaderboard.py` and `/games/` views

---

## 🧪 Testing Locally

Start the OCR API locally:
```bash
uvicorn ocr_backend.app:app --reload
```

Send an image POST to `/ocr` from curl, Postman, or the bot.
```
