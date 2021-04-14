# twitch-emote-tracker
Emote tracking webapp to visualize Twitch emote usage.

# Running locally
Run the docker-compose:
```
docker-compose -f docker-compose-test.yml up -d
```

To stop services (on windows, my condolances for macOS):

```
# list all docker containers
docker ps -a

# stop all running containers
docker stop $(docker ps -a -q)

# remove all containers
docker rm $(docker ps -a -q)
```

# Current functioning components:
### Fake chat watcher bot
- Very simple prototype for actual twitch chat watcher bot
- Picks 1 of 3 keys randomly
- The key is sent to redis in the form of an INCR command, to ++ the count for that emote
- The actual chat watcher has some extra logic to match the words in a chat message to valid emote names
### Redis cached storage
- Runs from standard redis image on dockerhub
- Uses a `redis.conf` file to allow for outside connections
  - This seems to be a *security risk*! So will need to be changed in the future?

# TODO
### Bot manager
- There is currently a test/scratch file `fake_chat_watcher/bot_manager.py` that spins up fake chat watcher images. 
- The goal is to have the bot manager be able to start/stop bots as needed based on popular streams.
- This will probably be called in the `docker-compose-test.yml` instead of just running 1 chat watcher and connecting it to redis.
### mongoDB persistent database
- This will periodically read from the redis cache and increment any new emote counts to existing emote counts
### Node/Express back-end
- This will read from the database to obtain emote counts
- Will clear redis cache after the database reads from it
- Also will create webpage for now using EJS (to be eventually replaced by an actual front-end)
