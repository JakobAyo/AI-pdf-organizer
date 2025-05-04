from services.pdf_service import PDFService
from services.ai_service import AIService
from utils.file_utils import FileUtils
from config.settings import settings
from dotenv import load_dotenv
import os

load_dotenv()
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

def main():
    # Initialize components
    pdf_service = PDFService()
    file_utils = FileUtils()

    # Get inputs
    folder_path = os.path.join(os.getcwd(), 'PDF_files')
    api_key = os.getenv("API_KEY")
    ai_service = AIService(api_key)
    
    try:
        # Get and process files
        files = file_utils.get_supported_files(folder_path)
        documents = [pdf_service.extract_text(f) for f in files]
        valid_docs = [doc for doc in documents if doc]
        
        # Get suggestions
        suggestions = ai_service.suggest_categories(valid_docs)
        
        # Output results
        print("\n=== Suggested Categories ===")
        print(suggestions)
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion.name}")
            print(f"   - {suggestion.description}")
            print(f"   - Includes documents: {', '.join(map(str, suggestion.document_ids))}\n")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
