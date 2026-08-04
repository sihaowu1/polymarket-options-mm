import json
import os
from datetime import date, timedelta

import yfinance as yf

# =========================
# CHANGE THE DATE HERE
# =========================
YEAR = 2026
MONTH = 7
DAY = 31
# =========================

TICKER = "CL=F"

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def main() -> None:
    start_date = date(YEAR, MONTH, DAY)
    end_date = start_date + timedelta(days=1)

    bars = yf.Ticker(TICKER).history(
        start=start_date.isoformat(), end=end_date.isoformat(), interval="1m"
    )

    data = [
        {"t": int(ts.timestamp()), "p": float(row["Close"])}
        for ts, row in bars.iterrows()
    ]

    out_path = os.path.join(DATA_DIR, f"futures-{start_date.isoformat()}.json")
    with open(out_path, "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()
