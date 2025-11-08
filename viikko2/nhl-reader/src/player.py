class Player:
    def __init__(self, data):
        self.name = data['name']
        self.nationality = data['nationality']
        self.team = data['team']
        self.goals = data['goals']
        self.assists = data['assists']

    def __str__(self):
        return (
            f"{self.name} {self.team} {self.goals} + {self.assists}"
            f" = {self.goals + self.assists}"
        )
