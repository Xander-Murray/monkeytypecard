import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("APEKEY")
if not api_key:
    raise ValueError("APEKEY is not set")

headers = {"Authorization": f"ApeKey {api_key}"}
params = {"mode": "words", "mode2": "10"}

r = requests.get(
    "https://api.monkeytype.com/users/personalBests",
    headers=headers,
    params=params,
    timeout=5,
)
print("url:", r.url)
print("status:", r.status_code)
print("content-type:", r.headers.get("content-type"))
print(r.text[:1000])
# get_stats(username):
#
#
#
#
# select_display_stats(stats, time_value, word_value):
