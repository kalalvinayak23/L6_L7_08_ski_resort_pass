"""Hypothesis fuzzing and regression tests: PES2UG25AM809."""
from datetime import date
import math

import pytest
from hypothesis import given, settings, strategies as st

from processor import (parse_season_pass_validity, compute_trail_gradient,
                       calculate_lift_access_tier, main)


UNEXPECTED = st.one_of(st.text(), st.none(), st.integers(), st.floats(),
                       st.booleans(), st.binary(), st.lists(st.integers()),
                       st.dictionaries(st.text(), st.integers()))


@settings(max_examples=500, derandomize=True, report_multiple_bugs=False)
@given(UNEXPECTED)
def test_parse_season_pass_validity_no_crash(value):
    try:
        result = parse_season_pass_validity(value)
    except Exception as exc:
        pytest.fail(f"Unhandled {type(exc).__name__} for {value!r}: {exc}")
    assert isinstance(result, str)
    assert result == "INVALID_DATE" or result.startswith("Pass Expiry: ")


@settings(max_examples=500, derandomize=True, report_multiple_bugs=False)
@given(UNEXPECTED)
def test_compute_trail_gradient_safe(value):
    try:
        result = compute_trail_gradient(value)
    except Exception as exc:
        pytest.fail(f"Unhandled {type(exc).__name__} for {value!r}: {exc}")
    assert result is None or (isinstance(result, float) and
                              math.isfinite(result) and result >= 0)


@settings(max_examples=500, derandomize=True, report_multiple_bugs=False)
@given(UNEXPECTED)
def test_calculate_lift_access_tier_safe(value):
    try:
        result = calculate_lift_access_tier(value)
    except Exception as exc:
        pytest.fail(f"Unhandled {type(exc).__name__} for {value!r}: {exc}")
    assert result is None or result in {35.0, 60.0, 85.0, 110.0}


@settings(max_examples=300, derandomize=True)
@given(st.dates(min_value=date(1, 1, 1), max_value=date(9999, 12, 31)))
def test_real_calendar_dates_have_correct_status(value):
    text = f"{value.year:04d}/{value.month:02d}/{value.day:02d}"
    status = "VALID" if value.year >= 2026 else "EXPIRED"
    assert parse_season_pass_validity(text) == f"Pass Expiry: {value.isoformat()} ({status})"


@pytest.mark.parametrize("value", ["2026/02/29", "2026/02/30", "2026/04/31",
    "0000/01/01", "10000/01/01", "2026/00/01", "2026/13/01", "2026/01/00",
    "2026/01/32", "2026/1", "2026/1/1/2", "NaN", "２０２６/01/01"])
def test_bad_dates_are_rejected(value):
    assert parse_season_pass_validity(value) == "INVALID_DATE"


def test_leap_day_and_year_cutoff():
    assert parse_season_pass_validity("2028/02/29") == "Pass Expiry: 2028-02-29 (VALID)"
    assert parse_season_pass_validity("2025/12/31") == "Pass Expiry: 2025-12-31 (EXPIRED)"
    assert parse_season_pass_validity(" 2026/1/1 ") == "Pass Expiry: 2026-01-01 (VALID)"


@settings(max_examples=500, derandomize=True, report_multiple_bugs=False)
@given(drop=st.integers(0, 10**9), distance=st.integers(1, 10**9))
def test_valid_gradient_values(drop, distance):
    assert compute_trail_gradient(f"{drop}:{distance}") == round(drop / distance * 100, 2)


@pytest.mark.parametrize("value", ["1:0", "1:-1", "-1:1", "nan:1", "inf:1",
    "1:inf", "1:nan", "1e308:1e-308", "1:2:3", ":", "", "one:two",
    "1" * 300 + ":1"])
def test_invalid_gradients_return_none(value):
    assert compute_trail_gradient(value) is None


def test_zero_drop_and_whitespace():
    assert compute_trail_gradient("0:10") == 0.0
    assert compute_trail_gradient(" 250 : 1000 ") == 25.0


@settings(max_examples=200, derandomize=True)
@given(code=st.sampled_from(["BEG", "INT", "ADV", "ALL"]),
       padding=st.sampled_from(["", " ", "\t", "\n"]), lower=st.booleans())
def test_known_zone_prices(code, padding, lower):
    text = code.lower() if lower else code
    assert calculate_lift_access_tier(padding + text + padding) == {
        "BEG": 35.0, "INT": 60.0, "ADV": 85.0, "ALL": 110.0}[code]


def test_prefix_compatibility_and_unknown_zone():
    assert calculate_lift_access_tier("beginner") == 35.0
    assert calculate_lift_access_tier("advanced") == 85.0
    assert calculate_lift_access_tier("XYZ") is None
    assert calculate_lift_access_tier(" ") is None


@pytest.mark.parametrize("value", [None, 123, 1.5, True, b"2026/1/1", [], {}])
def test_non_string_inputs_have_documented_invalid_results(value):
    assert parse_season_pass_validity(value) == "INVALID_DATE"
    assert compute_trail_gradient(value) is None
    assert calculate_lift_access_tier(value) is None


@pytest.mark.parametrize("answers,expected", [
    (["2026/12/31", "250:1000", "BEG"], ["VALID", "25.0", "35.00"]),
    (["bad", "1:0", "XYZ"], ["INVALID_DATE", "Invalid gradient", "Invalid zone"])])
def test_cli_continues_through_all_three_functions(monkeypatch, capsys, answers, expected):
    values = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt: next(values))
    main()
    output = capsys.readouterr().out
    for text in expected:
        assert text in output
