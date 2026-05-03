import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    INPUT_PATH = os.getenv("INPUT_PATH", "data/raw/customers_100.xml.gpg")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH", "data/processed/")
    GPG_PASSPHRASE = os.getenv("GPG_PASSPHRASE")
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")