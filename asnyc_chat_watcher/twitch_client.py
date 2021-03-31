import asyncio
import logging
import time

from websockets import connect


logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

class TwitchChatClient:

    TWITCH_CHAT_URL = 'wss://irc-ws.chat.twitch.tv:443'
    CAP_REQ = 'CAP REQ :twitch.tv/tags twitch.tv/commands twitch.tv/membership'
    NICK = 'NICK justinfan31337'
    CHANNEL = 'JOIN #{channel}'

    async def __aenter__(self):
        self._conn = connect(self.TWITCH_CHAT_URL)
        self.websocket = await self._conn.__aenter__()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self._conn.__aexit__(*args, **kwargs)

    async def send(self, message):
        await self.websocket.send(message)

    async def receive(self):
        return await self.websocket.recv()


class TwitchManager:
    def __init__(self, channel):
        logger.info(f"Instatiating TwitchManager for {channel}")
        self.channel = channel
        self.twich_channel = TwitchChatClient()
        # self.loop = asyncio.get_event_loop()

    def parse_message(self, message):
        """
        Parses a twitch message
        :param message:
        :return:

        @badge-info=subscriber/16;badges=moderator/1,subscriber/12,bits-charity/1;color=#BF8C3F;display-name=Evanito;emotes=111700:16-24;flags=;id=2472002c-c974-4b91-bac8-8490623d798a;mod=1;room-id=60978448;subscriber=1;tmi-sent-ts=1598306044470;turbo=0;user-id=71602891;user-type=mod :evanito!evanito@evanito.tmi.twitch.tv PRIVMSG #dogdog :@Ralth_ neither DatSheffy

        """

        try:
            message_content = message.split(f'PRIVMSG #{self.channel} :')[1]
        except IndexError:
            message_content = None
        return TwitchMessage(message, message_content)


    def get_messages(self):
        return self.loop.run_until_complete(self._async_get_messages())
        # return self.loop.run_in_executor(None,func=self.__async__get_messages)

    async def _async_get_messages(self):
        print(f"HELLO ASYNC WORLD")
        async with self.twich_channel as twitch:
            print(f"WOAAHH")
            logger.info("Sending CAP")
            await twitch.send(twitch.CAP_REQ)
            logger.info("Sending NICK")
            await twitch.send(twitch.NICK)
            logger.info("Joining CHANNEL")
            await twitch.send(twitch.CHANNEL.format(channel=self.channel))
            while True:
                message = await twitch.receive()
                logger.info(self.parse_message(message))



class TwitchMessage:
    def __init__(self, raw_message, message_content):
        self.raw_message = raw_message
        self.message_content = message_content

    def __str__(self):
        return self.message_content or self.raw_message