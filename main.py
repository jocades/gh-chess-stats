import requests as http
from pprint import pprint
import os

# https://gist.github.com/jocades/0910d35984c15933e380df460a6fc97d


GIST_TITLE = "♟︎ Chess.com Ratings"
GIST_ID = os.getenv("GIST_ID")
GH_TOKEN = os.getenv("GH_TOKEN")
CHESS_USERNAME = os.getenv("CHESS_USERNAME")

STATS_URL = f"https://api.chess.com/pub/player/{CHESS_USERNAME}/stats"


def get_stats() -> dict[str, dict]:
    headers = {"User-Agent": f"@{CHESS_USERNAME}"}
    return http.get(STATS_URL, headers=headers).json()


def main():
    stats = get_stats()
    pprint(stats)


if __name__ == "__main__":
    main()
