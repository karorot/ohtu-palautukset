from enum import IntEnum

class Score(IntEnum):
    LOVE = 0
    FIFTEEN = 1
    THIRTY = 2
    FORTY = 3
    ADVANTAGE = 4

class TennisGame:
    WINNING_CALL = "Win for "
    ADVANTAGE_CALL = "Advantage "

    def __init__(self, player1_name, player2_name):
        self.player1 = player1_name
        self.player2 = player2_name
        self.scores = {
            player1_name: Score.LOVE,
            player2_name: Score.LOVE
        }
        self.score_names = {
            Score.LOVE: "Love",
            Score.FIFTEEN: "Fifteen",
            Score.THIRTY: "Thirty",
            Score.FORTY: "Forty"
        }

    def won_point(self, player_name):
        if player_name in self.scores:
            self.scores[player_name] += 1

    def get_score(self):
        if self.scores[self.player1] == self.scores[self.player2]:
            return self.call_even_score(self.scores[self.player1])

        if self.scores[self.player1] >= Score.ADVANTAGE or \
            self.scores[self.player2] >= Score.ADVANTAGE:
            return self.call_winning_score()

        return self.call_score()

    def call_even_score(self, score):
        if score < Score.FORTY:
            return self.score_names[score] + "-All"
        return "Deuce"

    def call_winning_score(self):
        minus_result = self.scores[self.player1] - self.scores[self.player2]

        if minus_result == 1:
            return self.ADVANTAGE_CALL + self.player1
        if minus_result == -1:
            return self.ADVANTAGE_CALL + self.player2
        if minus_result >= 2:
            return self.WINNING_CALL + self.player1
        return self.WINNING_CALL + self.player2

    def call_score(self):
        temp_score = 0
        score = ""

        for i in range(1, 3):
            if i == 1:
                temp_score = self.scores[self.player1]
            else:
                score = score + "-"
                temp_score = self.scores[self.player2]

            score = score + self.score_names[temp_score]

        return score
