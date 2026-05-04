import sys
import os

# 🔹 Add project root to path (keep minimal + safe)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from src.ingestion.load_xml import load_xml, get_spark
from src.ingestion.decrypt_gpg import decrypt_auto
from src.utils.config_loader import Config
from src.processing.dq_engine import apply_dq_rules_dynamic  # 🔥 upgraded
from src.processing.dq_checks import generate_dq_report, split_data
from src.utils.email_utils import send_dq_email
from src.utils.logger import get_logger

logger = get_logger(__name__)


def validate_config():
    """Fail fast if required configs missing"""
    required = [
        Config.INPUT_PATH,
        Config.GPG_PASSPHRASE,
        Config.EMAIL_SENDER,
        Config.EMAIL_PASSWORD,
        Config.EMAIL_RECEIVER
    ]

    if not all(required):
        raise ValueError("Missing required configuration values")


def write_outputs(good_df, bad_df, dq_report):
    """Handle all output writing"""
    import json

    logger.info("Writing XML outputs...")

    good_df.coalesce(1).write \
        .mode("overwrite") \
        .format("xml") \
        .option("rootTag", "customers") \
        .option("rowTag", "customer") \
        .save("data/output/good_xml")

    bad_df.coalesce(1).write \
        .mode("overwrite") \
        .format("xml") \
        .option("rootTag", "customers") \
        .option("rowTag", "customer") \
        .save("data/output/bad_xml")

    logger.info("Writing DQ report JSON...")

    os.makedirs("data/output/dq_report", exist_ok=True)

    with open("data/output/dq_report/dq_report.json", "w") as f:
        json.dump(dq_report, f, indent=4)

    logger.info("Output writing completed")


def run():
    spark = None

    try:
        logger.info("🚀 Pipeline started")

        # 🔹 Validate config early
        validate_config()

        # 🔹 Step 1: Decrypt
        logger.info("Decrypting input file...")
        decrypted_file = decrypt_auto(
            Config.INPUT_PATH,
            Config.GPG_PASSPHRASE
        )
        logger.info(f"Decrypted file: {decrypted_file}")

        # 🔹 Step 2: Load
        logger.info("Loading XML into Spark...")
        spark = get_spark()
        df = load_xml(decrypted_file)

        logger.info("Schema:")
        df.printSchema()

        # 🔹 Step 3: DQ (CONFIG-DRIVEN)
        logger.info("Applying DQ rules...")
        df_dq = apply_dq_rules_dynamic(df, "config/dq_rules.json")

        # 🔹 Step 4: Report
        logger.info("Generating DQ report...")
        dq_report = generate_dq_report(df_dq)
        logger.info(f"DQ Report: {dq_report}")

        # 🔹 Step 5: Split
        logger.info("Splitting good and bad records...")
        good_df, bad_df = split_data(df_dq)

        # 🔹 Step 6: Write
        write_outputs(good_df, bad_df, dq_report)

        # 🔹 Step 7: Notify
        logger.info("Sending email notification...")
        send_dq_email(
            dq_report,
            Config.EMAIL_SENDER,
            Config.EMAIL_RECEIVER,
            Config.EMAIL_PASSWORD
        )

        logger.info("✅ Pipeline completed successfully")

    except Exception:
        logger.error("❌ Pipeline failed", exc_info=True)
        raise

    finally:
        if spark:
            logger.info("Stopping Spark session...")
            spark.stop()


if __name__ == "__main__":
    run()