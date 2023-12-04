"""Test cases for TimeInterval.TimeInterval."""
from datetime import datetime, timedelta
import pytest

from time_interval import TimeInterval, create_empty_time_interval


# pylint: disable=redefined-outer-name


@pytest.fixture
def time_interval_1() -> TimeInterval:
    """Fixture TimeInterval 1."""
    begin = datetime.fromisoformat("2023-12-02T16:47:00")
    return TimeInterval(begin, begin + timedelta(minutes=5))


@pytest.fixture
def time_interval_2() -> TimeInterval:
    """Fixture TimeInterval 2."""
    begin = datetime.fromisoformat("2023-12-02T16:00:00")
    return TimeInterval(begin, begin + timedelta(hours=1))


@pytest.fixture
def time_interval_3() -> TimeInterval:
    """Fixture TimeInterval 3."""
    begin = datetime.fromisoformat("2023-12-02T15:30:00")
    return TimeInterval(begin, begin + timedelta(hours=1))


@pytest.fixture
def time_interval_4() -> TimeInterval:
    """Fixture TimeInterval 4."""
    begin = datetime.fromisoformat("2023-12-02T16:00:00")
    return TimeInterval(begin, begin + timedelta(minutes=30))


@pytest.fixture
def time_interval_5() -> TimeInterval:
    """Fixture TimeInterval 5."""
    begin = datetime.fromisoformat("2023-12-02T16:05:00")
    return TimeInterval(begin, begin + timedelta(minutes=10))


@pytest.fixture
def empty_time_interval() -> TimeInterval:
    """Fixture empty time interval."""
    return create_empty_time_interval()


def test_intersection_complete_cover(
    time_interval_1: TimeInterval, time_interval_2: TimeInterval
):
    """Test interextion() for an interval nested completely in another."""
    assert time_interval_1.intersection(time_interval_2) == time_interval_1
    assert time_interval_2.intersection(time_interval_1) == time_interval_1
    assert time_interval_1.intersection(time_interval_1) == time_interval_1
    assert time_interval_2.intersection(time_interval_2) == time_interval_2


def test_intersection_endpoint_overlaps(time_interval_1: TimeInterval):
    """Test intersection() for intervals overlapped at a single endpoint."""
    time_interval_after = TimeInterval(
        time_interval_1.end, time_interval_1.end + timedelta(minutes=1)
    )
    expected_result = TimeInterval(time_interval_1.end, time_interval_1.end)
    assert time_interval_1.intersection(time_interval_after) == expected_result
    assert time_interval_after.intersection(time_interval_1) == expected_result

    time_interval_before = TimeInterval(
        time_interval_1.begin - timedelta(minutes=1), time_interval_1.begin
    )
    expected_result = TimeInterval(time_interval_1.begin, time_interval_1.begin)
    assert time_interval_1.intersection(time_interval_before) == expected_result
    assert time_interval_before.intersection(time_interval_1) == expected_result


def test_intersection_disconnects(time_interval_1: TimeInterval, empty_time_interval: TimeInterval):
    """Test completely disconnected time intervals - no overlapping."""
    time_interval_after = TimeInterval(
        time_interval_1.end + timedelta(minutes=1),
        time_interval_1.end + timedelta(minutes=2),
    )
    assert time_interval_1.intersection(time_interval_after).is_empty()
    assert time_interval_after.intersection(time_interval_1).is_empty()
    assert time_interval_1.intersection(time_interval_after) == empty_time_interval
    assert time_interval_after.intersection(time_interval_1) == empty_time_interval

    time_interval_before = TimeInterval(
        time_interval_1.begin - timedelta(minutes=2),
        time_interval_1.begin - timedelta(minutes=1),
    )
    assert time_interval_1.intersection(time_interval_before).is_empty()
    assert time_interval_before.intersection(time_interval_1).is_empty()
    assert time_interval_1.intersection(time_interval_before) == empty_time_interval
    assert time_interval_before.intersection(time_interval_1) == empty_time_interval


def test_intersection_with_empty_time_interval(
    time_interval_1: TimeInterval, empty_time_interval: TimeInterval):
    """Test intersection against empty tiem interval."""
    assert time_interval_1.intersection(empty_time_interval) == empty_time_interval
    assert empty_time_interval.intersection(time_interval_1) == empty_time_interval


def test_intersection_partial_overlaps(
    time_interval_2: TimeInterval,
    time_interval_3: TimeInterval,
    time_interval_4: TimeInterval,
    time_interval_5: TimeInterval,
):
    """Test partial overlappings."""
    assert time_interval_2.intersection(time_interval_3) == time_interval_4
    assert time_interval_3.intersection(time_interval_2) == time_interval_4

    assert time_interval_2.intersection(time_interval_5) == time_interval_5
    assert time_interval_5.intersection(time_interval_2) == time_interval_5

def test_direct_empty_time_interval_creation():
    """Test direct empty time interval creation, should raise ValueError."""
    now = datetime.now()
    try:
        TimeInterval(now, now - timedelta(minutes=1))
        assert False
    except ValueError:
        assert True


def test_span(time_interval_1: TimeInterval, empty_time_interval: TimeInterval):
    """Test span() in different scenarios."""

    # empty time interval, span() raises ValueError
    try:
        empty_time_interval.span()
        assert False
    except ValueError:
        assert True

    assert time_interval_1.span() == time_interval_1.end - time_interval_1.begin


def test_eqality(time_interval_1: TimeInterval, empty_time_interval: TimeInterval):
    """Test __eq__()."""
    assert time_interval_1 != empty_time_interval
    assert 1 != time_interval_1
    assert time_interval_1 != 1
