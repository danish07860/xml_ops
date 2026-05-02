import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    INPUT_PATH = os.getenv("INPUT_PATH", "data/raw/customers_100.xml.gpg")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH", "data/processed/")
    GPG_PASSPHRASE = os.getenv("GPG_PASSPHRASE")