"""Guards for sentences whose wording depends on the results.

A document states a claim next to the check that supports it:

    claim(best == summary["best_version"], "The best version is named in summary.json.")

If the check fails, the render stops with the sentence that is no longer true.
"""


class ClaimError(AssertionError):
    """A sentence in a document is not supported by outputs/."""


def claim(condition: bool, sentence: str) -> None:
    """Stop with `sentence` if `condition` is false."""
    if not condition:
        raise ClaimError(f"The results no longer support this sentence: {sentence}")
