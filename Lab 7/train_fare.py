"""Train-fare functions for Lab 7 fuzz testing."""

BERTHS = ["SU", "LB", "MB", "UB", "LB", "MB", "UB", "SL"]


def parse_pnr(pnr):
    """Return (zone, number) for a valid 10-digit PNR; otherwise return None."""
    if not isinstance(pnr, str):
        return None
    pnr = pnr.strip()
    if len(pnr) != 10 or not pnr.isascii() or not pnr.isdigit():
        return None
    return int(pnr[0]), int(pnr[1:])


def journey_distance(distances_csv):
    """Return last station distance minus first, or None for invalid input."""
    if not isinstance(distances_csv, str):
        return None
    parts = distances_csv.split(",")
    if not parts or any(not part.strip() for part in parts):
        return None
    try:
        distances = [int(part.strip()) for part in parts]
    except (TypeError, ValueError):
        return None
    return distances[-1] - distances[0]


def berth_type(seat):
    """Return normalized coach and berth; return None for malformed seats."""
    if not isinstance(seat, str) or seat.count("-") != 1:
        return None
    coach, number_text = (part.strip() for part in seat.split("-"))
    if not coach or not number_text:
        return None
    try:
        number = int(number_text)
    except (TypeError, ValueError):
        return None
    if number <= 0:
        return None
    # Preserve the assignment's original one-based seat-to-berth mapping.
    return coach.upper(), BERTHS[number % len(BERTHS)]


def main():
    print("==== Running parse_pnr ====")
    pnr_result = parse_pnr(input("Enter a 10 digit PNR (e.g. 4521367890): "))
    print("Zone and Number:", pnr_result)

    print("\n==== Running journey_distance ====")
    distance_result = journey_distance(
        input("Enter station distances as CSV (e.g. 0,120,340): ")
    )
    print("Total Distance:", distance_result)

    print("\n==== Running berth_type ====")
    berth_result = berth_type(input("Enter coach and seat (e.g. S3-45): "))
    print("Coach and Berth:", berth_result)


if __name__ == "__main__":
    main()
