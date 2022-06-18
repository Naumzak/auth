import pymongo
from  bson.objectid import ObjectId

def init_db():
    db_client = pymongo.MongoClient('mongodb://localhost:27017')
    current_db = db_client['shopdb']
    # collection = current_db['products']
    return current_db, db_client


def get_data(collection_name, params=None, all=False):
    db, cl = init_db()
    collection = db[collection_name]
    if not all:
        res = collection.find_one(params)
    elif all:
        res = list(collection.find(params))
    else:
        raise ValueError("incorrect value")
    return res


def write_data(collection_name, data):
    db, cl = init_db()
    collection = db[collection_name]
    collection.insert_one(data)
    cl.close()
