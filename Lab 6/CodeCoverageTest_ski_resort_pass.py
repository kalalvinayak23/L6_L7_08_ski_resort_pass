"""Lab 6 line coverage: Vinayak Yuvraj Kalal, PES2UG25AM809."""
import pytest

from ski_resort_pass import process_resort_bookings, check_chairlift_anemometer


def active(duration="full_day", skiers=None, **extras):
    return dict(is_active=True, duration=duration,
                skiers=[] if skiers is None else skiers, **extras)


@pytest.mark.parametrize("groups,fee", [(None, 15), ([], -1)])
def test_invalid_arguments(groups, fee):
    with pytest.raises(ValueError, match="Invalid groups"):
        process_resort_bookings(groups, fee)


def test_empty_and_inactive_groups():
    assert process_resort_bookings([], 15) == {
        "total_revenue": 0.0, "status": "ZERO_SALES"}
    assert process_resort_bookings([{}, {"is_active": False}], 15) == {
        "total_revenue": 0.0, "status": "ZERO_SALES"}


@pytest.mark.parametrize("duration,amount", [
    ("season", 300.0), ("full_day", 80.0), ("half_day", 50.0)])
def test_pass_prices(duration, amount):
    assert process_resort_bookings([active(duration, [{"age": 30}])], 15) == {
        "total_revenue": amount, "status": "COMPLETED"}


def test_age_discounts_rental_and_locker():
    # Child 48+35, senior 56, adult 80, locker 15 = 234.
    group = active(skiers=[{"age": 11, "gear_rental": True},
                           {"age": 65}, {"age": 30}],
                   includes_lodge_locker=True)
    assert process_resort_bookings([group], 15) == {
        "total_revenue": 234.0, "status": "COMPLETED"}


def test_invalid_duration_and_skier_age():
    groups = [active("invalid"), active(skiers=[{"age": 0}, {"age": -1}, {}])]
    assert process_resort_bookings(groups, 15) == {
        "total_revenue": 0.0, "status": "ZERO_SALES"}


def test_full_day_blackout_charge():
    group = active(skiers=[{"age": 30, "blackout_override": True,
                            "gear_rental": True}])
    assert process_resort_bookings([group], 15) == {
        "total_revenue": 75.0, "status": "COMPLETED"}


def test_half_day_blackout_clears_group_and_stops_loop():
    group = active("half_day", [{"age": 30},
                               {"age": 30, "blackout_override": True},
                               {"age": 30}])
    assert process_resort_bookings([group], 15) == {
        "total_revenue": 0.0, "status": "ZERO_SALES"}


def test_audit_review_overrides_zero_sales():
    assert process_resort_bookings([active("invalid") for _ in range(5)], 15) == {
        "total_revenue": 0.0, "status": "AUDIT_REVIEW"}


def test_no_anemometer_data():
    assert check_chairlift_anemometer([]) == "NO_DATA"


def test_safe_readings_reset_streak():
    assert check_chairlift_anemometer([[46, 45, 46], []]) == "SAFE_OPERATION"


def test_consecutive_gusts_suspend_lift():
    assert check_chairlift_anemometer([[46, 47]]) == "SUSPEND_LIFT"
