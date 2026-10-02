"""Implementation of the time_interval module."""
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass(eq=False, frozen=True)
class TimeInterval:
    """Implementation of TimeInterval concept.

    Instances are immutable (``frozen=True``).

    The class invariant is ``begin <= end``, enforced by ``__post_init__``.
    The empty interval -- the absence of a range, i.e. the result of
    intersecting two disjoint intervals -- cannot satisfy that invariant, so
    it is not reachable through the public constructor. It is instead the
    single module-level ``EMPTY`` singleton (see ``_make_empty``), which the
    class treats as a distinct case in ``is_empty``/``__eq__``.
    """

    begin: datetime
    end: datetime

    def __post_init__(self):
        if self.end < self.begin:
            raise ValueError("invalid time interval, end >= begin")

    def intersection(self, ti: "TimeInterval") -> "TimeInterval":
        """Return the overlap of ``self`` and ``ti``.

        The intersection is the interval with the latest begin and the
        earliest end. Empty is absorbing: intersecting anything with an empty
        interval yields empty. Disjoint (or merely non-overlapping) intervals
        also yield empty. Intervals that touch at a single endpoint yield the
        degenerate point interval ``(t, t)``, which is *not* empty.
        """
        if self.is_empty() or ti.is_empty():
            return EMPTY
        begin = max(self.begin, ti.begin)
        end = min(self.end, ti.end)
        if begin > end:
            return EMPTY
        return TimeInterval(begin, end)

    def span(self) -> timedelta:
        """Returns length of TimeInterval as datetime.timedelta.
        It is an error (ValueError exception) to do a
        span() on an empty TimeInterval."""
        if self.is_empty():
            raise ValueError("span() is undefined on empty interval")
        return self.end - self.begin

    def is_empty(self) -> bool:
        """Returns if this is an empty TimeInterval."""
        return self.end < self.begin

    def __eq__(self, other: object) -> bool:
        if isinstance(other, TimeInterval):
            if self.is_empty() and other.is_empty():
                return True
            if self.is_empty() or other.is_empty():
                return False
            return self.begin == other.begin and self.end == other.end
        return False

    def __hash__(self) -> int:
        # Must agree with __eq__: every empty interval compares equal, so all
        # empties share one hash; non-empty intervals hash by their endpoints.
        if self.is_empty():
            return hash(())
        return hash((self.begin, self.end))


def _make_empty() -> TimeInterval:
    """Build the one sanctioned empty TimeInterval.

    ``begin <= end`` is the class invariant, so an empty value (``begin >
    end``) cannot come through the validated constructor. It is constructed
    here, deliberately, bypassing both ``__init__``/``__post_init__`` and the
    frozen ``__setattr__``. All empties compare equal (see ``__eq__``), so a
    single shared instance is sufficient.
    """
    obj = object.__new__(TimeInterval)
    object.__setattr__(obj, "begin", datetime.max)
    object.__setattr__(obj, "end", datetime.min)
    return obj


#: The canonical empty interval. Returned by every operation that has no
#: valid overlap, and absorbing under ``intersection``.
EMPTY = _make_empty()


def create_empty_time_interval() -> TimeInterval:
    """Return the canonical empty TimeInterval."""
    return EMPTY
