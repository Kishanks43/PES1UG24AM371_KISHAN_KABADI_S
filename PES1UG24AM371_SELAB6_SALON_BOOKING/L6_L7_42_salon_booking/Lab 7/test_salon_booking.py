from hypothesis import given, strategies as st
import pytest
from salon_booking import parse_booking, duration_average, payable_bill


@given(st.text() | st.none())
def test_parse_booking_no_crash(s):
    try:
        result = parse_booking(s)
    except (ValueError, AttributeError):
        return
    assert isinstance(result, tuple) and len(result) == 2
    service, minutes = result
    assert isinstance(service, str)
    assert isinstance(minutes, float)


@given(st.text() | st.none())
def test_duration_average_no_crash(s):
    try:
        result = duration_average(s)
    except (ValueError, AttributeError, ZeroDivisionError):
        return
    assert isinstance(result, int)


@given(st.text() | st.none())
def test_payable_bill_no_crash(s):
    try:
        result = payable_bill(s)
    except (ValueError, AttributeError):
        return
    assert isinstance(result, (int, float))
    assert result >= 0


def test_parse_booking_valid():
    assert parse_booking("haircut:45") == ("Haircut", 45.0)
    assert parse_booking(" colour : 60 ") == ("Colour", 60.0)


def test_duration_average_valid():
    assert duration_average("30,45,60") == 45
    assert duration_average("10,20") == 15


def test_payable_bill_valid():
    assert payable_bill("800|100") == 844.0
    assert payable_bill("100|200") == 0
