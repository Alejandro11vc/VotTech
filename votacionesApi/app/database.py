import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

def getDatabase():
    uri = os.getenv("MONGO_URI")
    dbVotociones = os.getenv("MONGO_DB", "voting_db")

    if not uri:
        raise ValueError("Falta la variable MONGO_URI en el archivo .env")

    client = MongoClient(uri)
    db = client[dbVotociones]
    return db
