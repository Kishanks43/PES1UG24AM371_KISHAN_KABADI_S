import pytest
from salon_booking import extra_time_charge, can_book, arrival_status

# --- Branch Coverage: extra_time_charge ---

def test_branch_service_validation():
    # True branch: service not in INCLUDED_MIN
    with pytest.raises(ValueError):
        extra_time_charge("invalid", 30, "junior", False)
    # False branch: service in INCLUDED_MIN
    assert extra_time_charge("haircut", 30, "junior", False) == 0

def test_branch_duration_validation():
    # True branch: duration_min < 0
    with pytest.raises(ValueError):
        extra_time_charge("haircut", -5, "junior", False)
    # False branch: duration_min >= 0
    assert extra_time_charge("haircut", 30, "junior", False) == 0

def test_branch_member_spa_condition():
    # is_member = True, service != "spa" -> True (included += 15)
    assert extra_time_charge("haircut", 45, "junior", True) == 0
    # is_member = True, service == "spa" -> False (no +15 bonus)
    assert extra_time_charge("spa", 100, "master", True) == 180
    # is_member = False -> False
    assert extra_time_charge("haircut", 40, "junior", False) == 100

def test_branch_extra_time_zero_vs_positive():
    # extra <= 0 -> True
    assert extra_time_charge("haircut", 20, "junior", False) == 0
    # extra > 0 -> False
    assert extra_time_charge("haircut", 40, "junior", False) > 0

def test_branch_stylist_levels():
    # stylist_level == "junior" -> True
    assert extra_time_charge("haircut", 40, "junior", False) == 100
    # stylist_level != "junior" -> False
    assert extra_time_charge("haircut", 40, "senior", False) == 180

def test_branch_extra_over_60_and_senior():
    # extra > 60 AND stylist_level == "senior" (rate = 18 + 8 + 4 = 30)
    assert extra_time_charge("colour", 130, "senior", False) == 2100
    # extra > 60 AND stylist_level != "senior" (rate = 10 + 8 = 18)
    assert extra_time_charge("haircut", 100, "junior", False) == 1260
    # extra <= 60 (rate unchanged)
    assert extra_time_charge("haircut", 50, "junior", False) == 200


# --- Branch Coverage: can_book ---

def test_branch_can_book_walk_in():
    # is_walk_in = True, party_size <= 2 -> True
    assert can_book(2, 1, True) is True
    # is_walk_in = True, party_size > 2 -> False
    assert can_book(3, 1, True) is False

def test_branch_can_book_party_size():
    # is_walk_in = False, party_size > 4 -> False
    assert can_book(5, 1, False) is False
    # is_walk_in = False, party_size <= 4, services <= 2 -> True
    assert can_book(4, 2, False) is True
    # is_walk_in = False, party_size <= 4, services > 2 -> False
    assert can_book(4, 3, False) is False


# --- Branch Coverage: arrival_status ---

def test_branch_arrival_status_cutoff_branches():
    # is_colour = True, is_weekend = False -> cutoff = 10
    assert arrival_status(10, True, False) == "open"
    # is_colour = False, is_weekend = True -> cutoff = 5 + 10 = 15
    assert arrival_status(15, False, True) == "open"

def test_branch_arrival_status_outcomes():
    # minutes_early >= cutoff -> "open"
    assert arrival_status(10, True, False) == "open"
    # minutes_early < cutoff AND minutes_early >= cutoff - 15 -> "late"
    assert arrival_status(0, True, False) == "late"
    # minutes_early < cutoff - 15 -> "closed"
    assert arrival_status(-10, True, False) == "closed"