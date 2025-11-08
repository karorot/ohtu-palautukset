from rich.table import Table, Column
from rich.console import Console
from rich.theme import Theme
from rich.prompt import Prompt
from player_reader import PlayerReader
from player_stats import PlayerStats

def main():
    custom_theme = Theme({"info": "bold magenta", "warning": "red"})
    console = Console(theme=custom_theme)

    console.print("Player statistics available for seasons 2018-2026", style="info")
    console.print("Quit at any time with 'q'", style="warning")
    season = Prompt.ask("Choose season, e.g. 2024-25").strip()

    if season.lower() == 'q':
        return

    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)

    console.print("Use the 3-letter country codes to list players (e.g. FIN, SWE, CAN)",
                    style="info")

    while True:
        nat = Prompt.ask("Choose nationality").strip()

        if nat.lower() == "q":
            break

        players = stats.top_scorers_by_nationality(nat.upper())

        table = Table(
            Column(header="Player", justify="left", style="cyan", no_wrap=True),
            Column(header="Teams", justify="left", style="magenta"),
            Column(header="Goals", justify="right", style="green"),
            Column(header="Assists", justify="right", style="green"),
            Column(header="Points", justify="right", style="green"),
            title=f"Players from {nat.upper()} in {season}"
        )

        for player in players:
            table.add_row(
                player.name,
                player.team,
                str(player.goals),
                str(player.assists),
                str(player.goals + player.assists)
            )

        if table.rows:
            console.print(table)
        else:
            print("No data available.\n")

if __name__ == "__main__":
    main()
