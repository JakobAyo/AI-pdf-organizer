import google.generativeai as genai
from models.schemas import CategorySuggestion
from typing import List, Dict
from utils import print_utils
from utils.logging_utils import logger
import re
from pathlib import Path
from helper import load_json, load_config
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))

class AIService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def extract_invoice(self, invoice_text: List[Dict[str, str]]) -> List[Dict]:
        combined_text = "\n\n--- INVOICE BREAK ---\n\n".join(
            f"Document {i + 1} ({invoice.filename}):\n{invoice.content}..."
            for i, invoice in enumerate(invoice_text)
        )

        prompt_template = load_prompt("invoice_data.txt")
        prompt = prompt_template.format(
            combined_text=combined_text,
            invoice_count=len(invoice_text),
        )

        try:
            response = self.model.generate_content(prompt)
            return self._parse_response(response.text)
        except Exception as e:
            logger.error(f"AI API Error: {e}")
            return []

    def categorize_invoice(self, number_of_categories):
        invoices = load_json(load_config()["folder_path"], "invoices")
        self.all_items = {}

        for index, invoice in enumerate(invoices):
            try:
                # print(f"{index:<10}{invoice["Item"]}")
                self.all_items.update({index: invoice["Item"]})
            except KeyError as e:
                logger.error(f"{print_utils.RED}KeyError{print_utils.ENDC} at {index}: {e}")

        prompt_template = load_prompt("categorize.txt")
        prompt = prompt_template.format(
            all_items=json.dumps(self.all_items),
            number_of_categories=number_of_categories,
            max_id=len(self.all_items)
        )

        try:
            response = self.model.generate_content(prompt)
            self.categories = self._parse_response(response.text)
            return self.categories
        except Exception as e:
            logger.error(f"AI API Error: {e}")
            return []

    def resuggest_categories(self, selected_categories):
        prompt_template = load_prompt("resuggest_categories.txt")
        prompt = prompt_template.format(
            all_items=json.dumps(self.all_items),
            selected_categories=selected_categories,
            number_of_selected_categories=len(selected_categories),
            current_categories=[category for category in self.categories],
            number_of_all_categories=len(self.categories)
        )

        try:
            response = self.model.generate_content(prompt)
            self.categories = self._parse_response(response.text)
            return self.categories
        except Exception as e:
            logger.error(f"AI API Error: {e}")
            return []

    def _parse_response(self, text: str) -> List[CategorySuggestion]:
        try:
            cleaned = text.strip()

            cleaned = re.sub("```json\n", "", cleaned)
            cleaned = re.sub("```", "", cleaned)

            return json.loads(cleaned.strip())
        except json.JSONDecodeError as je:
            logger.error(f"Failed to parse cleaned JSON: {je}")
            logger.info(text)
            return []
        except Exception as e:
            logger.error(f"Unexpected error during JSON parsing: {e}")
            logger.info(text)
            return []


def load_prompt(prompt):
    prompt_path = os.path.join(project_root, "src", "prompts", prompt)
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"⚠️ Prompt file '{prompt}' not found.")
