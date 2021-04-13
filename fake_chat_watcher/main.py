"""
Fake app meant to replicate a chat watcher locally
This is meant to run in conjuction w/ a redis
"""
# Builtins
from random import randrange
import time
# Packages
import redis
# Local imports

TWITCH_MESSAGES = [
    "PogChamp",
    "Kappa",
    "Keepo"
]

if __name__ == "__main__":
    hostname = '0.0.0.0'
    print(f"Attempting to connect to redis at: {hostname}")
    rdb = redis.Redis(host=hostname, port=6379, db=0)
    while True:
        # TODO: Send these to Redis instead smiley face
        message = TWITCH_MESSAGES[randrange(len(TWITCH_MESSAGES))]
        print(f"{message}")
        try:
            rdb.incr(message, 1)
        except redis.exceptions.ConnectionError:
            print("ERROR CONNECTING TO REDIS!")
        time.sleep(randrange(10, 20)/10)
