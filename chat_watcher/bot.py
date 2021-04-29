# Packages
import socket
import re
import redis
# Local imports
from emotes import emotes


class chatWatcher(object):
    """Single instance of a bot to join a channel and read chat.

    :username: username of twitch account used to connect to chat
    :token: oauth token associated with twitch account
    :channel: channel to connect to

    """
    def __init__(self, username, token, channel):
        self.username = username
        self.token = token
        self.channel = '#' + channel
        self.port = 6667
        self.server = 'irc.chat.twitch.tv'
        self.sock = None
        self.emotes = emotes
        self.rdb = None

    def joinChat(self):
        """Connect to channel specified in the chatWatcher object.

        Returns:
            socket: socket object representing connection to irc chat
        """
        sock = socket.socket()
        sock.connect((self.server, self.port))
        sock.send(f"PASS {self.token}\n".encode('utf-8'))
        sock.send(f"NICK {self.username}\n".encode('utf-8'))
        sock.send(f"JOIN {self.channel}\n".encode('utf-8'))
        # First 2 resp are a welcome message
        sock.recv(2048).decode('utf-8')
        sock.recv(2048).decode('utf-8')
        self.sock = sock
        print(f"CONNECTED TO {self.channel} AS {self.username}")
        return sock

    def redisConnect(self, hostname="redis", port=6379, db=0):
        """Connects to redis cache. Sets object's rdb to the opened
        redis connection for future writes.

        Args:
            hostname (str): redis host. Defaults to "redis".
            port (int): port number. Defaults to 6379.
            db (int): redis db to use. Defaults to 0.
        """
        print(f"Attempting to connect to redis at: {hostname}")
        rdb = redis.Redis(host=hostname, port=port, db=db)
        self.rdb = rdb

    def redisWrite(self, emotesDict):
        """Write the emotesDict of format (emote: count) into redis

        Args:
            emotesDict (dict): emoteName: emoteCount(per message) format
        """
        if self.rdb is None:
            print("ERROR: Redis connection does not exist!")
            return
        for key, value in emotesDict.items():
            try:
                # print(f"Writing {key}: {value} to redis")
                self.rdb.incr(key, value)
            except redis.exceptions.ConnectionError:
                print("ERROR: Could not connect to redis!")

    def messageListen(self):
        """Listens for messages from chatroom. Sends back PONG message if
        server pings the bot, and handles any valid messages in the chat.

        Returns:
            dictionary: dict of detected emotes where
            key = emote name
            value = number of occurences in message
        """
        if self.sock is None:
            print("Error! Socket does not exist. "
                  "Did you forget to joinChat() first?")
            return
        emotesFound = None
        try:
            message = self.sock.recv(2048)
            resp = message.decode('utf-8')
        except UnicodeDecodeError:
            print(f"Could not decode message! {message}")
            return None

        # Send back a PONG to prevent bot from being auto kicked
        if resp.startswith('PING'):
            self.sock.send("PONG\n".encode('utf-8'))
        # Valid message detected, parse and return any emotes
        elif len(resp) > 0:
            username = None
            channel = None
            message = None
            regex_string = ':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)'
            try:
                username, channel, message = re.search(regex_string, resp).groups()
            except AttributeError:
                print(f"Error parsing message: {resp}")
            if message is not None:
                # Remove return key and split into words.
                # Emotes must be properly spaced/spelled/capitalized
                for word in message.strip('\r').split(' '):
                    if word in self.emotes:
                        if emotesFound is None:
                            emotesFound = {}
                        if word not in emotesFound.keys():
                            emotesFound[word] = 1
                        else:
                            emotesFound[word] += 1

        return emotesFound


if __name__ == "__main__":
    # Starting inputs (will be done with args or json later)
    server = 'irc.chat.twitch.tv'
    port = 6667
    nickname = 'pogcount'
    token = 'oauth:do2xff0ei1fiiaz8tbexnrz3hmsoso'
    ircChannel = 'xqcow'
    hostname = 'redis'
    bot = chatWatcher(nickname, token, ircChannel)
    bot.joinChat()
    bot.redisConnect(hostname)
    while True:
        emotesCount = bot.messageListen()
        if emotesCount:
            bot.redisWrite(emotesCount)
