class PlayerStats: # pylint: disable=too-few-public-methods
    def __init__(self, player_reader):
        self.players = player_reader.get_players()

    def top_scorers_by_nationality(self, nationality):
        result = filter(lambda player: player.nationality == nationality, self.players)
        return sorted(result, key=lambda player: player.goals + player.assists, reverse=True)
