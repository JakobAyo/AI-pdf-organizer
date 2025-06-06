from typing import List
import json
import os

def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """Helper to split a list into chunks"""
    return[lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def save_json(root_dir, data, filename):
    output_path = f"{root_dir}/{filename}.json"
    with open(output_path, "w") as f:
        json.dump(data, f)

def load_json(root_dir, filename):
    path = f"{root_dir}/{filename}.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "config", "config.json")
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return {}

def save_config(config_data):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "config", "config.json")

    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=4)


