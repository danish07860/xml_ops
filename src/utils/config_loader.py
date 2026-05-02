import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    INPUT_PATH = os.getenv("INPUT_PATH", "data/raw/")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH", "data/processed/")
