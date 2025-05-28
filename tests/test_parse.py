import re
import pytest
from pathlib import Path
from src.services.ai_service import AIService
from src.config.settings import settings
import re

@pytest.fixture
def input_text():
    file_path = Path("tests") / "input.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

@pytest.fixture
def output_text():
    file_path = Path("tests") / "output.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

@pytest.fixture
def ai_service():
    return AIService(settings.API_KEY)

# def test_cleaning(input_text, output_text):
#     cleaned = input_text.strip()
#
#     cleaned = re.sub("```json\n", "", cleaned)
#     cleaned = re.sub("```", "", cleaned)
#
#     assert(cleaned == output_text)

def test_parse_returns_list(ai_service, input_text, output_text):
    result = ai_service._parse_response(input_text)
    print(result)
    assert(result != [])
    # assert(result == output_text)
