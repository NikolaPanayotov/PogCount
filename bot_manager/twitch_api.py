# Packages
import os
import requests
import json
# Local Imports
from twitch_errors import OAuthError, TwitchAPIError


def get_twitch_oauth():
    """
    Sends a POST to Twitch API to obtain Oauth token for future API requests

    Raises:
        TwitchAPIError: Any OAuth token error will be raised and logged

    Returns:
        Str: OAuth token string
    """
    oauth_url = "https://id.twitch.tv/oauth2/token"
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    query = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    response = requests.post(oauth_url, params=query)
    # Return successful API call
    if response.status_code == 200:
        result = json.loads(response.text)
        token = result['access_token']
        return token
    else:
        print(f"Error getting oauth token: {response.text}")
        raise TwitchAPIError


def get_top_channels(oauth, quantity):
    """
    Obtain [quantity] most popular channels

    Args:
        oauth (Str): OAuth token string
        quantity (Int): Number of channels to collect

    Raises:
        OAuthError: Invalid OAuth token, usually because old one expired
        TwitchAPIError: Any future TwitchAPI error

    Returns:
        List: List of channel names
    """
    streams_url = "https://api.twitch.tv/helix/streams"
    client_id = os.getenv('CLIENT_ID')
    # This api uses client-id with a - instead of _
    headers = {
        'Authorization': "Bearer " + oauth,
        "client-id": client_id,
    }
    query = {
        "first": quantity,
    }
    response = requests.get(streams_url, params=query, headers=headers)
    # Handle successful API call
    if response.status_code == 200:
        result = json.loads(response.text)
        channels = []
        # API responds with JSON object with a bunch of channel data
        for channel in result['data']:
            channels.append(channel['user_login'])
        return channels
    # 401 == unauthorized (usually because of Oauth mismatch)
    elif response.status_code == 401:
        print("Oauth invalid!")
        print(response.text)
        raise OAuthError
    # Log any other error
    else:
        print(response.status_code)
        print(response.text)
        raise TwitchAPIError
