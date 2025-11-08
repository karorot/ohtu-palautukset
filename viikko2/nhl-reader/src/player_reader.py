import requests
from player import Player

class PlayerReader:
    def __init__(self, url):
        self._url = url

    def get_players(self):
        response = requests.get(self._url).json()
        players = []

        for player_data in response:
            player = Player(player_data)
            players.append(player)

        return players
