import json
from os import path,makedirs
from json import JSONEncoder
from datetime import datetime
from zoneinfo import ZoneInfo
from time import time

from scores import SoccerScores, CricketScores, MotoGP

# TMP_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), ".tmux_status_cache.json")
TMP_FILE_PATH = path.join('/tmp/tmux-status', '.tmux_status_cache.json')
TZ_PST = ZoneInfo('America/Los_Angeles')


class Cache:
    next_line: int
    content: list[str]
    current_line_ttl: int

    def __init__(self, created_at, next_line, content, current_line_ttl=0):
        self.created_at = created_at
        self.next_line = next_line
        self.content = content
        self.current_line_ttl = current_line_ttl


class CacheEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def _get_next_line():
    if not path.isfile(TMP_FILE_PATH):
        return None

    try:
        with open(TMP_FILE_PATH, 'r') as f:
            d = json.load(f)
            cache: Cache = Cache(**d)
            if not cache:
                return None
            if cache.next_line >= len(cache.content):
                return None
            display_str = cache.content[cache.next_line]
            curr_epoch_seconds = int(time())
            if curr_epoch_seconds >= cache.current_line_ttl:
                cache.next_line += 1
                cache.current_line_ttl = int(time()) + 10

        with open(TMP_FILE_PATH, 'w') as f:
            json.dump(cache, cls=CacheEncoder, indent=4, fp=f)
            return display_str
    except Exception as e:
        print(e)
        return None


def _reload():
    if not path.isfile(TMP_FILE_PATH):
        makedirs(path.dirname(TMP_FILE_PATH), exist_ok=True)

    content = SoccerScores().get_score_ticker() or []
    content.extend(CricketScores().get_score_ticker())
    content.extend(MotoGP().get_score_ticker())
    cache = Cache(datetime.now(TZ_PST).__str__(), 0, content)
    with open(TMP_FILE_PATH, 'w') as f:
        json.dump(cache, cls=CacheEncoder, indent=4, fp=f)


if __name__ == '__main__':
    n = _get_next_line()
    if not n:
        _reload()
        n = _get_next_line()
    print(n)
