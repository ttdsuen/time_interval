# Time Intervals in Python

An abstract data type for time intervals, providing intersection and span
calculations with a single canonical **empty** interval for the no-overlap case.

## Description

A time interval is a pair `(begin, end)` of `datetime` values with the class
invariant

    begin <= end

When `begin == end` the interval is a single point in time.

The **span** of an interval is `end - begin`. The **intersection** of two
intervals `A` and `B` is the largest interval contained in both — that is, the
interval whose `begin` is the later of the two begins and whose `end` is the
earlier of the two ends.

This package was motivated by a need to identify overlapping login sessions for
each individual user account, in an attempt to catch illegal sharing of
accounts.

### The empty interval

Two disjoint intervals have no intersection. Instead of returning `None` and
forcing every caller to check, this package represents "no overlap" as a
distinct value: the **empty interval**.

An empty interval is not a range, so it cannot satisfy `begin <= end`. It is
therefore **not reachable through the public constructor**: constructing
`TimeInterval(b, a)` with `a > b` raises `ValueError`. There is exactly one
empty interval — the module-level singleton `EMPTY`, which is also returned by
`create_empty_time_interval()`.

Empty is **absorbing** under intersection:

```python
EMPTY.intersection(x) == EMPTY
x.intersection(EMPTY) == EMPTY
```

for any interval `x`.

Two intervals that merely touch at a single endpoint *do* overlap: their
intersection is the point interval `(t, t)`, which is **not** empty and has
span zero.

## Installation

The import name is `time_interval`. Install from a clone or directly from the
repository:

```bash
# from a local checkout
pip install .

# or straight from git
pip install git+https://github.com/ttdsuen/time_interval.git
```

The project is managed with [Poetry](https://python-poetry.org/). To set up a
development environment with the test dependencies:

```bash
poetry install --with dev
```

## How to Use

```python
from datetime import datetime, timedelta, UTC

from time_interval import EMPTY, TimeInterval, create_empty_time_interval

now = datetime.now(UTC)

one_minute = TimeInterval(now, now + timedelta(minutes=1))
two_minutes = TimeInterval(now, now + timedelta(minutes=2))

# one_minute is nested inside two_minutes, so the overlap is one_minute.
overlap = one_minute.intersection(two_minutes)
assert overlap == one_minute
assert overlap.span() == timedelta(minutes=1)

# A window five minutes later does not overlap one_minute.
later_start = now + timedelta(minutes=5)
later = TimeInterval(later_start, later_start + timedelta(minutes=5))

assert one_minute.intersection(later) is EMPTY
assert one_minute.intersection(later).is_empty()

# EMPTY is absorbing, in both directions.
assert EMPTY.intersection(one_minute) is EMPTY
assert one_minute.intersection(EMPTY) is EMPTY

# create_empty_time_interval() returns the same canonical singleton.
assert create_empty_time_interval() is EMPTY

# span() is undefined on an empty interval and raises ValueError.
try:
    EMPTY.span()
except ValueError:
    pass
```

## API

### `TimeInterval(begin, end)`

Constructs an interval. Raises `ValueError` if `end < begin`.

- `begin`, `end` — the endpoints, as `datetime` values.
- `intersection(other) -> TimeInterval` — the largest interval contained in
  both `self` and `other`; returns `EMPTY` when they do not overlap.
- `span() -> timedelta` — `end - begin`. Raises `ValueError` on an empty
  interval.
- `is_empty() -> bool` — whether this is the empty interval.
- `__eq__` — two non-empty intervals are equal when both endpoints match; all
  empty intervals are equal to each other.

### `EMPTY`

The canonical empty interval. Absorbing under `intersection`. Test whether an
interval is empty with `is_empty()` rather than by inspecting `begin`/`end`.

### `create_empty_time_interval() -> TimeInterval`

Returns the canonical empty interval (`EMPTY`).

## Development

```bash
poetry install --with dev
poetry run pytest
```

## License

The `time_interval` module was written and maintained by
Daniel Suen <ttdsuen@gmail.com>.

`time_interval` is released under the MIT license.

See the file [LICENSE](LICENSE) for details.
