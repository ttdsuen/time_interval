"""Implementation of the time_interval module."""
from datetime import datetime, timedelta
from dataclasses import dataclass


def create_empty_time_interval() -> "TimeInterval":
    """Create an instance of empty TimeInterval."""
    now = datetime.now()
    time_interval = TimeInterval(now, now + timedelta(seconds=10))
    time_interval.begin, time_interval.end = time_interval.end, time_interval.begin
    return time_interval


@dataclass(eq=False)
class TimeInterval:
    """Implementation of TimeInterval concept."""

    begin: datetime
    end: datetime

    def __post_init__(self):
        if self.end < self.begin:
            raise ValueError("invalid time interval, end >= begin")

    #
    # ref_time_interval - the longer of self and ti,
    # match_time_interval - the one different from ref_time_interval
    # Overlapping happens when either endpoints of
    # match_time_interval fall within ref_time_interval
    def intersection(self, ti: "TimeInterval") -> "TimeInterval":
        """Implements intersection on TimeIntervals."""
        try:
            ref_time_interval = self
            match_time_interval = ti
            if self.span() < ti.span():
                ref_time_interval = ti
                match_time_interval = self

            if (
                ref_time_interval.begin
                <= match_time_interval.begin
                <= ref_time_interval.end
            ):
                # ref.begin <= match_time_interval.begin <= ref.end
                if match_time_interval.end <= ref_time_interval.end:
                    return match_time_interval
                return TimeInterval(match_time_interval.begin, ref_time_interval.end)
            if (
                ref_time_interval.begin
                <= match_time_interval.end
                <= ref_time_interval.end
            ):
                # ref.begin <= match_time_interval.end <= ref.end
                return TimeInterval(
                    ref_time_interval.begin, match_time_interval.end
                )
            return create_empty_time_interval()
        except ValueError:
            # calling span() raises this exception if time interval is empty
            # and overlapping would be an empty time interval as well
            return create_empty_time_interval()

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
