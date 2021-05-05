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
            top20 = None
            try:
                top20 = get_top_channels(auth_token, 100)
            except OAuthError:
                print("Refreshing oauth token!")
                auth_token = get_twitch_oauth()
            except TwitchAPIError:
                print("New error!")
            if top20 is not None:
                bots = [container for container in client.containers.list()
                        if "chat-watcher" in str(container.image)]
                print(f"Current bots running: {bots}")
                for container in bots:
                    if container.name not in top20:
                        print("{container.name} is not in the top 20!"
                              "Removing chat watcher...")
                        container.kill()
                    else:
                        print("Already watching {container.name}!")
                        top20.remove(container.name)
                for channel in top20:
                    print(f"Watching {channel}...")
                    container_cmd = bot_command + channel
                    client.containers.run('chat-watcher:latest',
                                          name=channel,
                                          network=docker_network,
                                          detach=True,
                                          command=container_cmd)
                    print(f"{channel} container created!")
                print("Time to sleep!")
                time.sleep(15*60)
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
