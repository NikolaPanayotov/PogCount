# Packages
import socket
import re
# Local imports
from emotes import emotes

def joinChat(server, port, nickname, token, channel):
    sock = socket.socket()
    sock.connect((server, port))
    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {ircChannel}\n".encode('utf-8'))
    # First 2 resp are a welcome message
    resp = sock.recv(2048).decode('utf-8')
    resp = sock.recv(2048).decode('utf-8')
    return sock

def messageListen(sock):
    emotesFound = None
    resp = sock.recv(2048).decode('utf-8')

    if resp.startswith('PING'):
        sock.send("PONG\n".encode('utf-8'))
    elif len(resp) > 0:
        username = None
        channel = None
        message = None
        emotesFound = {}
        try:
            username, channel, message = re.search(':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', resp).groups()
            # print(f"{username}: {message}")
        except AttributeError:
            print(f"Error parsing message: {resp}")
        if message is not None:
            for word in message.strip('\r').split(' '):
                if word in emotes:
                    print(f"EMOTE FOUND! _{word}_")
                    if word not in emotesFound.keys():
                        emotesFound[word] = 1
                    else:
                        emotesFound[word] += 1
        print(f"RETURNING EMOTES: {emotesFound}")
    return emotesFound

# Starting inputs (will be done with args or json later)
server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'pogcount'
token = 'oauth:do2xff0ei1fiiaz8tbexnrz3hmsoso'
ircChannel = '#hasanabi'
sock = joinChat(server,port,nickname,token,ircChannel)
while True:
    messageListen(sock)