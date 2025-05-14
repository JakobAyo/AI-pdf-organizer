import google.generativeai as genai
from models.schemas import CategorySuggestion, Document
from config.settings import settings
from typing import List
from utils.logging_utils import logger
import re

class AIService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.categories = []

    def suggest_categories(self, documents: List[Document]) -> List[CategorySuggestion]:
        combined_text = "\n\n--- DOCUMENT BREAK ---\n\n".join(
            f"Document {i+1} ({doc.filename}):\n{doc.content[:5000]}..."
            for i, doc in enumerate(documents)
        )
        
        prompt = f"""
        Analyze the following {len(documents)} documents and categorize them into exactly {settings.NUM_CATEGORIES} distinct, logical categories.

        Requirements:

        Categories must be mutually exclusive (no document should fit into multiple categories).

        Categories should be clearly named based on common themes, topics, or patterns.

        Every document must be assigned to one category.

        Output Format:
        Strictly adhere to this structure for each category:

        1. [Category Name]  
        - Documents: [comma-separated list of document numbers (1-{len(documents)})]  
        
        Documents to Analyze:
        {combined_text}

        Additional Notes:

        Prioritize clarity and relevance in category names (e.g., "Healthcare Policy" over "General Topics").

        Do not introduce subcategories or additional sections beyond the specified format.
        """
        
        try:
            response = self.model.generate_content(prompt)
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
        categories = re.findall(r'^\d.*', text, re.MULTILINE)

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
        self.categories = [item if item not in selected_categories else "None" for item in self.categories]
