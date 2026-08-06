from datetime import datetime, timezone
from math import exp, log, sqrt
from zoneinfo import ZoneInfo
import pandas as pd
import json
import bisect

from scipy.stats import norm

SECONDS_PER_YEAR = 365 * 24 * 60 * 60
CLOSE_TZ = ZoneInfo("America/New_York")


def get_vol() -> float:
    """TODO"""
    return 0.0


def time_to_expiry(t: int) -> float:
    """
    Time to expiry (in years) from a unix timestamp to the close of that
    same trading day (5pm ET).
    """
    local = datetime.fromtimestamp(t, tz=CLOSE_TZ)
    close = local.replace(hour=17, minute=0, second=0, microsecond=0)
    return max(close.astimezone(timezone.utc).timestamp() - t, 0) / SECONDS_PER_YEAR


def black76_call(F: float, K: float, T: float, vol: float, r: float = 0) -> float:
    """Black-76 call price."""
    if T <= 0:
        return max(F - K, 0)

    d1 = (log(F / K) + 0.5 * vol ** 2 * T) / (vol * sqrt(T))
    d2 = d1 - vol * sqrt(T)

    return exp(-r * T) * (F * norm.cdf(d1) - K * norm.cdf(d2))


def call_spread_probability(F: float, K1: float, K2: float, T: float, vol: float, r: float = 0) -> float:
    return (black76_call(F, K1, T, vol, r) - black76_call(F, K2, T, vol, r)) / (K2 - K1)


def get_call_spread_probability_series(polymarket_strike: str) -> None:
    """Get a series of {t, p} of implied probability from call spread"""

    # first Unix timestamp of that day
    with open("../data/polymarket-2026-7-31.json") as f:
        poly = json.load(f)

    first_t = poly[polymarket_strike][0]["t"]

    # import the future prices
    with open("../data/futures-2026-07-31.json") as f:
        futures = json.load(f) 

    # sort future prices by t
    futures.sort(key=lambda pt: pt["t"])

    # only start calculated implied probability after first_t
    times = [pt["t"] for pt in futures]
    start_t = bisect.bisect_left(times, first_t) 

    # iterate through all future prices and store them to the series
    rows = []
    for pt in futures[start_t:]:
        K1 = pt["f"] - 0.5
        K2 = pt["f"] + 0.5
        T = time_to_expiry(pt["t"])
        vol = get_vol()
        p = call_spread_probability(pt["f"], K1, K2, T, vol)

        rows.append({"futures_t": pt["t"], "futures_p": p})

    output = pd.DataFrame(rows, columns=["futures_t", "futures_p"])

    output.to_parquet(f"../data/bsm_{polymarket_strike.lstrip("$")}.parquet")


def main() -> None: 
    with open("../data/polymarket-2026-7-31.json") as f:
        poly = json.load(f)

    for strike, history in poly.items():
        get_call_spread_probability_series(strike)