# Packages
import socket
import re
import sys
import irc.bot
import requests
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
        resp = sock.recv(2048).decode('utf-8')
        resp = sock.recv(2048).decode('utf-8')
        self.sock = sock
        print(f"CONNECTED TO {self.channel} AS {self.username}")
        return sock

    def messageListen(self):
        """Listens for messages from chatroom. Sends back PONG message if server pings the bot,
        and handles any valid messages in the chat.

        Returns:
            dictionary: dict of detected emotes where
            key = emote name
            value = number of occurences in message
        """
        if self.sock is None:
            print("Error! Socket does not exist. Did you forget to joinChat() first?")
            return
        emotesFound = None
        resp = self.sock.recv(2048).decode('utf-8')

        # Send back a PONG to prevent bot from being auto kicked
        if resp.startswith('PING'):
            self.sock.send("PONG\n".encode('utf-8'))
        # Valid message detected, parse and return any emotes
        elif len(resp) > 0:
            # emotesFound = self.parseMessage(resp)
            username = None
            channel = None
            message = None
            emotesFound = {}
            try:
                username, channel, message = re.search(':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', resp).groups()
            except AttributeError:
                print(f"Error parsing message: {resp}")
            if message is not None:
                # Remove return key and split into words. Emotes must be properly spaced/spelled/capitalized
                for word in message.strip('\r').split(' '):
                    if word in self.emotes:
                        if word not in emotesFound.keys():
                            emotesFound[word] = 1
                        else:
                            emotesFound[word] += 1
            
        return emotesFound
        


# Starting inputs (will be done with args or json later)
server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'pogcount'
token = 'oauth:do2xff0ei1fiiaz8tbexnrz3hmsoso'
ircChannel = 'hasanabi'
bot = chatWatcher(nickname, token, ircChannel)
bot.joinChat()
while True:
    emotes = bot.messageListen()
    print(emotes)