import re
import pytest
from pathlib import Path
from src.services.ai_service import AIService
from src.config.settings import settings
from dotenv import load_dotenv
import os

load_dotenv()

@pytest.fixture
def invoices_in():
    file_path = Path("tests") / "invoices_in.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

@pytest.fixture
def invoices_out():
    file_path = Path("tests") / "invoices_out.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

@pytest.fixture
def categories_in():
    file_path = Path("tests") / "categories_in.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

@pytest.fixture
def categories_out():
    file_path = Path("tests") / "categories_out.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

@pytest.fixture
def ai_service():
    return AIService(os.getenv("API_KEY"))

def test_parse_returns_list(ai_service, invoices_in):
    invoices_parse = ai_service._parse_response(invoices_in)
    categories_parse = ai_service._parse_response(categories_in)
    assert(str(invoices_parse) != [])
    assert(str(categories_parse) != [])

