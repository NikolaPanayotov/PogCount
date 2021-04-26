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

# to rebuild fake_chat_watcher (must be in fake_chat_watcher dir)
docker build -t fake-chat-watcher .

# to open redis CLI while container is running
docker exec -it <redis_containerID> redis-cli
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
  - This seems to be a **security risk!** So will need to be changed in the future?
### Data migrator
- Python file which reads from redis cache, clears it, and writes to mongoDB for persistent storage
### mongoDB persistent database
- Persistent storage containing counts for all emotes
### Node/Express back-end
- Reads from mongoDB to obtain emote counts
- Will create webpage for now using EJS (to be eventually replaced by an actual front-end)
### Realtime data streaming
- Backend subscribes for change events from DB
- Backend sends an event to frontend asynchronously


# TODO
### Bot manager
- There is currently a test/scratch file `fake_chat_watcher/bot_manager.py` that spins up fake chat watcher images. 
- The goal is to have the bot manager be able to start/stop bots as needed based on popular streams.
- This will probably be called in the `docker-compose-test.yml` instead of just running 1 chat watcher and connecting it to redis.
