import os
import logging

# Log config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("server_logger.log"),  # Save to file
        logging.StreamHandler(),  # Also print to console
    ],
)

logger = logging.getLogger(__name__)


# Helper to set up a logger for a specific mongo_id
def setup_mongo_id_logger(mongo_id: str) -> logging.Logger:
    logger = logging.getLogger(f"mongo_{mongo_id}")
    if not logger.handlers:  # Avoid duplicate handlers
        os.makedirs("logs", exist_ok=True)  # Create logs directory if it doesn't exist
        file_handler = logging.FileHandler(f"logs/{mongo_id}.log")
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
    return logger