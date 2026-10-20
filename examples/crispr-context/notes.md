# CRISPR-Cas9 teaching context

## Audience and question

For researchers and students learning Quarto: how do target-site indel-bearing
read fractions compare between a Cas9 example and a control? The tasks use the
same context in this order: introduction slides, a three-page essay, a research
Jupyter notebook with saved results, and a separate blog.

## Data provenance and units

All six rows in `counts.csv` are **synthetic**, invented for this workshop.
They are not observations from any cited paper. Keep the supplied CSV unchanged;
perform the slide's count-change exercise in a separate in-cell teaching list.

The revised teaching fixture uses unequal, multi-thousand read depths rather
than 100 reads per sample. Counts are illustrative, not a simulation calibrated
to a particular experiment or a claim about typical editing efficiency.

- One row represents one synthetic sample, with three samples per condition.
- `sample` is its identifier. `condition` is Control or Cas9.
- `indel_reads` counts reads with at least one insertion or deletion in a
  predefined window around the expected cut site, counting each read once even
  if it contains multiple indels. `total_reads` counts all quality-passing,
  aligned target-site reads assessed in that sample, including those without indels.
- Compute `100 * indel_reads / total_reads`, in percent, separately per sample.
  The descriptive group mean gives each sample equal weight.
- Also report each condition's sample count, median, and sample standard deviation
  of sample percentages. The SD uses denominator `sample count - 1` and units of
  percentage points. It describes the fixture's spread, not biological-effect
  uncertainty. No pooling of reads or inferential test is required.
- Reads within a sample are not independent biological replicates. No organism,
  gene, guide sequence, laboratory protocol, or experimental replicate design is
  provided. Do not infer these details or perform an efficacy significance test.

## Research notes

Cas9 can use guide RNA to direct DNA cleavage (Jinek et al., 2012). Cong et al.
(2013) demonstrated RNA-directed Cas9 cleavage at genomic loci in mammalian cells.
Use these primary studies as background, not as sources of the synthetic counts.
Clement et al. (2019) supplies a primary sequencing-analysis reference for the
counting discussion. None of the three papers supplies the teaching counts.

The assumed control has no target-directed Cas9 cleavage. Its nonzero counts
represent possible background variation or assay error, not confirmed Cas9
edits. A real assay must specify filtering and the indel-counting window; no
underlying reads or variant calls are supplied here to validate either.

An indel-bearing read fraction is a descriptive sequence readout. It does not
establish a precise intended edit, an edited-cell percentage, functional knockout,
or off-target specificity. Real interpretation needs assay definitions, controls,
and independent biological replicates. These inputs support a Quarto exercise.

## Completion checks

1. **Introduction slides:** deliver `intro.qmd` and `intro.html`, exactly six
   slides including title and references. Explain guide RNA/PAM, cleavage and
   repair, research value, and indel measurement limits for first-year students.
2. **Essay:** deliver `essay.qmd` and `essay.pdf`, exactly three pages total
   including references, with no separate cover. Explain why genomic indel
   counting and statistical summaries matter for CRISPR-Cas9. Use A4, 11-point
   text, and 1-inch margins. Page 1: repair and measurement value. Page 2:
   fractions, controls, and summaries. Page 3: replicates, uncertainty, limits,
   and references. Compute any synthetic illustration from `context/counts.csv`
   and verify page count. This task does not depend on the later notebook.
3. **Research Jupyter notebook:** deliver `notebook.qmd` and `notebook.ipynb`.
   Use `quarto convert notebook.qmd --output notebook.ipynb`, then
   `jupyter nbconvert --to notebook --execute --inplace notebook.ipynb`.
   Run from the task root with the selected Python/Jupyter environment. Restart
   the kernel and run all cells. Check saved outputs, six sample fractions,
   sample counts, mean/median/sample SD, chart labels, and readable reference links.
4. **Separate blog:** deliver editable website sources, an HTML home-page listing,
   and the rendered CRISPR-Cas9 post. Fix paths relative to
   `posts/crispr-cas9/index.qmd` and test navigation in the separate blog project.

Keep context inputs unchanged and record build commands in each workspace's
README. The worked `notebook.qmd` can also render as HTML for inspection, but
HTML alone does not satisfy Task 3. Keep all task outputs outside the workshop
site's render list. Check all three references and label synthetic data throughout.

Primary-study titles, authors, years, and DOI metadata verified 2026-10-07 against
Science (Jinek) and PubMed (Cong). Clement metadata checked 2026-10-19 against
Nature Biotechnology and PubMed (PMID 30809026). Dependencies: Python/Jupyter,
pandas, Matplotlib, nbconvert; the essay also needs a PDF engine.
Use a suitable local runtime and record its actual build invocation.
