import requests
import json
from datetime import datetime
from pathlib import Path

API_URL = "https://remoteok.com/api"
RAW_DATA_DIR = Path("data/raw")

def extract_remoteok_jobs():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    extraction_date = datetime.now().strftime("%Y_%m_%d")
    output_file = RAW_DATA_DIR / f"remoteok_{extraction_date}.json"

    headers = {
        "User-Agent": "global-data-careers-intelligence-platform"
    }

    try:
        response = requests.get(API_URL, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()

        payload = {
            "source": "RemoteOK",
            "extraction_date": datetime.now().isoformat(),
            "record_count": len(data),
            "data": data
        }

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=4, ensure_ascii=False)

        print(f"RemoteOK extraction successful: {output_file}")

    except requests.exceptions.RequestException as error:
        print(f"RemoteOK extraction failed: {error}")

if __name__ == "__main__":
    extract_remoteok_jobs()