# Synthetic paired runtime demonstration

These eight rows are invented for teaching. They are not measurements from a real
system and must never be presented as empirical performance evidence.

- Each row represents a matched baseline/candidate run on the same hypothetical workload.
- Both runtime columns are in seconds; lower is faster.
- The unit of analysis is the pair. Preserve pairing when computing differences.
- Define difference as candidate minus baseline. A negative value favors the candidate.
- One pair regresses; do not claim every run improves.
- There is no information about hardware, run order, warm-up, or sampling. Do not invent it.
- Discuss which measurements and design controls a real benchmark would need.

Use descriptive statistics and a paired plot. Any inferential interval must state
its assumptions and must not imply real-world validation of these synthetic values.
The supplied bibliography documents Quarto only; it does not support statistical
or performance claims. Verify additional methodological references before citing them.
