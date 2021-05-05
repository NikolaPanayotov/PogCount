# Packages
import docker
from dotenv import load_dotenv
import time
# Local Imports
from twitch_errors import OAuthError, TwitchAPIError
from twitch_api import get_twitch_oauth, get_top_channels


if __name__ == "__main__":
    load_dotenv()
    client = docker.from_env()
    auth_token = get_twitch_oauth()
    bots = []
    bot_command = "python -u bot.py "
    docker_network = "twitch-emote-tracker_default"
    while True:
        try:
            top_channels = None
            try:
                top_channels = get_top_channels(auth_token, 100)
            except OAuthError:
                print("Refreshing oauth token!")
                auth_token = get_twitch_oauth()
            # For handling future errors TwitchAPI throws at me
            except TwitchAPIError:
                print("New error!")
            if top_channels is not None:
                # Only track docker images with "chat-watcher"
                bots = [container for container in client.containers.list()
                        if "chat-watcher" in str(container.image)]
                print(f"Current bots running: {bots}")
                for container in bots:
                    # Remove any non top-X channel bots
                    if container.name not in top_channels:
                        print("{container.name} is not in the top channels!"
                              "Removing chat watcher...")
                        container.kill()
                        container.remove()
                    # Preserve channel bots that stayed in top-X
                    else:
                        print("Already watching {container.name}!")
                        top_channels.remove(container.name)
                # Go through remaining channels and add new watchers
                for channel in top_channels:
                    print(f"Watching {channel}...")
                    container_cmd = bot_command + channel
                    # Attach to the docker network so bots can write to redis
                    client.containers.run('chat-watcher:latest',
                                          name=channel,
                                          network=docker_network,
                                          detach=True,
                                          command=container_cmd)
                    print(f"{channel} container created!")
                # Top-X channels will be updated every 15 min
                print("Time to sleep!")
                time.sleep(15*60)
        # Clean up containers whenever script is manually cancelled
        except KeyboardInterrupt:
            print("Cleaning up!")
            bots = [container for container in client.containers.list()
                    if "chat-watcher" in str(container.image)]
            for container in bots:
                print(f"Stopping {container.name}")
                container.kill()
                print(f"Removing {container.name}")
                container.remove()
            break
