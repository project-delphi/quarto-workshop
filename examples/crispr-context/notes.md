# CRISPR-Cas9 teaching context

## Audience and question

For researchers and students learning Quarto: how do target-site indel-bearing
read fractions compare between a Cas9 example and a control? The deliverable is
an executable research notebook with code, interpretation notes, and references.

## Data provenance and units

All six rows in `counts.csv` are **synthetic**, invented for this workshop.
They are not observations from either cited paper. Keep the supplied CSV unchanged;
perform the slide's count-change exercise in a separate in-cell teaching list.

- One row represents one synthetic sample, with three samples per condition.
- `sample` is its identifier. `condition` is Control or Cas9.
- `indel_reads` counts target-site reads classified as containing an insertion
  or deletion. `total_reads` counts all target-site reads in that sample.
- Compute `100 * indel_reads / total_reads`, in percent, separately per sample.
  The descriptive group mean gives each sample equal weight.
- Reads within a sample are not independent biological replicates. No organism,
  gene, guide sequence, laboratory protocol, or experimental replicate design is
  provided. Do not infer these details or perform an efficacy significance test.

## Research notes

Cas9 can use guide RNA to direct DNA cleavage (Jinek et al., 2012). Cong et al.
(2013) demonstrated RNA-directed Cas9 cleavage at genomic loci in mammalian cells.
Use these primary studies as background, not as sources of the synthetic counts.

An indel-bearing read fraction is a descriptive sequence readout. It does not
establish a precise intended edit, an edited-cell percentage, functional knockout,
or off-target specificity. Real interpretation needs assay definitions, controls,
and independent biological replicates. These inputs support a Quarto exercise.

## Completion checks

Render `notebook.qmd` as HTML in a working copy of this directory. Confirm that all
six sample fractions appear, the figure uses a 0–100 percent axis, and the
computed means match the CSV. Check that both citations resolve and the notes
identify synthetic data and the denominator. For a blog adaptation, fix paths
relative to `posts/crispr-cas9/index.qmd`.

Primary-study titles, authors, years, and DOI metadata verified 2026-10-07 against
Science (Jinek) and PubMed (Cong). Dependencies: Python/Jupyter, pandas, Matplotlib.
Use a suitable local runtime and record its actual build invocation.
