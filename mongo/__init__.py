
from main import config
import pymongo
from pymongo import MongoClient


from mongo.crud import MongoCRUD

# 数据库前缀
DB_PREFIX = config.get("sys").get("db_prefix")
mdb = MongoClient(**config.get("sys").get("mongoDb"))


def get_db(module):
    return mdb[DB_PREFIX + module]

CRUD = MongoCRUD