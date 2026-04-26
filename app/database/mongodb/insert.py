import traceback
from datetime import datetime
from bson import ObjectId
from pymongo.collection import Collection

from app.database.mongodb.init import 
from app.utilities.logger import logging


def insert_document(document: dict, collection: Collection) -> str | None:
    try:
        document_copy = document.copy()

        now = datetime.now()
        document_copy["createdAt"] = now
        document_copy["updatedAt"] = now

        doc_id = collection.insert_one(document_copy)
        logging.info("✅ Document inserted successfully.")
        return str(doc_id.inserted_id)

    except Exception as e:
        logging.info(f"❌ Error inserting document: {e}")
        return None

