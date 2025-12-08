from statistics import Statistics
from player_reader import PlayerReader
from matchers import And, Not, HasAtLeast, HasFewerThan, PlaysIn, All, Or

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players.txt"
    reader = PlayerReader(url)
    stats = Statistics(reader)

    # Alkuperäinen esimerkki
    print("Players with at least 5 goals and 20 assists playing in PHI:")
    matcher = And(
        HasAtLeast(5, "goals"),
        HasAtLeast(20, "assists"),
        PlaysIn("PHI")
    )

    for player in stats.matches(matcher):
        print(player)

    # Not
    print("Players in NYR that don't have at least 2 goals:")
    matcher = And(
        Not(HasAtLeast(2, "goals")),
        PlaysIn("NYR")
    )
    for player in stats.matches(matcher):
        print(player)

    # HasFewerThan
    print("Players in NYR with less than 2 goals:")
    matcher = And(
        HasFewerThan(2, "goals"),
        PlaysIn("NYR")
    )
    for player in stats.matches(matcher):
        print(player)

    # All
    print("Number of all players")
    filtered_with_all = stats.matches(All())
    print(len(filtered_with_all)) #899

    # Or, part 1
    print("Players with at least 45 goals, or at least 70 assists:")
    matcher = Or(
        HasAtLeast(45, "goals"),
        HasAtLeast(70, "assists")
    )
    for player in stats.matches(matcher):
        print(player)

    # Or, part 2
    print("Players with at least 70 points playing in COL, FLA, or BOS:")
    matcher = And(
        HasAtLeast(70, "points"),
        Or(
            PlaysIn("COL"),
            PlaysIn("FLA"),
            PlaysIn("BOS")
        )
    )
    for player in stats.matches(matcher):
        print(player)

if __name__ == "__main__":
    main()
