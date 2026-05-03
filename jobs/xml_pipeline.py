import sys
import os

# add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ingestion.load_xml import load_xml, get_spark
from src.ingestion.decrypt_gpg import decrypt_auto
from src.utils.config_loader import Config
from src.processing.dq_checks import apply_dq_rules, generate_dq_report, split_data


def run():
    print("🚀 Starting XML pipeline...")

    # 🔐 Step 1: Decrypt
    decrypted_file = decrypt_auto(
        Config.INPUT_PATH,
        Config.GPG_PASSPHRASE
    )

    # 📂 Step 2: Load
    df = load_xml(decrypted_file)

    print("\n📊 Schema:")
    df.printSchema()

    print("\n👀 Sample data:")
    df.show(5, truncate=False)

    # 🔥 Step 3: Apply DQ
    df_dq = apply_dq_rules(df)

    # 🔥 Step 4: Generate report
    dq_report = generate_dq_report(df_dq)

    print("\n📋 DQ REPORT:")
    for k, v in dq_report.items():
        print(f"{k}: {v}")

    # 🔥 Step 5: Split
    good_df, bad_df = split_data(df_dq)

    print("\n✅ Good records:")
    good_df.show(5)

    print("\n❌ Bad records:")
    bad_df.show(5)

    # 🚀 Step 6: Write outputs

    # ✔ GOOD XML
    good_df.coalesce(1).write \
        .mode("overwrite") \
        .format("xml") \
        .option("rootTag", "customers") \
        .option("rowTag", "customer") \
        .save("data/output/good_xml")

    # ✔ BAD XML
    bad_df.coalesce(1).write \
        .mode("overwrite") \
        .format("xml") \
        .option("rootTag", "customers") \
        .option("rowTag", "customer") \
        .save("data/output/bad_xml")

    # ✔ DQ JSON
    import json

    with open("data/output/dq_report/dq_report.json", "w") as f:
        json.dump(dq_report, f, indent=4)


if __name__ == "__main__":
    run()