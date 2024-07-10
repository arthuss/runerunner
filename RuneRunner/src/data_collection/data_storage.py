# src/data_collection/data_storage.py
import json
import os
from datetime import datetime

class DataStorage:
    def __init__(self):
        self.base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "processed")
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def store_scraped_data(self, data):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{data['type']}_{timestamp}.json"
        filepath = os.path.join(self.base_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Data stored in {filepath}")