import requests as http
from pprint import pprint
from os import getenv
from github import Github, Auth, InputFileContent


GIST_TITLE = "♟︎ Chess.com Ratings"

GH_TOKEN = getenv("GH_TOKEN")
GIST_ID = getenv("GIST_ID")
CHESS_USERNAME = getenv("CHESS_USERNAME")

STATS_URL = f"https://api.chess.com/pub/player/{CHESS_USERNAME}/stats"
GAME_MODES = {
    "bullet": "🚅",
    "blitz": "⚡",
    "rapid": "🕖",
}


hub = Github(auth=Auth.Token(GH_TOKEN))


def get_stats() -> dict[str, dict]:
    headers = {"User-Agent": f"@{CHESS_USERNAME}"}
    return http.get(STATS_URL, headers=headers).json()


def update_gist(content: str):
    hub.get_gist(GIST_ID).edit(files={GIST_TITLE: InputFileContent(content)})


def parse(mode, rating, max_line_length):
    icon = GAME_MODES[mode]
    separator = "." * (max_line_length - len(mode) + len(rating) + 2)
    return f"{icon} {mode.capitalize()} {separator} {rating} 📈"


def main():
    stats = get_stats()

    lines = [
        parse(mode, str(stats[f"chess_{mode}"]["last"]["rating"]), 52)
        for mode in GAME_MODES.keys()
    ]

    print("\n".join(lines))

    hub.close()


if __name__ == "__main__":
    main()
