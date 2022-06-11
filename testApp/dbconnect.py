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
        res['id'] = res['_id']
    elif all:
        res = list(collection.find(params))
        for i in res:
            i["id"] = i["_id"]
    else:
        raise ValueError("incorrect value")
    return res


def write_data(collection_name, data):
    db, cl = init_db()
    collection = db[collection_name]
    collection.insert_one(data)
    cl.close()


t = get_data('products', params={"_id": ObjectId('62a2fe743741a7075625e227')})
print(t)
