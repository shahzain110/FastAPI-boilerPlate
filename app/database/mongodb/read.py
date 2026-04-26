import traceback
from bson import ObjectId

from app.database.mongodb.init import (
    article_brief_collection,
)
from app.modules.security.encodings_secrets import decrypt_v2
from app.utilities.logger import logging


def fetch_single_document(document_id: str) -> dict | None:
    try:
        document = article_brief_collection.find_one({"_id": ObjectId(document_id)})

        if document:
            logging.info("✅ Document fetched successfully.")
            # Convert ObjectId to string if needed
            document["_id"] = str(document["_id"])
            return document
        else:
            logging.info("⚠️ No document found with the given ID.")
            return None

    except Exception as e:
        logging.info(
            f"❌ Error fetching document: {e} \n Input document_id {document_id}"
        )
        traceback.print_exc()
        return None
