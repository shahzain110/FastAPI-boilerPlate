from datetime import datetime
import json
import os
import traceback
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from copy import deepcopy

from app.database.mongodb.init import (
    article_brief_collection,
    queue_collection,
    brands_collection,
    data_banks_collection,
)
from app.utilities.logger import logging


def update_article_briefs(document_id: str, update_fields: dict):
    try:
        now = datetime.now()
        update_fields_for_db = deepcopy(update_fields)
        update_fields_for_db["updatedAt"] = now

        result = article_brief_collection.update_one(
            {"_id": ObjectId(document_id)}, {"$set": update_fields_for_db}
        )

        if result.modified_count == 0:
            logging.info("⚠️ Document not modified!.")
        else:
            logging.info(f"✅ Document updated successfully : {document_id} ")

    except Exception as e:
        logging.info(f"❌ Error updating document: {e}")
        print(document_id, update_fields)


def find_update_queue(user_id):
    doc = queue_collection.find_one_and_update(
        {"user_id": user_id, "status": "queued"},
        {"$set": {"status": "processing"}},
        sort=[("createdAt", 1)],
    )

    return doc


def update_queue_status(id, updated_payload):

    doc = queue_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": updated_payload},
    )


def update_queue_documents(user_id):

    result = queue_collection.update_many(
        {"user_id": user_id, "status": "idle"}, {"$set": {"status": "queued"}}
    )

    docs = queue_collection.find({"user_id": user_id, "status": "queued"})

    return result, docs


def insert_or_update_document(document: dict) -> str | None:
    try:
        brand_id = str(document.get("brand_id"))

        # Find existing document with same brand_id
        existing = data_banks_collection.find_one({"brand_id": ObjectId(brand_id)})

        if not existing:
            print("inserting")
            # Update existing document and return updated doc
            inserted_id = data_banks_collection.insert_one(document).inserted_id
            return str(inserted_id)
        else:
            print("updating")
            updated_doc = data_banks_collection.find_one_and_update(
                {"brand_id": ObjectId(brand_id)},
                {"$set": document},
                return_document=ReturnDocument.AFTER,
            )
            return str(existing["_id"])

    except Exception as e:
        print(f"Error in insert_or_update_document: {e}")
        traceback.print_exc()
        return None


def update_function_usage(document_id, func_name: str, tokens: int, cost: float):
    """
    Update tokens & cost for a specific function inside a document (by article ID).
    If function already exists, increment values. Otherwise, create it.
    """
    result = article_brief_collection.update_one(
        {"_id": ObjectId(document_id)},  # find document by _id
        {
            "$inc": {
                f"llm_cost.{func_name}.tokens": tokens,
                f"llm_cost.{func_name}.cost": cost,
            }
        },
        upsert=True,  # create document if not exists (optional)
    )
    return result


def update_craw_status(brand_id, status):

    doc = brands_collection.find_one_and_update(
        {"_id": ObjectId(brand_id)},
        {"$set": {"status": status}},
        sort=[("createdAt", 1)],
    )

    return doc


def update_crawl_state(crawl_file, summary_file, doc_id):

    update_data = {}

    # Read crawl file
    if os.path.exists(crawl_file):
        with open(crawl_file, "r") as f:
            update_data["visited_links"] = json.load(f)

    # Read summary file
    if os.path.exists(summary_file):
        with open(summary_file, "r") as f:
            update_data["data_bank"] = json.load(f)

    # Nothing to update
    if not update_data:
        return None

    # Always update updatedAt
    update_data["updatedAt"] = datetime.now()

    result = data_banks_collection.find_one_and_update(
        {"_id": ObjectId(doc_id)},
        {
            "$set": update_data,
            "$setOnInsert": {"createdAt": datetime.now()},
        },
        upsert=True,
        return_document=True,
    )

    return result


def save_or_merge_payload(new_payload: dict, brand_id: str):
    brand_obj_id = ObjectId(brand_id)

    existing = data_banks_collection.find_one({"brand_id": brand_obj_id})

    if existing:
        # Merge databank array-by-array
        for section, new_items in new_payload["databank"].items():
            old_items = existing["databank"].get(section, [])
            existing["databank"][section] = old_items + new_items

        update_data = {"databank": existing["databank"], "updatedAt": datetime.now()}

        data_banks_collection.update_one(
            {"brand_id": brand_obj_id}, {"$set": update_data}
        )

        logging.info("✅ Existing payload updated successfully.")
        return update_data

    else:
        # Insert for the first time
        new_payload["brand_id"] = brand_obj_id
        new_payload["createdAt"] = datetime.now()
        new_payload["updatedAt"] = datetime.now()

        data_banks_collection.insert_one(new_payload)
        # logging.info("✅ New payload inserted.")
        return new_payload
