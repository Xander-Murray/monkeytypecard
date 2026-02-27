import requests
from datetime import timedelta
import time as time_mod
import re

_profile_cache = {}
CACHE_TTL_SECONDS = 300  # 5 minutes


def get_profile(username: str):
    """Fetch a user's public profile from the monkeytype API.
    Returns cached response if available and fresh."""
    now = time_mod.time()
    cached = _profile_cache.get(username)

    if cached and (now - cached["ts"]) < CACHE_TTL_SECONDS:
        return cached["data"]

    url = f"https://api.monkeytype.com/users/{username}/profile"
    params = {"isUid": "false"}

    r = requests.get(url, params=params, timeout=5)
    r.raise_for_status()
    data = r.json()

    _profile_cache[username] = {"data": data, "ts": now}
    return data


def best_result(results: list[dict]):
    if not results:
        return None
    return max(results, key=lambda x: x.get("wpm", 0))


def normalize_time(raw_time) -> str:
    try:
        td = timedelta(seconds=round(float(raw_time)))
        total = int(td.total_seconds())
        h, rem = divmod(total, 3600)
        m, s = divmod(rem, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"
    except (ValueError, TypeError, OverflowError):
        return "00:00:00"


def is_profile_private(profile_json: dict) -> bool:
    data = profile_json.get("data", {})
    pbs = data.get("personalBests", {})
    # A private profile returns an empty personalBests or none at all
    return not pbs


# only allow alphanumeric, underscores, hyphens, and periods; max 20 chars
USERNAME_RE = re.compile(r"^[\w.\-]{1,20}$")


def is_valid_username(username: str) -> bool:
    return bool(USERNAME_RE.match(username))


def get_card_stats_from_profile(profile_json, time_value: int, word_value: int) -> dict:
    """Extract the best wpm/acc for the given time and word modes from a profile."""
    data = profile_json.get("data", {})
    pbs = data.get("personalBests", {})
    typing_stats = data.get("typingStats", {})

    time_typing = normalize_time(typing_stats.get("timeTyping", 0))
    time_bucket = pbs.get("time", {}).get(str(time_value), [])
    word_bucket = pbs.get("words", {}).get(str(word_value), [])

    best_time = best_result(time_bucket)
    best_words = best_result(word_bucket)

    return {
        "name": data.get("name", "user"),
        "time_typing": time_typing,
        "time_wpm": int(round(best_time.get("wpm", 0))) if best_time else "--",
        "time_acc": int(round(best_time.get("acc", 0))) if best_time else "--",
        "words_wpm": int(round(best_words.get("wpm", 0))) if best_words else "--",
        "words_acc": int(round(best_words.get("acc", 0))) if best_words else "--",
        "time_found": best_time is not None,
        "words_found": best_words is not None,
    }
