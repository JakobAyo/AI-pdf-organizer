import pytest
import os
from pathlib import Path

categories = Path(__file__).parent.parent / "categories.json"

def test_path():
    assert(str(categories) == "/home/jaco/Projects/AI-pdf-organizer/categories.json")

