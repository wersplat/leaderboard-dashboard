from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import io
from PIL import Image
from ocr_engine import run_ocr
from parser import parse_stat_block  # NEW
from normalizer import clean_and_normalize_ocr_data
from sheets.sheets_api import append_stats_to_sheet
from datetime import datetime
import json, os
import csv
from dedup import compute_stat_hash, is_duplicate, record_game
from indexer import append_to_index, build_game_index_entry
import logging

logger = logging.getLogger("ocr_backend")

app = FastAPI()

class ImageRequest(BaseModel):
    image_url: str

@app.post("/ocr")
async def ocr_endpoint(request: ImageRequest):
    try:
        # Download the image from Discord CDN
        response = requests.get(request.image_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to download image.")

        image_data = io.BytesIO(response.content)
        img = Image.open(image_data)

        # Run OCR
        ocr_text = run_ocr(img)

        # Parse the OCR text
        parsed_result = parse_stat_block(ocr_text)
        parsed_result = clean_and_normalize_ocr_data(parsed_result)
        stat_hash = compute_stat_hash(parsed_result)
        if is_duplicate(stat_hash):
            logger.warning(f"Duplicate game detected. Hash: {stat_hash}")
            raise HTTPException(status_code=409, detail="Duplicate game detected. This game was already processed.")
        mvp_tag = parsed_result['mvp']['name'][:4].replace(" ", "") or "ID"
        timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M")
        game_id = f"Game-{mvp_tag}-{timestamp}"
        record_game(stat_hash, game_id)
        append_to_index(build_game_index_entry(game_id, stat_hash, request.image_url, source="discord"))

        os.makedirs("data/games", exist_ok=True)
        json_path = f"data/games/{game_id}.json"
        with open(json_path, "w") as f:
            json.dump(parsed_result, f, indent=2)
        
        csv_path = f"data/games/{game_id}.csv"
        with open(csv_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Team", "Player", "PTS"])
            for player in parsed_result["team1"]:
                writer.writerow(["Team 1", player["name"], player["pts"]])
            for player in parsed_result["team2"]:
                writer.writerow(["Team 2", player["name"], player["pts"]])
            writer.writerow([])
            writer.writerow(["Winner", parsed_result["winner"]])
            writer.writerow(["MVP", parsed_result["mvp"]["name"], parsed_result["mvp"]["line"]])

        try:
            append_stats_to_sheet(parsed_result, game_id)
        except Exception as e:
            print(f"Failed to append to {game_id}: {e}")

        try:
            append_stats_to_sheet(parsed_result, "AllGames")
        except Exception as e:
            print(f"Failed to append to AllGames tab: {e}")

        return parsed_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")