import unittest
from statistics_service import StatisticsService
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Wayne Gretzky", "EDM", 92, 120),
            Player("Mario Lemieux", "PIT", 85, 114),
            Player("Jaromir Jagr", "PIT", 70, 90),
            Player("Mark Messier", "NYR", 50, 60),
            Player("Jari Kurri", "EDM", 60, 50),
            Player("Steve Yzerman", "DET", 60, 80),
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        self.stats = StatisticsService(PlayerReaderStub())

    def test_find_existing_player(self):
        player = self.stats.search("Wayne Gretzky")
        self.assertEqual(player.name, "Wayne Gretzky")

    def test_find_when_no_player_exists(self):
        player = self.stats.search("Test Player")
        self.assertIsNone(player)

    def test_return_players_from_team(self):
        players = self.stats.team("PIT")
        self.assertEqual(len(players), 2)

    def test_return_empty_list_if_team_doesnt_exist(self):
        team = self.stats.team("Test")
        self.assertEqual(len(team), 0)

    def test_return_top_players(self):
        top = self.stats.top(3)
        self.assertEqual(len(top), 3)
        self.assertEqual(top[0].name, "Wayne Gretzky")

    def test_return_top_players_when_requesting_more_than_listed(self):
        top = self.stats.top(10)
        self.assertEqual(len(top), 6)

    def test_return_top_players_with_same_score(self):
        top = self.stats.top(4)
        self.assertEqual(len(top), 4)

    def test_return_0_top_players(self):
        top = self.stats.top(0)
        self.assertEqual(len(top), 0)
