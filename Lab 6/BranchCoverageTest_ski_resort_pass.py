"""Lab 6 branch coverage and boundaries: PES2UG25AM809."""
import pytest

from ski_resort_pass import process_resort_bookings, check_chairlift_anemometer


def group(skiers=None, **changes):
    return {"is_active": True, "duration": "full_day",
            "skiers": [] if skiers is None else skiers, **changes}


@pytest.mark.parametrize("groups,fee", [(None, 0), ({}, 0), ([], -0.01)])
def test_validation_rejects_bad_inputs(groups, fee):
    with pytest.raises(ValueError):
        process_resort_bookings(groups, fee)


@pytest.mark.parametrize("groups", [[], [{}], [{"is_active": False}], [group()]])
def test_zero_sales_paths(groups):
    assert process_resort_bookings(groups, 0) == {
        "total_revenue": 0.0, "status": "ZERO_SALES"}


@pytest.mark.parametrize("duration,base", [
    ("season", 300), ("full_day", 80), ("half_day", 50)])
@pytest.mark.parametrize("age,factor", [(1, .6), (11, .6), (12, 1),
                                        (64, 1), (65, .7), (100, .7)])
def test_duration_and_age_boundaries(duration, base, age, factor):
    assert process_resort_bookings([group([{"age": age}], duration=duration)], 15) == {
        "total_revenue": round(base * factor, 2), "status": "COMPLETED"}


def test_missing_duration_defaults_to_full_day():
    assert process_resort_bookings([{"is_active": True, "skiers": [{"age": 30}]}], 0) == {
        "total_revenue": 80.0, "status": "COMPLETED"}


@pytest.mark.parametrize("rejections,status", [(4, "ZERO_SALES"), (5, "AUDIT_REVIEW")])
def test_invalid_duration_audit_boundary(rejections, status):
    assert process_resort_bookings([group(duration="bad") for _ in range(rejections)], 0) == {
        "total_revenue": 0.0, "status": status}


def test_invalid_ages_are_skipped_and_later_skier_is_processed():
    assert process_resort_bookings([group([{}, {"age": 0}, {"age": -5}, {"age": 12}])], 0) == {
        "total_revenue": 80.0, "status": "COMPLETED"}


@pytest.mark.parametrize("duration,amount", [("season", 150), ("full_day", 40)])
@pytest.mark.parametrize("gear", [False, True])
def test_blackout_non_half_day_and_gear(duration, amount, gear):
    skiers = [{"age": 10, "blackout_override": True, "gear_rental": gear}]
    assert process_resort_bookings([group(skiers, duration=duration)], 0) == {
        "total_revenue": amount + (35 if gear else 0), "status": "COMPLETED"}


@pytest.mark.parametrize("locker,fee,expected", [(False, 15, 0), (True, 15, 15), (True, 0, 0)])
def test_half_day_blackout_break_and_locker(locker, fee, expected):
    skiers = [{"age": 30, "gear_rental": True},
              {"age": 30, "blackout_override": True, "gear_rental": True},
              {"age": 30}]
    assert process_resort_bookings([group(skiers, duration="half_day",
                                          includes_lodge_locker=locker)], fee) == {
        "total_revenue": expected, "status": "COMPLETED" if expected else "ZERO_SALES"}


def test_multiple_groups_sum_and_round():
    groups = [group([{"age": 30, "gear_rental": True}], includes_lodge_locker=True),
              group([{"age": 65}], duration="half_day")]
    assert process_resort_bookings(groups, 15.126) == {
        "total_revenue": 165.13, "status": "COMPLETED"}


def test_audit_with_positive_revenue():
    groups = [group([{"age": 0}] * 5 + [{"age": 30}])]
    assert process_resort_bookings(groups, 0) == {
        "total_revenue": 80.0, "status": "AUDIT_REVIEW"}


@pytest.mark.parametrize("streams,expected", [
    ([], "NO_DATA"), (None, "NO_DATA"), ([[]], "SAFE_OPERATION"),
    ([[0, 45]], "SAFE_OPERATION"), ([[46]], "SAFE_OPERATION"),
    ([[46, 45, 46]], "SAFE_OPERATION"), ([[46], [47]], "SAFE_OPERATION"),
    ([[46, 47]], "SUSPEND_LIFT"), ([[], [45, 46, 47, 0]], "SUSPEND_LIFT")])
def test_anemometer_branches(streams, expected):
    assert check_chairlift_anemometer(streams) == expected
