from typing import Optional
import os
import pdfplumber
from models.schemas import Document
from config.settings import settings
from utils.logging_utils import logger


class PDFService:
    @staticmethod
    def extract_text(filepath: str) -> Optional[Document]:
        """Extract text from supported PDF files using pdfplumber"""
        # Verify file extension first
        _, ext = os.path.splitext(filepath)
        if ext.lower() not in settings.SUPPORTED_FILE_TYPES:
            logger.error(f"Unsupported file type: {filepath}")
            return None

        try:
            text = ""
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    # Extract text with layout preservation
                    page_text = page.extract_text() or ""

                    # Check length limit
                    if len(text) + len(page_text) > settings.MAX_TEXT_LENGTH:
                        remaining = settings.MAX_TEXT_LENGTH - len(text)
                        text += page_text[:remaining]
                        break
                    text += page_text

            logger.info(
                f"Extracted {len(text)} chars from {os.path.basename(filepath)}"
            )
            return Document(
                filename=os.path.basename(filepath), content=text, size=len(text)
            )
        except Exception as e:
            logger.error(f"Failed to process {filepath}: {str(e)}", exc_info=True)
            return None
