from pymongo import MongoClient
from pymongo.collection import Collection
from dotenv import load_dotenv, find_dotenv
import os
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
# print("Loaded env variables:", os.getenv("MONGO_URI"))
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)


def get_database():
    """Return the main database"""
    return client["profile_db"]

def get_personal_info_collection() -> Collection:
    """Return the collection for personal information"""
    db = get_database()
    return db["persional_information"]



