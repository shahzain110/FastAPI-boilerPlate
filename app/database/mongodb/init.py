import pymongo
from app.configs.models import env_var

client = pymongo.MongoClient(env_var.mongo_string)

db = client["prod"]

keys_collection = db["keys"]