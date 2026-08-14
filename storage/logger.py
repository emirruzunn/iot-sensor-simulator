import os
import csv
import json

def save_to_csv(records: list[dict], path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    file_exists = os.path.isfile(path)
    
    with open(path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["sensor_id", "timestamp", "temperature", "humidity", "battery"])
        if not file_exists:
            writer.writeheader()
        writer.writerows(records)

def save_to_json(records: list[dict], path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    existing_data = []
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []
            
    existing_data.extend(records)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4)