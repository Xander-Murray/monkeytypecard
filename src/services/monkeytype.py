import requests
from datetime import timedelta


def get_profile(username: str):
    url = f"https://api.monkeytype.com/users/{username}/profile"
    params = {"isUid": "false"}

    r = requests.get(url, params=params, timeout=5)
    r.raise_for_status()
    return r.json()


def best_result(results: list[dict]):
    if not results:
        return None
    return max(results, key=lambda x: x.get("wpm", 0))


def normalize_time(time: str) -> str:
    td = timedelta(seconds=round(float(time)))
    total = int(td.total_seconds())
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def get_card_stats_from_profile(profile_json, time_value: int, word_value: int) -> dict:
    data = profile_json.get("data", {})
    pbs = data.get("personalBests", {})
    typing_stats = data.get("typingStats", {})

    time_typing = normalize_time(typing_stats.get("timeTyping", "0"))
    time_bucket = pbs.get("time", {}).get(str(time_value), [])
    word_bucket = pbs.get("words", {}).get(str(word_value), [])

    best_time = best_result(time_bucket)
    best_words = best_result(word_bucket)

    return {
        "name": data.get("name", "user"),
        "time_typing": time_typing,
        "time_wpm": int(round(best_time.get("wpm", 0), 0)) if best_time else "--",
        "time_acc": round(best_time.get("acc", 0), 0) if best_time else "--",
        "words_wpm": int(round(best_words.get("wpm", 0), 0)) if best_words else "--",
        "words_acc": round(best_words.get("acc", 0), 0) if best_words else "--",
        "time_found": best_time is not None,
        "words_found": best_words is not None,
    }
