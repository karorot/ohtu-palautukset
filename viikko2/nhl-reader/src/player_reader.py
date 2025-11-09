import requests
from player import Player

class PlayerReader: # pylint: disable=too-few-public-methods
    def __init__(self, url):
        self._url = url

    def get_players(self):
        try:
            response = requests.get(self._url, timeout=5).json()
            players = []

            for player_data in response:
                player = Player(player_data)
                players.append(player)

            return players
        except requests.Timeout:
            print("Request timed out after 5s")
            return []
