from datetime import timedelta
import math
import re
from typing import overload


NANOSECONDS_PER_TICK = 100
TICKS_PER_MICROSECOND = 10

TICKS_PER_MILLISECOND = 10_000
TICKS_PER_SECOND = 10_000_000
TICKS_PER_MINUTE = 600_000_000
TICKS_PER_HOUR = 36_000_000_000
TICKS_PER_DAY = 864_000_000_000

MICROSECONDS_PER_MILLISECOND = 1_000
MICROSECONDS_PER_SECOND = 1_000_000
MICROSECONDS_PER_MINUTE = 60_000_000
MICROSECONDS_PER_HOUR = 3_600_000_000
MICROSECONDS_PER_DAY = 86_400_000_000

MILLISECONDS_PER_SECOND = 1_000
MILLISECONDS_PER_MINUTE = 60_000
MILLISECONDS_PER_HOUR = 3_600_000
MILLISECONDS_PER_DAY = 86_400_000

SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 3_600
SECONDS_PER_DAY = 86_400

MINUTES_PER_HOUR = 60
MINUTES_PER_DAY = 1_440

HOURS_PER_DAY = 24

MIN_TICKS = -(2**63)
MAX_TICKS = 2**63 - 1

MIN_MICROSECONDS = -922_337_203_685_477_580
MAX_MICROSECONDS = +922_337_203_685_477_580

MIN_MILLISECONDS = -922_337_203_685_477
MAX_MILLISECONDS = +922_337_203_685_477

MIN_SECONDS = -922_337_203_685
MAX_SECONDS = +922_337_203_685

MIN_MINUTES = -15_372_286_728
MAX_MINUTES = +15_372_286_728

MIN_HOURS = -256_204_778
MAX_HOURS = +256_204_778

MIN_DAYS = -10_675_199
MAX_DAYS = +10_675_199

TICKS_PER_TENTH_SECOND = TICKS_PER_MILLISECOND * 100


class timespan:
    @overload
    def __init__(self, a: int) -> None:
        """ticks"""
        ...

    @overload
    def __init__(self, a: tuple[int, int, int]) -> None:
        """(hour, minute, second)"""
        ...

    @overload
    def __init__(self, a: tuple[int, int, int, int]) -> None:
        """(day, hour, minute, second)"""
        ...

    @overload
    def __init__(self, a: tuple[int, int, int, int, int]) -> None:
        """(day, hour, minute, second, millisecond)"""
        ...

    @overload
    def __init__(self, a: tuple[int, int, int, int, int, int]) -> None:
        """(day, hour, minute, second, millisecond, microsecond)"""
        ...

    def __init__(self, a) -> None:
        if isinstance(a, int):
            self.__ticks = a
        elif isinstance(a, tuple) and 3 <= len(a) <= 6:
            self.__ticks = time_to_ticks(*a)
        else:
            raise TypeError()

    @property
    def sign(self) -> int:
        return 1 if self.ticks > 0 else -1 if self.ticks < 0 else 0

    @property
    def ticks(self) -> int:
        return self.__ticks

    @property
    def days(self) -> int:
        return math.floor(self.ticks / TICKS_PER_DAY)

    @property
    def hours(self) -> int:
        return int((abs(self.ticks) % TICKS_PER_DAY) // TICKS_PER_HOUR) * self.sign

    @property
    def minutes(self) -> int:
        return int((abs(self.ticks) % TICKS_PER_HOUR) // TICKS_PER_MINUTE) * self.sign

    @property
    def seconds(self) -> int:
        return int((abs(self.ticks) % TICKS_PER_MINUTE) // TICKS_PER_SECOND) * self.sign

    @property
    def milliseconds(self) -> int:
        return (
            int((abs(self.ticks) % TICKS_PER_SECOND) // TICKS_PER_MILLISECOND)
            * self.sign
        )

    @property
    def microseconds(self) -> int:
        return (
            int((abs(self.ticks) % TICKS_PER_MILLISECOND) // TICKS_PER_MICROSECOND)
            * self.sign
        )

    @property
    def nanoseconds(self) -> int:
        return (
            int(abs(self.ticks) % TICKS_PER_MICROSECOND * NANOSECONDS_PER_TICK)
            * self.sign
        )

    @property
    def total_days(self) -> float:
        return self.ticks / TICKS_PER_DAY

    @property
    def total_hours(self) -> float:
        return self.ticks / TICKS_PER_HOUR

    @property
    def total_minutes(self) -> float:
        return self.ticks / TICKS_PER_MINUTE

    @property
    def total_seconds(self) -> float:
        return self.ticks / TICKS_PER_SECOND

    @property
    def total_milliseconds(self) -> float:
        return (
            MAX_MILLISECONDS
            if (ms := self.ticks / TICKS_PER_MILLISECOND) > MAX_MILLISECONDS
            else MIN_MILLISECONDS if ms < MIN_MILLISECONDS else ms
        )

    @property
    def total_microseconds(self) -> float:
        return self.ticks / TICKS_PER_MICROSECOND

    @property
    def total_nanoseconds(self) -> float:
        return float(self.ticks) * NANOSECONDS_PER_TICK

    def to_timedelta(self) -> timedelta:
        return timedelta(
            self.days,
            self.seconds,
            self.microseconds,
            self.milliseconds,
            self.minutes,
            self.hours,
        )

    def __int__(self) -> int:
        return self.ticks

    def __float__(self) -> float:
        return float(self.ticks)

    def __abs__(self) -> "timespan":
        return timespan(abs(self.ticks))

    def __hash__(self) -> int:
        return hash(self.ticks)

    def __repr__(self) -> str:
        ts = abs(self)
        ms = ts.milliseconds
        us = ts.microseconds

        frac = ""
        if ms or us:
            total_micro = ms * 1000 + us
            frac = f".{total_micro:06d}".rstrip("0")

        # hh:mm:ss[.ffffff]
        time_part = f"{ts.hours:02}:{ts.minutes:02}:{ts.seconds:02}{frac}"

        # [d.]hh:mm:ss[.ffffff]
        if ts.days != 0:
            time_part = f"{ts.days}.{time_part}"

        return ("-" if self.sign == -1 else "") + time_part

    def __format__(self, format_spec: str) -> str:
        if not format_spec:
            format_spec = "c"

        sign = "-" if self.ticks < 0 else ""
        t = abs(self.ticks)
        d = abs(self.days)
        h = abs(self.hours)
        m = abs(self.minutes)
        s = abs(self.seconds)
        _ = abs(self.microseconds)
        _ = abs(self.milliseconds)

        total_ticks = t % TICKS_PER_SECOND
        frac7 = int((total_ticks / TICKS_PER_SECOND) * 10_000_000)

        if format_spec in ("c", "t", "T"):
            # [-][d.]hh:mm:ss[.fffffff]
            frac = f"{frac7:07}".rstrip("0")
            core = f"{h:02}:{m:02}:{s:02}" + (f".{frac}" if frac else "")
            return f"{sign}{d}.{core}" if d != 0 else f"{sign}{core}"

        elif format_spec == "g":
            # [d:]hh:mm:ss[.fff]
            frac = f"{frac7:07}".rstrip("0")[:3].rstrip("0")
            core = f"{h:02}:{m:02}:{s:02}" + (f".{frac}" if frac else "")
            return f"{sign}{d}:{core}" if d != 0 else f"{sign}{core}"

        elif format_spec == "G":
            # [d:]hh:mm:ss[.fffffff]
            frac = f"{frac7:07}"
            return f"{sign}{d}:{h:02}:{m:02}:{s:02}.{frac}"

        fmt = format_spec
        fmt = fmt.replace("\\:", "\x01").replace("\\.", "\x02")

        # [Ff]
        def repl_frac(m: re.Match):
            spec = m.group(0)
            count = len(spec)
            digits = f"{frac7:07}"[:count]
            if spec[0] == "f":
                return digits.ljust(count, "0")
            else:
                return digits.rstrip("0")

        fmt = re.sub(r"[Ff]{1,7}", repl_frac, fmt)

        repls = {
            "dddddddd": f"{d:08}",
            "ddddddd": f"{d:07}",
            "dddddd": f"{d:06}",
            "ddddd": f"{d:05}",
            "dddd": f"{d:04}",
            "ddd": f"{d:03}",
            "dd": f"{d:02}",
            "d": f"{d:01}",
            "hh": f"{h:02}",
            "h": f"{h:01}",
            "mm": f"{m:02}",
            "m": f"{m:01}",
            "ss": f"{s:02}",
            "s": f"{s:01}",
        }

        for k in sorted(repls.keys(), key=len, reverse=True):
            fmt = fmt.replace(k, repls[k])

        fmt = fmt.replace("\x01", ":").replace("\x02", ".")

        return sign + fmt

    def __pos__(self) -> "timespan":
        return self

    def __neg__(self) -> "timespan":
        return timespan(-self.ticks)

    def __add__(self, ts: "timespan") -> "timespan":
        ticks = self.ticks + ts.ticks
        if ticks > MAX_TICKS or ticks < MIN_TICKS:
            raise OverflowError()
        return timespan(ticks)

    def __sub__(self, ts: "timespan") -> "timespan":
        return self + -ts

    def __mul__(self, f: float) -> "timespan":
        if math.isnan(f):
            raise ValueError()

        if (t := self.ticks * f) >= 0:
            rounded_ticks = int(t + 0.5)
        else:
            rounded_ticks = int(t - 0.5)

        return interval_from_float_ticks(rounded_ticks)

    def __rmul__(self, f: float) -> "timespan":
        return self * f

    def __truediv__(self, d: float) -> "timespan":
        if math.isnan(d):
            raise ValueError()
        if d == 0:
            raise ZeroDivisionError()
        if (t := self.ticks / d) >= 0:
            rounded_ticks = int(t + 0.5)
        else:
            rounded_ticks = int(t - 0.5)

        return interval_from_float_ticks(rounded_ticks)


MIN = timespan(MIN_TICKS)
MAX = timespan(MAX_TICKS)


def time_to_ticks(
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
    milliseconds: int = 0,
    microseconds: int = 0,
) -> int:
    total = (
        days * MICROSECONDS_PER_DAY
        + hours * MICROSECONDS_PER_HOUR
        + minutes * MICROSECONDS_PER_MINUTE
        + seconds * MICROSECONDS_PER_SECOND
        + milliseconds * MICROSECONDS_PER_MILLISECOND
        + microseconds
    )

    if MAX_MICROSECONDS < total or total < MIN_MICROSECONDS:
        raise OverflowError()
    return total * TICKS_PER_MICROSECOND


def interval_from_float_ticks(t: float) -> timespan:
    if math.isnan(t):
        raise ValueError()
    if MAX_TICKS < t or t < MIN_TICKS:
        raise OverflowError()
    return MAX if t == MAX_TICKS else timespan(int(t))


def interval(v: float, s: float) -> timespan:
    if math.isnan(v):
        raise ValueError()
    return interval_from_float_ticks(v * s)


def parse(text: str) -> timespan:
    if not isinstance(text, str):
        raise TypeError()

    if not (s := text.strip()):
        raise ValueError()

    sign = -1 if s.startswith("-") else 1
    if s[0] in "+-":
        s = s[1:].strip()

    pattern = re.compile(
        r"^"
        r"(?:(?P<d>\d+)\.)?"
        r"(?P<h>\d{1,2}):"
        r"(?P<m>\d{1,2}):"
        r"(?P<s>\d{1,2})"
        r"(?:\.(?P<f>\d{1,7}))?"
        r"$",
        re.VERBOSE,
    )

    match = pattern.match(s)
    if not match:
        raise ValueError()

    values = match.groupdict()

    d = int(values["d"] or 0)
    h = int(values["h"])
    m = int(values["m"])
    s = int(values["s"])
    frac = values["f"]

    us = 0
    if frac:
        frac = (frac + "0" * 7)[:7]
        us = int(frac[:6])
        if len(frac) > 6 and int(frac[6]) >= 5:
            us += 1
        us = min(us, 999999)

    ts = timespan((d, h, m, s, 0, us))
    return ts * sign


def try_parse(text: str) -> tuple[bool, timespan | None]:
    try:
        return True, parse(text)
    except Exception:
        return False, None


def from_ticks(ticks: int) -> timespan:
    return timespan(ticks)


def from_days(days: float) -> timespan:
    return interval(days, TICKS_PER_DAY)


def from_hours(hours: float) -> timespan:
    return interval(hours, TICKS_PER_HOUR)


def from_minutes(minutes: float) -> timespan:
    return interval(minutes, TICKS_PER_MINUTE)


def from_seconds(seconds: float) -> timespan:
    return interval(seconds, TICKS_PER_SECOND)


def from_milliseconds(milliseconds: float) -> timespan:
    return interval(milliseconds, TICKS_PER_MILLISECOND)


def from_microseconds(microseconds: float) -> timespan:
    return interval(microseconds, TICKS_PER_MICROSECOND)


def from_nanoseconds(nanoseconds: float) -> timespan:
    return interval(nanoseconds, 1 / 10)


def from_timedelta(td: timedelta) -> timespan:
    return interval(td.total_seconds(), TICKS_PER_SECOND)


if __name__ == "__main__":
    ts1 = timespan((7, 1, 23, 45, 632, 942))
    ts2 = -timespan((3, 13, 9, 52, 973, 439))
    print(ts1 * 2)
    print(ts1 / 2)
    print(ts1 + ts2)
    print(ts1 - ts2)
    print(ts2)
    print(-ts2)
    print(parse("01.12:23:34.5678901"))

    td = timedelta(
        days=4, hours=3, minutes=23, seconds=49, milliseconds=934, microseconds=32
    )
    print(from_timedelta(td))
