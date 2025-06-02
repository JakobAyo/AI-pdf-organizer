import pytest
from src.utils.organizer_util import InvoiceOrganizer
from pathlib import Path
from src.helper import load_json

def test_create_dir():
    InvoiceOrganizer.create_folders()
    InvoiceOrganizer.move_to_folders()
