import json
import os
import requests

# =========================
# CHANGE THE DATE HERE
# =========================
YEAR = 2026
MONTH = 7
DAY = 31
# =========================


EVENT = f"wti-closes-above-on-july-31-2026"

GAMMA_API = "https://gamma-api.polymarket.com/events/slug/"
CLOB_API = "https://clob.polymarket.com/prices-history"

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def main() -> None:
    """
    1. get event
    2. get all strikes
    3. get minute interval trades for all strikes
    """

    # Get event
    event = requests.get(
        GAMMA_API + EVENT,
        timeout=10
    ).json()

    data = {}

    for market in event["markets"]:
        # Get contract strike
        strike = market["groupItemTitle"]

        yes_token = json.loads(market["clobTokenIds"])[0]

        # Get market history
        history = requests.get(
            CLOB_API,
            params={
                "market": yes_token,
                "interval": "max",
                "fidelity": 1,
            },
            timeout=10,
        ).json()["history"]

        data[strike] = history

    out_path = os.path.join(DATA_DIR, f"polymarket-{YEAR}-{MONTH}-{DAY}.json")
    with open(out_path, "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()