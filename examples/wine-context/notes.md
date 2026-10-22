# Wine recognition teaching context

## Audience and question

For students new to Quarto: can measured wine chemistry help distinguish three
anonymous cultivars? Use the same real dataset for introduction slides, a
three-page essay, an executable Jupyter notebook, and a separate blog.

## Provenance and interpretation

`wine.csv` is a local, unchanged-feature copy of the [UCI Wine recognition
dataset](https://archive.ics.uci.edu/dataset/109/wine), exported from
scikit-learn 1.6.1 `load_wine(as_frame=True)` on 2026-10-21. The export adds
`sample_id` and changes scikit-learn's zero-based target to UCI cultivar labels
1–3. The 178 rows and 13 measured features retain their source order and values.
The UCI page licenses the dataset CC BY 4.0. Keep this CSV unchanged in each
student workspace.

- One row is one wine sample, not a person, tasting score, or independent
  vineyard replicate. `cultivar` is an anonymized class label (1, 2, or 3),
  not a quality ranking or a grape name.
- There are 59, 71, and 48 samples in cultivars 1, 2, and 3. The 13 features
  include alcohol, malic acid, flavanoids, color intensity, and proline.
- Compare **descriptive** counts, means, medians, and sample standard deviations
  for alcohol and color intensity. The unit of analysis is a wine sample.
  UCI does not state units for either feature. Call them dataset
  measurements without inventing physical units.
- A scatterplot shows overlap and variation that group means hide. An association
  within this curated dataset is neither a blind-tasting result nor a guarantee
  that a model will generalize to new regions, vintages, or laboratories.
- Do not interpret the numbered cultivars as ordered quality classes. If a
  learner adds prediction, split data before fitting preprocessing, report a
  held-out result, and explain that this small curated sample limits inference.

## Completion checks

1. **Introduction slides:** `intro.qmd` and exactly six slides in `intro.html`,
   including title and sources. Explain the classification question, sample,
   measurements, and what the anonymous labels do and do not mean.
2. **Essay:** `essay.qmd` and exactly three pages in `essay.pdf`, including
   references, with no separate cover. Use A4, 11-point text, and 1-inch margins.
   Page 1 introduces the question and provenance; page 2 explains two chemical
   measurements and descriptive summaries; page 3 discusses overlap, limits,
   and sources. Trace every numerical claim to the CSV.
3. **Notebook:** adapt `notebook.qmd`, convert it with `quarto convert`, execute
   with `jupyter nbconvert --to notebook --execute --inplace`, and verify the
   saved table and chart from a fresh kernel. Keep readable source links.
4. **Blog:** publish a separate post at `posts/wine-chemistry/index.qmd`, with a
   home-page listing, executable chart, caption, alt text, provenance, and limits.

Keep editable sources, the CSV, and working build commands. The context bundle
is outside this workshop site's render list. The UCI dataset and scikit-learn
documentation were checked 2026-10-21.
