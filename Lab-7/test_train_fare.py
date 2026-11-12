"""Property-based fuzz tests for the Train Fare Lab 7 functions."""

import pytest
from hypothesis import given, settings, strategies as st

from train_fare import BERTHS, berth_type, journey_distance, parse_pnr


FUZZ_INPUTS = st.one_of(
    st.text(),
    st.none(),
    st.integers(),
    st.lists(st.integers(), max_size=8),
)


@settings(max_examples=300, deadline=None)
@given(FUZZ_INPUTS)
def test_parse_pnr_handles_arbitrary_inputs(value):
    """Only a valid 10-digit PNR succeeds; malformed values fail predictably."""
    try:
        zone, number = parse_pnr(value)
    except ValueError:
        return
    assert isinstance(value, str)
    normalized = value.strip()
    assert len(normalized) == 10 and normalized.isascii() and normalized.isdigit()
    assert zone == int(normalized[0])
    assert number == int(normalized[1:])


@settings(max_examples=300, deadline=None)
@given(FUZZ_INPUTS)
def test_journey_distance_handles_arbitrary_inputs(value):
    """Accepted CSV inputs contain ordered non-negative integers."""
    try:
        result = journey_distance(value)
    except ValueError:
        return
    assert isinstance(value, str)
    distances = [int(part.strip()) for part in value.strip().split(",")]
    assert len(distances) >= 2
    assert distances == sorted(distances)
    assert result == distances[-1] - distances[0]


@settings(max_examples=300, deadline=None)
@given(FUZZ_INPUTS)
def test_berth_type_handles_arbitrary_inputs(value):
    """Accepted seats map to one of the eight berth positions."""
    try:
        coach, berth = berth_type(value)
    except ValueError:
        return
    assert isinstance(value, str)
    assert coach and coach.isupper()
    assert berth in BERTHS


@given(st.integers(min_value=1, max_value=10**9))
def test_valid_pnr_round_trip(number):
    pnr = f"{number:010d}"
    assert parse_pnr(pnr) == (int(pnr[0]), int(pnr[1:]))


@given(st.lists(st.integers(min_value=0, max_value=10**7), min_size=2, max_size=20))
def test_valid_journey_distance_matches_endpoints(distances):
    ordered = sorted(distances)
    csv_value = ",".join(map(str, ordered))
    assert journey_distance(csv_value) == ordered[-1] - ordered[0]


@given(st.integers(min_value=1, max_value=10000))
def test_valid_seat_uses_cyclic_berth_mapping(number):
    assert berth_type(f"S3-{number}") == ("S3", BERTHS[(number - 1) % 8])


@pytest.mark.parametrize("bad_pnr", ["", "123", "12345678901", "12345abc90", None, 1234567890])
def test_invalid_pnr_is_rejected(bad_pnr):
    with pytest.raises(ValueError):
        parse_pnr(bad_pnr)


@pytest.mark.parametrize("bad_distances", ["", "1", "1,,3", "1,abc,3", "3,2", None, 123])
def test_invalid_distances_are_rejected(bad_distances):
    with pytest.raises(ValueError):
        journey_distance(bad_distances)


@pytest.mark.parametrize("bad_seat", ["", "S3", "S3-0", "S3-x", "-45", "S3-45-extra", None, 45])
def test_invalid_seats_are_rejected(bad_seat):
    with pytest.raises(ValueError):
        berth_type(bad_seat)
