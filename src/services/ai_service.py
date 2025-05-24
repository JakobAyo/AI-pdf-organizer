import google.generativeai as genai
from models.schemas import CategorySuggestion, Document
from config.settings import settings
from typing import List
from utils.logging_utils import logger
import re


class AIService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.categories = []

    def suggest_categories(self, documents: List[Document]) -> List[CategorySuggestion]:
        combined_text = "\n\n--- DOCUMENT BREAK ---\n\n".join(
            f"Document {i + 1} ({doc.filename}):\n{doc.content[:5000]}..."
            for i, doc in enumerate(documents)
        )

        # print(combined_text)

        prompt = f"""
        Prompt for Invoice Data Analysis & Categorization
        Objective: Analyze the {
            len(documents)
        } invoices to identify recurring patterns and suggest contextual categories based on the most frequent and relevant keys/values.

        Parameters:

        Number of categories : [{settings.NUM_CATEGORIES}] (strictly enforce this count)

        Task:
        Step 1 – Aggregate Analysis

        Scan all invoices to identify:

        - extract the most frequent keys and values (e.g Invoice Number, Balance, Date, Bill To, Ship To)
        
        - also the item and the quantity and rate and the total amount


        Step 2 – Per-Invoice Categorization
        For each invoice:

        Cross-reference its data (vendor, amount, descriptions) with the aggregated frequent keys/values.

        Assign exactly [{settings.NUM_CATEGORIES}] categories, prioritizing:

        Frequency: Categories tied to recurring vendors/keywords (e.g., "Cloud Services" if "AWS" is frequent).

        Specificity: Prefer granular labels (e.g., "IT Hardware Purchases" > "General Expenses").

        Amount Logic: Use amount ranges to infer context (e.g., "$5000" → "Equipment Purchase" vs. "$50" → "Office Supplies").

        Output Format:

        - in json format
        - only give the raw data of the response. skip the explaination.
        - dont miss any invoice. respond to all {len(documents)}

        [Invoice #number-of-invoice [
            Bill-to:
            Ship-to:
            Balance:
            Date:
            Item:
            quantity:
            Rate:
        ]
        ]
        """

        try:
            response = self.model.generate_content(prompt)
            print(response.text)
            return self._parse_response(response.text)
        except Exception as e:
            logger.error(f"AI API Error: {e}")
            return []

    def resuggest_categories(self, selected_categories):
        prompt = f"""
        from the {self.categories} the user didn't like these suggestions {selected_categories}
        could you resuggest some categories instead of the {selected_categories}

        Output Format:
        Strictly adhere to this structure for each category:
        
        1. [Category Name]

        only suggest on Category for {len(selected_categories)} unwanted Categories in the chronological
        order.
        """
        try:
            self.remove_categories(selected_categories)
            response = self.model.generate_content(prompt)
            return self._parse_response(response.text)
        except Exception as e:
            logger.error(f"AI API Error: {e}")
            return []

    def _parse_response(self, text: str) -> List[CategorySuggestion]:
        # Implementation of response parsing
        categories = re.findall(r"^\d.*", text, re.MULTILINE)

        for i, category in enumerate(categories):
            category = category.replace("*", " ")
            category = category.split(".")
            category = category[1].strip()
            categories[i] = category

        if self.categories:
            self.update_categories(categories)
        else:
            self.categories = categories

        return self.categories

    def update_categories(self, new_categories):
        # self.categories = [item if item !="None" else new_categories for item in self.categories]
        for i, category in enumerate(self.categories):
            if category == "None":
                self.categories[i] = new_categories[0]
                del new_categories[0]

    def remove_categories(self, selected_categories):
        self.categories = [
            item if item not in selected_categories else "None"
            for item in self.categories
        ]
