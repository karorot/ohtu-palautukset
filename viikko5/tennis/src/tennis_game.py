from enum import IntEnum

class Score(IntEnum):
    LOVE = 0
    FIFTEEN = 1
    THIRTY = 2
    FORTY = 3
    ADVANTAGE_THRESHOLD = 4

class TennisGame:
    WINNING_CALL = "Win for "
    ADVANTAGE_CALL = "Advantage "

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
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
        if self.scores[self.player1_name] == self.scores[self.player2_name]:
            return self.call_even_score(self.scores[self.player1_name])

        if (self.scores[self.player1_name] >= Score.ADVANTAGE_THRESHOLD or
            self.scores[self.player2_name] >= Score.ADVANTAGE_THRESHOLD):
            return self.call_winning_score()

        return self.call_score()

    def call_even_score(self, score):
        if score < Score.FORTY:
            return self.score_names[score] + "-All"
        return "Deuce"

    def call_winning_score(self):
        score_difference = self.scores[self.player1_name] - self.scores[self.player2_name]

        if score_difference == 1:
            return self.ADVANTAGE_CALL + self.player1_name
        if score_difference == -1:
            return self.ADVANTAGE_CALL + self.player2_name
        if score_difference >= 2:
            return self.WINNING_CALL + self.player1_name
        return self.WINNING_CALL + self.player2_name

    def call_score(self):
        temp_score = 0
        score = ""

        for i in range(1, 3):
            if i == 1:
                temp_score = self.scores[self.player1_name]
            else:
                score = score + "-"
                temp_score = self.scores[self.player2_name]

            score = score + self.score_names[temp_score]

        return score
