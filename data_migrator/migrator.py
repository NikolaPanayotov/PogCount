import redis
import pymongo
import csv
import time
from pathlib import Path

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
                # print(f"Migrator: {key} -- {emoteCount}")
                rdb.set(key, 0)
                emotesCollection.update_one({'name': key},
                                            {'$setOnInsert': {'name': key},
                                            '$inc': {'count': emoteCount}},
                                            upsert=True)
        except redis.exceptions.ConnectionError:
            print('ERROR CONNECTING TO REDIS!')
        except pymongo.errors.ServerSelectionTimeoutError:
            print('ERROR WRITING TO MONGO!')
        time.sleep(0.2)


def init_mongo(mongoConneciton):
    mdb = mongoConneciton.pogcount
    emotesCollection = mdb['emoteCounts']
    csvLoc = str(Path(__file__).parent) + '/emote_starter.csv'
    csvFile = open(csvLoc)
    reader = csv.DictReader(csvFile)
    entries = []
    for row in reader:
        entry = {"name": row["name"],
                 "count": 0,
                 "imageUrl": row["imageUrl"]}
        entries.append(entry)
    res = 0
    while res == 0:
        try:
            db_resp = emotesCollection.insert_many(entries)
            res = db_resp.inserted_ids
        except pymongo.errors.ServerSelectionTimeoutError:
            print("Error with writing to Mongo! Retrying...")
    print("DB initialized!")
    return


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
