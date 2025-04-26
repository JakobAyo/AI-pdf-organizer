import google.generativeai as genai
from models.schemas import CategorySuggestion, Document
from config.settings import settings
from typing import List
from utils.logging_utils import logger

class AIService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        print(genai.list_models())
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def suggest_categories(self, documents: List[Document]) -> List[CategorySuggestion]:
        combined_text = "\n\n--- DOCUMENT BREAK ---\n\n".join(
            f"Document {i+1} ({doc.filename}):\n{doc.content[:5000]}..."
            for i, doc in enumerate(documents)
        )
        
        prompt = f"""Analyze these {len(documents)} documents and suggest exactly {settings.NUM_CATEGORIES} logical categories.
        For each category provide:
        - A clear name
        - Description
        - Which documents belong there (by number 1-{len(documents)})
        
        Documents:
        {combined_text}
        
        Respond in this exact format:
        1. [Category Name]
        - Description: [description]
        - Documents: [comma-separated numbers]
        ..."""
        
        try:
            response = self.model.generate_content(prompt)
            # return self._parse_response(response.text)
            return response.text
        except Exception as e:
            logger.error(f"AI API Error: {e}")
            return []

    def _parse_response(self, text: str) -> List[CategorySuggestion]:
        # Implementation of response parsing
        pass