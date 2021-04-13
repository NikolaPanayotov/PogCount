import docker
import time

client = docker.from_env()
print("Starting up first container...")
client.containers.run('fake-chat-watcher:latest', detach=True)
print(f"{len(client.containers.list())} containers up!")
client.containers.run('fake-chat-watcher:latest', detach=True)
print(f"{len(client.containers.list())} containers up!")
print("Stopping containers in 3 seconds...")
time.sleep(3)
for container in client.containers.list():
    print(f"Stopping container {container}")
    container.kill()
print(f"{len(client.containers.list())} containers up!")
