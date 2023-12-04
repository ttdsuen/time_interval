# Time Intervals in Python

An abstract data type for time intervals in Python.

## Description

A time interval is a two-tuple $(u, v)$
where $u$ and $v$ represent time, with $v\ge u$. Note if $u = v$,
the time interval becomes a point in time.

The span of a time interval is $v - u$. For any time intervals $A$ and $B$,
their intersection is
the time interval with maximum span that is inside both $A$ and $B$.
If no such time interval exists, the intersection is undefined.
This has implications in the implementation.

This package was motivated to help identify
overlapping login sessions for each indivdual user account, in
an attempt to catch illegal sharing of user accounts.

This package implements time interval in Python as `TimeInterval`. It supports intersection and span calculations. Internally, the start and end of the interval are represented as attributes `begin` and `end`. Note that `begin <= end` for all valid time intervals.

Since intersection is undefined if time intervals are disjoint. We implement this as an
invalid `TimeInterval` instance, with `begin > end`, and we call such instance `empty`.
If `C` is an instance of `TimeInterval` and is `empty`,
`C.intersection(x) == C, x.intersection(C) == C` for any time interval `x`.


## Installation

    pip install time_interval

## How to Use

    from datetime import datetime, timedelta
    from time_interval import TimeInterval

    now = datetime.utcnow()
    one_minute_interval = TimeInterval(now, now + timedelta(minutes=1))
    two_minute_interval = TimeInterval(now, now + timedelta(minutes=2))

    five_minutes_later = now + timedelta(minutes=5)
    later_time_interval = TimeInterval(
        five_minutes_later, five_minutes_later + timedelta(minutes=1))

    interval_x = one_minute_interval.intersection(two_minute_interval)
    assert interval_x == one_minute_interval # True
    assert interval_x.span() == timedelta(minutes=1) # True
    what = one_minute_interval.insersection(later_time_interval)
    # one_minute_interval and later_time_interval are disjoint,
    what.is_empty() # True
    what.span() # raises ValueError exception.
    # x is any instance of TimeInterval
    empty_time_interval.intersection(x) == empty_time_interval
    x.intersection(empty_time_interval) == empty_time_interval


## License

The time_interval module was written and maintained by Daniel Suen <ttdsuen@gmail.com>.

time_interval is released under MIT license.

See the file LICENSE for details.