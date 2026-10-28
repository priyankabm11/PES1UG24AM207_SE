import pytest
from train_fare import base_fare, concession, tatkal_charge


def test_base_fare_valid_and_minimum():
    assert base_fare("SL", 500) == 500
    assert base_fare("SL", 10) == 50


@pytest.mark.parametrize("travel_class", ["unknown", ""])
def test_base_fare_rejects_unknown_class(travel_class):
    with pytest.raises(ValueError, match="unknown class"):
        base_fare(travel_class, 100)


@pytest.mark.parametrize("distance", [0, -10])
def test_base_fare_rejects_invalid_distance(distance):
    with pytest.raises(ValueError, match="invalid distance"):
        base_fare("SL", distance)


def test_concession_tatkal():
    assert concession(3, "F", True) == 0


def test_concession_child_under_five():
    assert concession(4, "M", False) == 100


def test_concession_child_up_to_twelve():
    assert concession(12, "M", False) == 50


def test_concession_senior_woman():
    assert concession(60, "F", False) == 50


def test_concession_senior_man():
    assert concession(60, "M", False) == 40


def test_concession_adult():
    assert concession(30, "M", False) == 0


def test_tatkal_sleeper_minimum_and_regular_charge():
    assert tatkal_charge("SL", 500) == 100
    assert tatkal_charge("SL", 2000) == 200


def test_tatkal_other_class_minimum_and_regular_charge():
    assert tatkal_charge("3A", 100) == 100
    assert tatkal_charge("3A", 1000) == 300


def test_tatkal_charge_maximum():
    assert tatkal_charge("SL", 5000) == 400
    assert tatkal_charge("3A", 2000) == 400
