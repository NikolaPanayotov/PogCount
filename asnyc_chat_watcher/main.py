import asyncio
import logging
import time
import websockets

from twitch_client import TwitchManager

# # hello_world = input("Type a thing: ")
# t = TwitchManager('dogdog')
# t.get_messages()


async def get_twitch_chat(channel):
    print('1')
    t = TwitchManager(channel)
    print('2')
    asyncio.ensure_future(t._async_get_messages())
    print('3')

print(f"Hello!")

while True:
    command = input(f"Type some number: ")
    if command == "1":
        break
    else:
        print(f"Starting a twitch chat client for: {command}")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(get_twitch_chat(command))

print(f"Bye!")




