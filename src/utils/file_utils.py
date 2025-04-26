import os
from config.settings import settings
from typing import List
from utils.logging_utils import logger

class FileUtils:
    @staticmethod
    def get_supported_files(folder_path: str) -> List[str]:
        """Get all supported files from a directory"""
        if not os.path.exists(folder_path):
            logger.error(f"Directory not found: {folder_path}")
            raise FileNotFoundError(f"Folder not found: {folder_path}")
        
        supported_files = []
        for f in os.listdir(folder_path):
            file_path = os.path.join(folder_path, f)
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(f)
                if ext.lower() in settings.SUPPORTED_FILE_TYPES:
                    supported_files.append(file_path)
                else:
                    logger.debug(f"Skipping unsupported file type: {f}")
        
        if not supported_files:
            logger.warning(f"No supported files found in {folder_path}")
        
        return supported_files