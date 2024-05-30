import urllib.parse
from pymongo import MongoClient
from core.config import settings

client = MongoClient(
    host=settings.MONGO_HOST,
    port=settings.MONGO_PORT,
    username=urllib.parse.quote_plus(settings.MONGO_USER),
    password=urllib.parse.quote_plus(settings.MONGO_PWD),
)

client_dev = MongoClient(
    host=settings.MONGO_HOST_DEV,
    port=settings.MONGO_PORT_DEV,
    username=urllib.parse.quote_plus(settings.MONGO_USER_DEV),
    password=urllib.parse.quote_plus(settings.MONGO_PWD_DEV),
)