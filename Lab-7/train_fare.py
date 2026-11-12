"""Train-fare helper functions hardened against malformed input."""

import re

BERTHS = ["SU", "LB", "MB", "UB", "LB", "MB", "UB", "SL"]
_PNR_PATTERN = re.compile(r"^[0-9]{10}$")
_COACH_PATTERN = re.compile(r"^[A-Za-z]+[0-9]*$")


def _require_text(value, field_name):
    """Return a stripped string or raise a consistent, descriptive error."""
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    return value.strip()


def parse_pnr(pnr):
    """Split a 10-digit PNR into its first-digit zone and 9-digit number."""
    pnr = _require_text(pnr, "PNR")
    if not _PNR_PATTERN.fullmatch(pnr):
        raise ValueError("PNR must contain exactly 10 digits")
    return int(pnr[0]), int(pnr[1:])


def journey_distance(distances_csv):
    """Return the distance between the first and last listed stations."""
    distances_csv = _require_text(distances_csv, "Distances")
    if not distances_csv:
        raise ValueError("At least two station distances are required")

    parts = [part.strip() for part in distances_csv.split(",")]
    if len(parts) < 2 or any(not part for part in parts):
        raise ValueError("Provide at least two comma-separated distances")
    if any(not re.fullmatch(r"[0-9]+", part) for part in parts):
        raise ValueError("Station distances must be non-negative integers")

    distances = [int(part) for part in parts]
    if any(current < previous for previous, current in zip(distances, distances[1:])):
        raise ValueError("Station distances must be in non-decreasing order")
    return distances[-1] - distances[0]


def berth_type(seat):
    """Return the normalized coach and berth for a positive seat number."""
    seat = _require_text(seat, "Seat")
    if seat.count("-") != 1:
        raise ValueError("Seat must use COACH-NUMBER format, for example S3-45")

    coach, number_text = (part.strip() for part in seat.split("-"))
    if not _COACH_PATTERN.fullmatch(coach):
        raise ValueError("Coach must contain letters optionally followed by digits")
    if not re.fullmatch(r"[0-9]+", number_text):
        raise ValueError("Seat number must be a positive integer")

    number = int(number_text)
    if number <= 0:
        raise ValueError("Seat number must be a positive integer")
    return coach.upper(), BERTHS[(number - 1) % len(BERTHS)]


def main():
    """Run the three functions interactively, reporting invalid input cleanly."""
    print("==== Running parse_pnr ====")
    try:
        result = parse_pnr(input("Enter a 10 digit PNR (e.g. 4521367890): "))
        print("Zone and Number:", result)
    except ValueError as error:
        print("Invalid PNR:", error)

    print("\n==== Running journey_distance ====")
    try:
        result = journey_distance(input("Enter station distances as CSV (e.g. 0,120,340): "))
        print("Total Distance:", result)
    except ValueError as error:
        print("Invalid distances:", error)

    print("\n==== Running berth_type ====")
    try:
        result = berth_type(input("Enter coach and seat (e.g. S3-45): "))
        print("Coach and Berth:", result)
    except ValueError as error:
        print("Invalid seat:", error)


if __name__ == "__main__":
    main()
