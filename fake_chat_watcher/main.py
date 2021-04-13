"""
Fake app meant to replicate a chat watcher locally
This is meant to run in conjuction w/ a redis
"""

from random import randrange
import time

TWITCH_MESSAGES = [
    "PogChamp",
    "Kappa Kappa KAPPA",
    "INJOKER 420"
]

if __name__ == "__main__":
    while True:
        # TODO: Send these to Redis instead smiley face
        print(TWITCH_MESSAGES[randrange(len(TWITCH_MESSAGES))])
        time.sleep(randrange(10, 20)/10)
