import redis
import pymongo
import time

hostname = 'redis'
rdb = redis.Redis(host=hostname, port=6379, db=0)

mongoClient = None
# Initialize mongoDB connection
while mongoClient is None:
    try:
        mongoClient = pymongo.MongoClient(
            host='mongo:27017',
            serverSelectionTimeoutMS=3000,  # 3 second timeout
            username='root',
            password='rootpassword',
        )
    except pymongo.errors.ServerSelectionTimeoutError as err:
        # set the client and DB name list to 'None' and `[]` if exception
        mongoClient = None
        database_names = []
        print(f"Error connecting to mongoDB: {err}")
        print("Retrying in 5 seconds...")
        time.sleep(5)

mdb = mongoClient.pogcount
emotesCollection = mdb["emoteCounts"]

while True:
    # Iterate through all keys in redis
    try:
        for key in rdb.scan_iter():
            # Save the current value and clear redis for the key
            emoteCount = rdb.get(key)
            key = key.decode('utf-8')
            emoteCount = int(emoteCount)
            print(f"Key type: {type(key)} // Value type: {type(emoteCount)}")
            print(f"Migrator: {key} -- {emoteCount}")
            rdb.set(key, 0)
            emotesCollection.update_one({'name': key},
                                        {'$setOnInsert': {'name': key},
                                         '$inc': {'count': emoteCount}},
                                        upsert=True)
            # mdb.pogcount.update({'emote': key}, {'$inc': {'item': 1}})
            # Write value to mongo[key] = value
    except redis.exceptions.ConnectionError:
        print('ERROR CONNECTING TO REDIS!')
    time.sleep(1)
