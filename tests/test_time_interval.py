"""Test cases for TimeInterval.TimeInterval."""
from datetime import datetime, timedelta
import pytest

from time_interval import EMPTY, TimeInterval, create_empty_time_interval


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
    """Test intersection() for an interval nested completely in another."""
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
    """Test intersection against an empty time interval."""
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


def test_span(time_interval_1: TimeInterval, empty_time_interval: TimeInterval):
    """Test span() in different scenarios."""
    # span() is undefined on an empty interval.
    with pytest.raises(ValueError):
        empty_time_interval.span()

    assert time_interval_1.span() == time_interval_1.end - time_interval_1.begin


def test_equality(time_interval_1: TimeInterval, empty_time_interval: TimeInterval):
    """Test __eq__()."""
    assert time_interval_1 != empty_time_interval
    assert 1 != time_interval_1
    assert time_interval_1 != 1


def test_empty_is_canonical_singleton():
    """create_empty_time_interval() returns the shared EMPTY instance."""
    assert create_empty_time_interval() is EMPTY
    assert EMPTY.is_empty()


def test_empty_construction_raises_through_constructor():
    """The empty value cannot be built through the public constructor."""
    a = datetime.fromisoformat("2023-12-02T16:00:00")
    b = a + timedelta(minutes=5)
    with pytest.raises(ValueError):
        TimeInterval(b, a)


def test_point_interval_is_not_empty():
    """Intervals touching at one endpoint yield a non-empty point interval."""
    t = datetime.fromisoformat("2023-12-02T16:00:00")
    result = TimeInterval(t, t).intersection(TimeInterval(t, t))
    assert not result.is_empty()
    assert result.span() == timedelta(0)


def test_empty_is_absorbing(time_interval_1: TimeInterval):
    """EMPTY is absorbing under intersection, in both directions."""
    assert time_interval_1.intersection(EMPTY) is EMPTY
    assert EMPTY.intersection(time_interval_1) is EMPTY
    assert EMPTY.intersection(EMPTY) is EMPTY
