"""
Lumina Creative Tool — bitcoin_mining_estimator
Created : 2026-08-10T15:59:16
Purpose : Estimates expected Bitcoin block discovery time, daily revenue, electricity cost, and net profit for a given hash rate, power draw, difficulty, and BTC price, outputting a JSON report and an ASCII profit chart.
"""

#!/usr/bin/env python3
"""
bitcoin_mining_estimator.py

Estimate expected mining performance and profitability for Bitcoin
using only standard‑library modules.

Usage (interactive):
    python bitcoin_mining_estimator.py

The script prompts for:
    - hash rate (H/s)
    - power consumption (W)
    - electricity cost (USD/kWh)
    - network difficulty
    - block reward (BTC, default 6.25)
    - BTC price (USD)
It then prints a summary, saves a JSON report, and shows a tiny ASCII chart.
"""

import json
import math
import os
import sys
from datetime import datetime, timedelta

# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------
HASHES_PER_DIFFICULTY_UNIT = 2**32  # per Bitcoin protocol


def expected_hashes_for_one_block(difficulty: float) -> float:
    """Number of hashes needed on average to find a block."""
    return difficulty * HASHES_PER_DIFFICULTY_UNIT


def seconds_per_block(hash_rate: float, difficulty: float) -> float:
    """Expected seconds to find a block at a given hash rate."""
    if hash_rate <= 0:
        return float('inf')
    return expected_hashes_for_one_block(difficulty) / hash_rate


def daily_stats(hash_rate: float, difficulty: float, block_reward: float,
                btc_price: float, power_w: float, cost_per_kwh: float) -> dict:
    """Compute daily expected revenue, cost and net profit."""
    hashes_per_day = hash_rate * 86400.0
    prob_block_per_day = hashes_per_day / expected_hashes_for_one_block(difficulty)
    expected_blocks_per_day = prob_block_per_day  # since each trial is independent
    daily_btc = expected_blocks_per_day * block_reward
    daily_usd = daily_btc * btc_price

    # electricity cost
    kwh_per_day = power_w * 24.0 / 1000.0
    daily_cost = kwh_per_day * cost_per_kwh

    net_profit = daily_usd - daily_cost
    return {
        "hash_rate_hps": hash_rate,
        "power_w": power_w,
        "cost_per_kwh_usd": cost_per_kwh,
        "difficulty": difficulty,
        "block_reward_btc": block_reward,
        "btc_price_usd": btc_price,
        "hashes_per_day": hashes_per_day,
        "expected_blocks_per_day": expected_blocks_per_day,
        "daily_btc": daily_btc,
        "daily_usd": daily_usd,
        "daily_electricity_cost_usd": daily_cost,
        "net_daily_profit_usd": net_profit,
    }


def format_time(seconds: float) -> str:
    """Human‑readable time from seconds."""
    if seconds == float('inf'):
        return "∞ (hash rate zero)"
    td = timedelta(seconds=seconds)
    return str(td)


def ascii_bar(value: float, max_value: float, width: int = 30) -> str:
    """Simple horizontal bar."""
    if max_value <= 0:
        return ""
    filled = int(round(width * value / max_value))
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def prompt_float(prompt: str, default: float = None) -> float:
    while True:
        txt = input(f"{prompt}{' ['+str(default)+']' if default is not None else ''}: ").strip()
        if not txt and default is not None:
            return default
        try:
            return float(txt)
        except ValueError:
            print("Please enter a numeric value.")


def main() -> None:
    print("\n=== Bitcoin Mining Estimator (standard‑library only) ===\n")
    hash_rate = prompt_float("Hash rate (hashes per second, e.g. 500000)", default=500000)
    power_w = prompt_float("Power consumption (watts)", default=5.0)
    cost_per_kwh = prompt_float("Electricity cost (USD per kWh)", default=0.12)
    difficulty = prompt_float("Network difficulty (current difficulty)", default=60_000_000_000_000)
    block_reward = prompt_float("Block reward (BTC)", default=6.25)
    btc_price = prompt_float("BTC price (USD)", default=30000.0)

    # Compute stats
    secs = seconds_per_block(hash_rate, difficulty)
    daily = daily_stats(hash_rate, difficulty, block_reward, btc_price, power_w, cost_per_kwh)

    # Print summary
    print("\n--- Summary ---")
    print(f"Expected time to find ONE block: {format_time(secs)}")
    print(f"Expected blocks per day: {daily['expected_blocks_per_day']:.6f}")
    print(f"Daily BTC earned: {daily['daily_btc']:.8f} BTC")
    print(f"Daily revenue: ${daily['daily_usd']:.2f}")
    print(f"Daily electricity cost: ${daily['daily_electricity_cost_usd']:.2f}")
    print(f"Net daily profit: ${daily['net_daily_profit_usd']:.2f}")

    # ASCII chart for profit vs. time (1 day, 30 days, 365 days)
    periods = [1, 30, 365]
    max_profit = max(daily['net_daily_profit_usd'] * p for p in periods)
    print("\n--- Profit Projection (ASCII) ---")
    for days in periods:
        profit = daily['net_daily_profit_usd'] * days
        bar = ascii_bar(profit, max_profit)
        print(f"{days:3d}d: ${profit:8.2f} {bar}")

    # Save JSON report
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename = f"mining_estimate_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(daily, f, indent=2)
    print(f"\nReport saved to {os.path.abspath(filename)}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nInterrupted by user.")