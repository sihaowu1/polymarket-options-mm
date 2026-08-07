from datetime import datetime, timezone
import json
import argparse

import pandas as pd
import matplotlib.pyplot as plt


def plot_strike(strike: str) -> None:
    """Plot futures-implied probability vs Polymarket probability over time for a strike."""
    futures = pd.read_parquet(f"../data/bsm_{strike}.parquet")

    with open("../data/polymarket-2026-7-31.json") as f:
        poly = json.load(f)[f"${strike}"]

    start_t = max(futures["futures_t"].min(), min(pt["t"] for pt in poly))
    futures = futures[futures["futures_t"] >= start_t]
    poly = [pt for pt in poly if pt["t"] >= start_t]

    fig, ax = plt.subplots()
    ax.plot(
        [datetime.fromtimestamp(t, tz=timezone.utc) for t in futures["futures_t"]],
        futures["futures_p"],
        label="Futures-implied",
    )
    ax.plot(
        [datetime.fromtimestamp(pt["t"], tz=timezone.utc) for pt in poly],
        [pt["p"] for pt in poly],
        label="Polymarket",
    )

    ax.set_xlabel("Time")
    ax.set_ylabel("Probability")
    ax.set_title(f"${strike} - implied probability")
    ax.legend()
    fig.autofmt_xdate()
    plt.show()


def parse_args() -> argparse.Namespace: 
    parser = argparse.ArgumentParser() 

    parser.add_argument(
        "-s", 
        "--strike",
        required=True,
    ) 

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    plot_strike(args.strike)


if __name__ == "__main__":
    main()
