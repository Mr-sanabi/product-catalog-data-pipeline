import logging
import time
from pathlib import Path

def setup_logging():
    Path("logs").mkdir(parents=True, exist_ok=True)

    logging.Formatter.converter = time.gmtime

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)sZ (%(levelname)s) %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        handlers=[
            logging.FileHandler("logs/log.txt", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
