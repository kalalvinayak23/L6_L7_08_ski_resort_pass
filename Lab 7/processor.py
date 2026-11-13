"""Validated ski-resort inputs. Vinayak Yuvraj Kalal | PES2UG25AM809.

Invalid dates return 'INVALID_DATE'; invalid gradients and zones return None.
The starter's year >= 2026 rule and three-character zone prefixes are retained.
"""
from datetime import date
import math
import re


def parse_season_pass_validity(date_str):
    """Parse a real calendar date; classify using the lab's fixed year rule."""
    if not isinstance(date_str, str) or len(date_str) > 64:
        return "INVALID_DATE"
    match = re.fullmatch(r"([0-9]{1,4})/([0-9]{1,2})/([0-9]{1,2})", date_str.strip())
    if match is None:
        return "INVALID_DATE"
    try:
        expiry = date(*(int(part) for part in match.groups()))
    except ValueError:
        return "INVALID_DATE"
    status = "VALID" if expiry.year >= 2026 else "EXPIRED"
    return f"Pass Expiry: {expiry.isoformat()} ({status})"

def compute_trail_gradient(elevation_str):
    """Return a finite, nonnegative percentage or None for invalid input."""
    if not isinstance(elevation_str, str) or len(elevation_str) > 256:
        return None
    parts = elevation_str.split(':')
    if len(parts) != 2:
        return None
    try:
        drop, distance = (float(part) for part in parts)
    except (ValueError, OverflowError):
        return None
    if not math.isfinite(drop) or not math.isfinite(distance):
        return None
    if drop < 0 or distance <= 0:
        return None
    gradient_pct = (drop / distance) * 100.0
    if not math.isfinite(gradient_pct):
        return None
    return round(gradient_pct, 2)

def calculate_lift_access_tier(zone_code):
    """Preserve the starter's BEG/INT/ADV/ALL prefix convention."""
    if not isinstance(zone_code, str):
        return None
    prefix = zone_code.strip()[:3].upper()
    zone_rates = {
        "BEG": 35.0,
        "INT": 60.0,
        "ADV": 85.0,
        "ALL": 110.0
    }
    return zone_rates.get(prefix)

def main():
    print("==== Running parse_season_pass_validity ====")
    d_input = input("Enter pass expiry (YYYY/MM/DD): ")
    print(parse_season_pass_validity(d_input))

    print("\n==== Running compute_trail_gradient ====")
    e_input = input("Enter drop:distance (e.g. 250:1000): ")
    gradient = compute_trail_gradient(e_input)
    print("Invalid gradient: use a finite drop >= 0 and distance > 0."
          if gradient is None else f"Gradient %: {gradient}")

    print("\n==== Running calculate_lift_access_tier ====")
    z_input = input("Enter zone code (e.g. BEG, INT, ALL): ")
    price = calculate_lift_access_tier(z_input)
    print("Invalid zone: use BEG, INT, ADV, or ALL."
          if price is None else f"Lift Pass Price: $ {price:.2f}")

if __name__ == "__main__":
    main()
