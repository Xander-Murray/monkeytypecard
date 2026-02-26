import os
import requests
from dotenv import load_dotenv

# load_dotenv()
#
# api_key = os.getenv("APEKEY")
# if not api_key:
#     raise ValueError("APEKEY is not set")
#
# headers = {"Authorization": f"ApeKey {api_key}"}
# params = {"mode": "words", "mode2": "10"}
#
# r = requests.get(
#     "https://api.monkeytype.com/users/personalBests",
#     headers=headers,
#     params=params,
#     timeout=5,
# )
# print("url:", r.url)
# print("status:", r.status_code)
# print("content-type:", r.headers.get("content-type"))
# print(r.text[:1000])


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


def get_card_stats_from_profile(profile_json, time_value: str, word_value: str):
    data = profile_json.get("data", {})
    pbs = data.get("personalBests", {})

    time_bucket = pbs.get("time", {}).get(str(time_value), [])
    word_bucket = pbs.get("words", {}).get(str(word_value), [])

    best_time = best_result(time_bucket)
    best_words = best_result(word_bucket)

    return {
        "name": data.get("name", "user"),
        "time_wpm": round(best_time.get("wpm", 0), 2) if best_time else 0,
        "time_acc": round(best_time.get("acc", 0), 2) if best_time else 0,
        "words_wpm": round(best_words.get("wpm", 0), 2) if best_words else 0,
        "words_acc": round(best_words.get("acc", 0), 2) if best_words else 0,
        "time_found": best_time is not None,
        "words_found": best_words is not None,
    }
