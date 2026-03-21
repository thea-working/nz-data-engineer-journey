import json
import logging
from pathlib import Path

import requests

logger = logging.getLogger(__name__)


class APIIngestion:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self):
        logger.info("Requesting API data from %s", self.api_url)

        response = requests.get(self.api_url)

        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code}")

        data = response.json()
        logger.info("Fetched %d records from API", len(data))

        return data

    def save_json(self, data, output_path: Path):
        output_path.mkdir(parents=True, exist_ok=True)
        output_file = output_path / "api_posts.json"
        logger.info("Saving API data to %s", output_file)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        logger.info("Saving API data successfully")
