# twitch-emote-tracker
Emote tracking webapp to learn Twitch API

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