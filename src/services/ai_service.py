import google.generativeai as genai
from models.schemas import CategorySuggestion, Document
from typing import List, Dict
from utils.logging_utils import logger
import re
from pathlib import Path
import json

class AIService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def suggest_categoreis(self, documents: List[Document]):
        pass

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
            logger.info(response.text)
            print(response.text)
            return self._parse_response(response.text)

            # return self._parse_response(response.text)
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
            return []
        except Exception as e:
            logger.error(f"Unexpected error during JSON parsing: {e}")
            return []

def load_prompt(prompt):
    prompt_path = Path("prompts") / f"{prompt}"
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"⚠️ Prompt file '{prompt}' not found.")
