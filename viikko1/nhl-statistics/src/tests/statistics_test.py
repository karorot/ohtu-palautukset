import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Wayne Gretzky", "EDM", 92, 120), # 92 + 120 = 212
            Player("Mario Lemieux", "PIT", 93, 114), # 93 + 114 = 207
            Player("Jaromir Jagr", "PIT", 70, 121), # 70 + 121 = 191
            Player("Mark Messier", "NYR", 50, 60), # 50 + 60 = 110
            Player("Jari Kurri", "EDM", 80, 60), # 80 + 60 = 140
            Player("Steve Yzerman", "DET", 60, 80), # 60 + 80 = 140
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        self.stats = StatisticsService(PlayerReaderStub())

    def test_find_existing_player(self):
        player = self.stats.search("Wayne Gretzky")
        self.assertEqual(player.name, "Wayne Gretzky")

    def test_return_none_when_no_player_exists(self):
        player = self.stats.search("Test Player")
        self.assertIsNone(player)

    def test_return_players_from_team(self):
        players = self.stats.team("PIT")
        self.assertEqual(len(players), 2)

    def test_return_empty_list_if_team_doesnt_exist(self):
        team = self.stats.team("ABC")
        self.assertEqual(len(team), 0)

    def test_return_top_players_no_sortby(self):
        top = self.stats.top(3)
        self.assertEqual(len(top), 3)
        self.assertEqual(top[0].name, "Wayne Gretzky")

    def test_return_top_players_by_points(self):
        top = self.stats.top(3, SortBy.POINTS)
        self.assertEqual(len(top), 3)
        self.assertEqual(top[0].name, "Wayne Gretzky")

    def test_return_top_players_by_goals(self):
        top = self.stats.top(3, SortBy.GOALS)
        self.assertEqual(len(top), 3)
        self.assertEqual(top[0].name, "Mario Lemieux")

    def test_return_top_players_by_assists(self):
        top = self.stats.top(3, SortBy.ASSISTS)
        self.assertEqual(len(top), 3)
        self.assertEqual(top[0].name, "Jaromir Jagr")

    def test_return_top_players_when_requesting_more_than_listed(self):
        top = self.stats.top(10)
        self.assertEqual(len(top), 6)

    def test_return_top_player_with_more_goals_if_same_points(self):
        top = self.stats.top(4)
        self.assertEqual(len(top), 4)
        self.assertEqual(top[3].name, "Jari Kurri")

    def test_return_0_top_players(self):
        top = self.stats.top(0)
        self.assertEqual(len(top), 0)
