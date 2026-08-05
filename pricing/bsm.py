from datetime import datetime, timezone
from math import exp, log, sqrt
from zoneinfo import ZoneInfo

from scipy.stats import norm

SECONDS_PER_YEAR = 365 * 24 * 60 * 60
CLOSE_TZ = ZoneInfo("America/New_York")


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
