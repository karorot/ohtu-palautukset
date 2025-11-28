from enum import IntEnum

class Score(IntEnum):
    LOVE = 0
    FIFTEEN = 1
    THIRTY = 2
    FORTY = 3
    ADVANTAGE = 4

class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1 = player1_name
        self.player2 = player2_name
        self.scores = {
            player1_name: Score.LOVE,
            player2_name: Score.LOVE
        }

    def won_point(self, player_name):
        if player_name in self.scores:
            self.scores[player_name] += 1

    def get_score(self):
        if self.scores[self.player1] == self.scores[self.player2]:
            return self.call_even_score()

        if self.scores[self.player1] >= Score.ADVANTAGE or \
            self.scores[self.player2] >= Score.ADVANTAGE:
            return self.call_winning_score()

        return self.call_score()

    def call_even_score(self):
        if self.scores[self.player1] == Score.LOVE:
            return "Love-All"
        if self.scores[self.player1] == Score.FIFTEEN:
            return "Fifteen-All"
        if self.scores[self.player1] == Score.THIRTY:
            return "Thirty-All"
        return "Deuce"

    def call_winning_score(self):
        minus_result = self.scores[self.player1] - self.scores[self.player2]

        if minus_result == 1:
            return "Advantage " + self.player1
        if minus_result == -1:
            return "Advantage " + self.player2
        if minus_result >= 2:
            return "Win for " + self.player1
        return "Win for " + self.player2

    def call_score(self):
        temp_score = 0
        score = ""

        for i in range(1, 3):
            if i == 1:
                temp_score = self.scores[self.player1]
            else:
                score = score + "-"
                temp_score = self.scores[self.player2]

            if temp_score == Score.LOVE:
                score = score + "Love"
            elif temp_score == Score.FIFTEEN:
                score = score + "Fifteen"
            elif temp_score == Score.THIRTY:
                score = score + "Thirty"
            elif temp_score == Score.FORTY:
                score = score + "Forty"

        return score
