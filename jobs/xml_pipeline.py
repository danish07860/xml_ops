import sys
import os

# add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ingestion.load_xml import load_xml
from src.ingestion.decrypt_gpg import decrypt_auto
from src.utils.config_loader import Config


def run():
    print("🚀 Starting XML pipeline...")

    # 🔐 Step 1: Decrypt first
    decrypted_file = decrypt_auto(
        Config.INPUT_PATH,
        Config.GPG_PASSPHRASE
    )

    # 📂 Step 2: Load XML
    df = load_xml(decrypted_file)

    print("\n📊 Schema:")
    df.printSchema()

    print("\n👀 Sample data:")
    df.show(5, truncate=False)


if __name__ == "__main__":
    run()