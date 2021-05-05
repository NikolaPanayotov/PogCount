# Packages
import os
import requests
import json
# Local Imports
from twitch_errors import OAuthError, TwitchAPIError


def get_twitch_oauth():
    oauth_url = "https://id.twitch.tv/oauth2/token"
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    query = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    response = requests.post(oauth_url, params=query)
    if response.status_code == 200:
        result = json.loads(response.text)
        token = result['access_token']
        return token
    else:
        print(f"Error getting oauth token: {response.text}")
        raise TwitchAPIError


def get_top_channels(oauth, quantity):
    streams_url = "https://api.twitch.tv/helix/streams"
    client_id = os.getenv('CLIENT_ID')
    headers = {
        'Authorization': "Bearer " + oauth,
        "client-id": client_id,
    }
    query = {
        "first": quantity,
    }
    response = requests.get(streams_url, params=query, headers=headers)
    if response.status_code == 200:
        result = json.loads(response.text)
        channels = []
        for channel in result['data']:
            channels.append(channel['user_login'])
        return channels
    elif response.status_code == 401:
        print("Oauth invalid!")
        print(response.text)
        raise OAuthError
    else:
        print(response.status_code)
        print(response.text)
        raise TwitchAPIError
