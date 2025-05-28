from typing import List
import json

def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """Helper to split a list into chunks"""
    return[lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def save_json(root_dir, invoices):
    output_path = f"{root_dir}/invoices.json"
    with open(output_path, "w") as f:
        json.dump(invoices, f)
