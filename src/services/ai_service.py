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

    def _parse_response(self, text: str) -> List[CategorySuggestion]:
        # Implementation of response parsing
        self.categories = re.findall(r'^\d.*', text, re.MULTILINE)

        for i, category in enumerate(self.categories):
            category = category.replace("*", " ")
            category = category.split(".")
            category = category[1].strip()
            self.categories[i] = category
        
        return self.categories