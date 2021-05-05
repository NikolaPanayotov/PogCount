# PogCount
Webapp to visualize Twitch emote usage in realtime.

# Running locally
Run the docker-compose:
```
docker-compose -f docker-compose-test.yml up -d
```
Run the bot manager (must be in the bot_manager directory of the project):
```
python3 bot_manager.py
```

To stop services (on windows, my condolances for macOS):

```
# list all docker containers
docker ps -a

# stop all running containers
docker stop $(docker ps -a -q)

# remove all containers
docker rm $(docker ps -a -q)

# to open redis CLI while container is running
docker exec -it <redis_containerID> redis-cli
```

# Current functioning components:
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
### Chat watcher
- Python irc bot which connects to a stream chat and listens for any emotes
- Writes emotes found and # of emotes found to Redis cache
### Bot manager
- Standalone Python tool to be run in parallel with `docker-compose`
- Polls Twitch API every 15 min to get top 100 channels
- Controls creation and removal of standalone chat watcher Docker containers


# Future plans
- Deploy to site
- Add "current channels" to mongo to keep track of which channels are being used
- Keep track of emote usage per channel?
- Ability to select top 10, 100, 1000? channels and update the page
- More stats? Emotes per hour?
