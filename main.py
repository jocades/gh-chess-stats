import requests as http
from os import getenv
from github import Github, Auth, InputFileContent


GIST_TITLE = "♟︎ Chess.com Ratings"
GAME_MODES = {
    "bullet": "🚅",
    "blitz": "⚡ ",
    "rapid": "⏲️",
}

STATS_URL = "https://api.chess.com/pub/player/{user}/stats"


def environ():
    vars = []
    missing = False
    for key in ("GH_TOKEN", "GIST_ID", "CHESS_USERNAME"):
        var = getenv(key)
        if not var:
            print(f"Missing required environment variable: {var}")
            missing = True
        else:
            vars.append(var)
    if missing:
        exit(1)

    return vars


def get_stats(user: str) -> dict[str, dict]:
    headers = {"User-Agent": f"@{user}"}
    return http.get(STATS_URL.format(user=user), headers=headers).json()


def parse_line(mode: str, rating: str, max_line_length: int):
    icon = GAME_MODES[mode]
    sep = "." * (max_line_length - len(mode) + len(rating))
    return f"{icon} {mode.capitalize()} {sep} {rating} 📈"


def parse(stats: dict[str, dict]):
    return "\n".join(
        parse_line(
            mode,
            str(stats[f"chess_{mode}"]["last"]["rating"]),
            36,
        )
        for mode in GAME_MODES.keys()
    )


def update_gist(token: str, gist_id: str, content: str):
    hub = Github(auth=Auth.Token(token))
    hub.get_gist(gist_id).edit(files={GIST_TITLE: InputFileContent(content)})
    hub.close()


def main():
    token, gist_id, user = environ()

    stats = get_stats(user)
    content = parse(stats)

    print(content)

    update_gist(token, gist_id, content)


if __name__ == "__main__":
    main()
