from statistics import Statistics
from player_reader import PlayerReader
from query_builder import QueryBuilder


def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players.txt"
    reader = PlayerReader(url)
    stats = Statistics(reader)
    query = QueryBuilder()

    print("And test: Players in NYR with at least 10 but fewer than 20 goals")
    matcher = (
        query
        .plays_in("NYR")
        .has_at_least(10, "goals")
        .has_fewer_than(20, "goals")
        .build()
    )

    for player in stats.matches(matcher):
        print(player)

    print(
        "\nOr test: Players in PHI with at least 10 assists but fewer than 10 goals "
        "OR players in EDM with at least 50 points"
    )
    matcher = (
    query
        .one_of(
        query.plays_in("PHI")
            .has_at_least(10, "assists")
            .has_fewer_than(10, "goals"),
        query.plays_in("EDM")
            .has_at_least(50, "points")
        )
        .build()
    )

    for player in stats.matches(matcher):
        print(player)

if __name__ == "__main__":
    main()
