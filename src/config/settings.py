# config/settings.py
class _Settings:
    def __init__(self):
        self.SUPPORTED_FILE_TYPES = ['.pdf']
        self.MAX_TEXT_LENGTH = 8000 
        self.NUM_CATEGORIES = 5

settings = _Settings()  # Singleton instance