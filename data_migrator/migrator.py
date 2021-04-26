import redis
import pymongo
import time

from connections import redisConnect, mongoConnect


def migrateData(rdb, mongo):
    mdb = mongo.pogcount
    emotesCollection = mdb["emoteCounts"]

    while True:
        # Iterate through all keys in redis
        try:
            for key in rdb.scan_iter():
                # Save the current value and clear redis for the key
                emoteCount = rdb.get(key)
                key = key.decode('utf-8')
                emoteCount = int(emoteCount)
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
        time.sleep(0.5)


def init_mongo(mongoConneciton):
    mdb = mongoConneciton.pogcount
    emotesCollection = mdb["emoteCounts"]
    # Get all twitch emotes through API
    # For each emote in the returned list:
        # create/update db entry with image, set count to 0, 
    #Done!


if __name__ == "__main__":
    redisHost = 'redis'
    redisPort = 6379
    redisDb = 0
    mongoHost = 'mongo1:27017,mongo2:27018,mongo3:27019'
    mongoSet = 'rs0'

    rdb = redisConnect(redisHost, redisPort, redisDb)
    mongo = mongoConnect(mongoHost, mongoSet)

    init_mongo(mongo)
    migrateData(rdb, mongo)
