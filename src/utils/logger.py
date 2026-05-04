import logging
import os


def get_logger(name: str):
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # avoid duplicate logs
    if logger.handlers:
        return logger

    # 🔹 Format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # 🔹 File handler
    file_handler = logging.FileHandler("logs/pipeline.log")
    file_handler.setFormatter(formatter)

    # 🔹 Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger