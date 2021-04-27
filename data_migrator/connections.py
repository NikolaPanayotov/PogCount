import redis
import pymongo
import time


def redisConnect(hostname, port, db):
    return redis.Redis(host=hostname, port=port, db=db)


def mongoConnect(hostname, replicaname):
    mongoClient = None
    while mongoClient is None:
        try:
            mongoClient = pymongo.MongoClient(
                host=hostname,
                serverSelectionTimeoutMS=3000,  # 3 second timeout
                replicaSet=replicaname
                # username='root',
                # password='rootpassword',
            )
        except pymongo.errors.ServerSelectionTimeoutError as err:
            # set the client and DB name list to 'None' and `[]` if exception
            mongoClient = None
            print(f"Error connecting to mongoDB: {err}")
            print("Retrying in 5 seconds...")
            time.sleep(5)
    return mongoClient
