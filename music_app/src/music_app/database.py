from typing import Any

from pymongo import MongoClient

HOST = 'localhost'
PORT = 27017

def init_client() -> MongoClient[dict[str, Any]]:
    return MongoClient(HOST, PORT)
