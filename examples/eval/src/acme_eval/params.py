"""Checks for the parameters of the parameterised documents, and wording chosen by code.

A parameterised document is rendered many times with values it was not written for, so it
checks each value before using it:

    month = params.month(month, business["month"])  # "latest" becomes the last month

A value that is not in the data stops the render with a message that lists the values that
are, instead of rendering a document about nothing.
"""

import re

MONTH_FORMAT = re.compile(r"\d{4}-(0[1-9]|1[0-2])")
FACTORS = {"age_band": "age band", "job": "job"}  # outputs/segments.csv's factors
FEW_SUBSCRIBERS = 50  # below this many subscribers, a segment's figures carry a caveat


class ParameterError(ValueError):
    """A parameter value the document cannot report on."""


def month(value: str, months) -> str:
    """The month to report: `value` ("YYYY-MM", or "latest") checked against `months`."""
    months = sorted(str(m) for m in months)
    if value == "latest":
        return months[-1]
    if not MONTH_FORMAT.fullmatch(str(value)):
        raise ParameterError(f'month must be "YYYY-MM" or "latest", not {value!r}')
    if value not in months:
        raise ParameterError(
            f"month {value} is not in the data, which runs from {months[0]} to {months[-1]}")
    return value


def segment(factor: str, value: str, segments) -> tuple[str, str]:
    """The factor and segment to report, checked against a table with those columns."""
    if factor not in FACTORS:
        raise ParameterError(f"factor must be one of {', '.join(FACTORS)}, not {factor!r}")
    known = sorted(set(segments.loc[segments["factor"] == factor, "segment"]))
    if value not in known:
        raise ParameterError(
            f"{FACTORS[factor]} {value!r} is not in outputs/segments.csv: one of {', '.join(known)}")
    return factor, value


def direction(now: float, before: float) -> str:
    """ "up", "down" or "unchanged": the change from `before` to `now`, as printed.

    Compare the numbers as the document prints them (rounded the same way), so that the word
    and the figures beside it never disagree.
    """
    if now > before:
        return "up"
    if now < before:
        return "down"
    return "unchanged"


def relation(value: float, reference: float) -> str:
    """ "above", "below" or "level with": `value` against `reference`, as printed."""
    return {"up": "above", "down": "below", "unchanged": "level with"}[direction(value, reference)]
