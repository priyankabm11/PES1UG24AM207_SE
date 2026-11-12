
BERTHS = ["SU", "LB", "MB", "UB", "LB", "MB", "UB", "SL"]


def parse_pnr(pnr):
    try:
        if not isinstance(pnr, str) or len(pnr) != 10:
            return None
        if not pnr.isascii() or not pnr.isdigit():
            return None
        return int(pnr[0]), int(pnr[1:])
    except (ValueError, TypeError, IndexError):
        return None


def journey_distance(distances_csv):
    try:
        if not isinstance(distances_csv, str):
            return None

        distances = [
            int(d.strip())
            for d in distances_csv.split(',')
        ]

        if len(distances) < 2:
            return None

        return distances[-1] - distances[0]

    except (ValueError, TypeError, IndexError):
        return None


def berth_type(seat):
    try:
        if not isinstance(seat, str):
            return None

        parts = seat.split('-')

        if len(parts) != 2:
            return None

        coach, number = parts

        if not coach.strip() or not number.strip():
            return None

        return coach.upper(), BERTHS[int(number) % 8]

    except (ValueError, TypeError, IndexError):
        return None


def main():
    print("==== Running parse_pnr ====")
    user_input = input("Enter a 10 digit PNR (e.g. 4521367890): ")
    result = parse_pnr(user_input)
    print("Zone and Number:", result)

    print("\n==== Running journey_distance ====")
    user_input = input("Enter station distances as CSV (e.g. 0,120,340): ")
    result = journey_distance(user_input)
    print("Total Distance:", result)

    print("\n==== Running berth_type ====")
    user_input = input("Enter coach and seat (e.g. S3-45): ")
    result = berth_type(user_input)
    print("Coach and Berth:", result)


if __name__ == "__main__":
    main()
