import pytest
from unittest.mock import patch

from twitch_client import TwitchManager

@patch("twitch_client.TwitchManager.__init__", return_value=None)
@pytest.mark.parametrize("message, expected", [
    (
        "@badge-info=subscriber/16;badges=moderator/1,subscriber/12,bits-charity/1;color=#BF8C3F;display-name=Evanito;emotes=111700:16-24;flags=;id=2472002c-c974-4b91-bac8-8490623d798a;mod=1;room-id=60978448;subscriber=1;tmi-sent-ts=1598306044470;turbo=0;user-id=71602891;user-type=mod :evanito!evanito@evanito.tmi.twitch.tv PRIVMSG #dogdog :@Ralth_ neither DatSheffy",
        "@Ralth_ neither DatSheffy"
    )
])
def test_parse_message(mock_init, message, expected):
    TwitchManager.__init__ = mock_init
    tm = TwitchManager()
    tm.channel = "dogdog"
    assert tm.parse_message(message).message_content == expected


