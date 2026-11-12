"""Hypothesis fuzz tests for the assigned Train Fare functions."""

from hypothesis import given, strategies as st

from train_fare import BERTHS, berth_type, journey_distance, parse_pnr


ARBITRARY_INPUTS = st.one_of(
    st.text(),
    st.none(),
    st.integers(),
    st.lists(st.integers(), max_size=10),
)


@given(ARBITRARY_INPUTS)
def test_parse_pnr_no_crash(value):
    result = parse_pnr(value)
    assert result is None or (
        isinstance(result, tuple)
        and len(result) == 2
        and all(isinstance(part, int) for part in result)
    )


@given(ARBITRARY_INPUTS)
def test_journey_distance_no_crash(value):
    result = journey_distance(value)
    assert result is None or isinstance(result, int)


@given(ARBITRARY_INPUTS)
def test_berth_type_no_crash(value):
    result = berth_type(value)
    assert result is None or (
        isinstance(result, tuple)
        and len(result) == 2
        and isinstance(result[0], str)
        and result[1] in BERTHS
    )


@given(st.integers(min_value=0, max_value=9), st.integers(min_value=0, max_value=999999999))
def test_valid_pnr_is_parsed(zone, remainder):
    pnr = f"{zone}{remainder:09d}"
    assert parse_pnr(pnr) == (zone, remainder)


@given(st.lists(st.integers(), min_size=1, max_size=20))
def test_valid_distance_csv_preserves_endpoint_calculation(distances):
    csv_value = ",".join(str(value) for value in distances)
    assert journey_distance(csv_value) == distances[-1] - distances[0]


@given(st.integers(min_value=1, max_value=10000))
def test_valid_seat_preserves_original_berth_mapping(number):
    assert berth_type(f"S3-{number}") == ("S3", BERTHS[number % 8])


def test_standard_first_eight_berths():
    expected = ["LB", "MB", "UB", "LB", "MB", "UB", "SL", "SU"]
    assert [berth_type(f"S3-{seat}")[1] for seat in range(1, 9)] == expected


def test_invalid_values_return_none():
    assert parse_pnr(None) is None
    assert parse_pnr("123") is None
    assert journey_distance(None) is None
    assert journey_distance("1,,3") is None
    assert berth_type(None) is None
    assert berth_type("S3-0") is None
    assert berth_type("S3-x") is None
