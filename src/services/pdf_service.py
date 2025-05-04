from typing import Optional
import os
import PyPDF2
from models.schemas import Document
from config.settings import settings
from utils.logging_utils import logger

class PDFService:
    @staticmethod
    def extract_text(filepath: str) -> Optional[Document]:
        """Extract text from supported PDF files"""
        # Verify file extension first
        _, ext = os.path.splitext(filepath)
        if ext.lower() not in settings.SUPPORTED_FILE_TYPES:
            logger.error(f"Unsupported file type: {filepath}")
            return None

        try:
            text = ""
            with open(filepath, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    page_text = page.extract_text() or ""
                    if len(text) + len(page_text) > settings.MAX_TEXT_LENGTH:
                        text += page_text[:settings.MAX_TEXT_LENGTH - len(text)]
                        break
                    text += page_text
            
            #logger.info(f"Extracted {len(text)} chars from {os.path.basename(filepath)}")
            return Document(
                filename=os.path.basename(filepath),
                content=text,
                size=len(text)
            )
        except Exception as e:
            logger.error(f"Failed to process {filepath}: {str(e)}", exc_info=True)
            return None