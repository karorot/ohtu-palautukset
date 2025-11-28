class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.m_score1 = 0
        self.m_score2 = 0

    def won_point(self, player_name):
        # how to have cleaner dependency on name
        if player_name == "player1":
            self.m_score1 = self.m_score1 + 1
        else:
            self.m_score2 = self.m_score2 + 1

    def get_score(self):
        if self.m_score1 == self.m_score2:
            return self.call_even_score()

        if self.m_score1 >= 4 or self.m_score2 >= 4:
            return self.call_winning_score()

        return self.call_score()

    def call_even_score(self):
        if self.m_score1 == 0:
            return "Love-All"
        if self.m_score1 == 1:
            return "Fifteen-All"
        if self.m_score1 == 2:
            return "Thirty-All"
        return "Deuce"

    def call_winning_score(self):
        minus_result = self.m_score1 - self. m_score2

        if minus_result == 1:
            return "Advantage player1"
        if minus_result == -1:
            return "Advantage player2"
        if minus_result >= 2:
            return "Win for player1"
        return "Win for player2"

    def call_score(self):
        temp_score = 0
        score = ""

        for i in range(1, 3):
            if i == 1:
                temp_score = self.m_score1
            else:
                score = score + "-"
                temp_score = self.m_score2

            if temp_score == 0:
                score = score + "Love"
            elif temp_score == 1:
                score = score + "Fifteen"
            elif temp_score == 2:
                score = score + "Thirty"
            elif temp_score == 3:
                score = score + "Forty"

        return score

    def score_call(self, points):
        pass
