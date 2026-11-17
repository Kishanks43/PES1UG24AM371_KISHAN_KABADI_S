import pytest
from salon_booking import extra_time_charge, can_book, arrival_status

# --- Tests for extra_time_charge ---

def test_extra_time_charge_unknown_service():
    with pytest.raises(ValueError, match="unknown service"):
        extra_time_charge("waxing", 30, "junior", False)

def test_extra_time_charge_invalid_duration():
    with pytest.raises(ValueError, match="invalid duration"):
        extra_time_charge("haircut", -10, "junior", False)

def test_extra_time_charge_within_included_time():
    assert extra_time_charge("haircut", 20, "junior", False) == 0

def test_extra_time_charge_junior_under_60_extra():
    # Haircut included = 30; extra = 40 - 30 = 10; rate = 10; total = 100
    assert extra_time_charge("haircut", 40, "junior", False) == 100

def test_extra_time_charge_senior_over_60_extra():
    # Colour included = 60; extra = 130 - 60 = 70 (> 60); rate = 18 + 8 + 4 = 30; total = 2100
    assert extra_time_charge("colour", 130, "senior", False) == 2100

def test_extra_time_charge_junior_over_60_extra():
    # Haircut included = 30; extra = 100 - 30 = 70 (> 60); rate = 10 + 8 = 18; total = 1260
    assert extra_time_charge("haircut", 100, "junior", False) == 1260

def test_extra_time_charge_member_non_spa():
    # Haircut included = 30 + 15 = 45; extra = 55 - 45 = 10; rate = 10; total = 100
    assert extra_time_charge("haircut", 55, "junior", True) == 100

def test_extra_time_charge_member_spa():
    # Spa included = 90 (no member bonus); extra = 100 - 90 = 10; rate = 18; total = 180
    assert extra_time_charge("spa", 100, "master", True) == 180


# --- Tests for can_book ---

def test_can_book_walk_in_success():
    assert can_book(2, 1, True) is True

def test_can_book_walk_in_too_large():
    assert can_book(3, 1, True) is False

def test_can_book_large_party():
    assert can_book(5, 1, False) is False

def test_can_book_advance_booking_success():
    assert can_book(4, 2, False) is True

def test_can_book_advance_booking_too_many_services():
    assert can_book(4, 3, False) is False


# --- Tests for arrival_status ---

def test_arrival_status_open():
    # Colour weekday: cutoff = 10; early = 10 -> open
    assert arrival_status(10, True, False) == "open"

def test_arrival_status_late():
    # Haircut weekend: cutoff = 5 + 10 = 15; early = 5 -> late (>= 0)
    assert arrival_status(5, False, True) == "late"

def test_arrival_status_closed():
    # Colour weekend: cutoff = 10 + 10 = 20; cutoff - 15 = 5; early = 0 -> closed
    assert arrival_status(0, True, True) == "closed"