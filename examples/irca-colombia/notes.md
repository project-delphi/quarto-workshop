# Teaching brief: reported municipal IRCA

Question: how do reported 2024 IRCA values vary among municipalities in
Boyacá, Cundinamarca, and Santander? The audience is first-year data science
students and university lecturers. The source is INS/SIVICAP's annual municipal
and departmental table, not raw sensor or sample data.

Use the bundled CSV unchanged. Exclude `#TODOS` department aggregates for
municipality comparisons, select 2024, and show the number of municipality
records by department. Plot the distribution of overall IRCA (%) by
department, with a caption and alt text. Report medians and ranges; explain
that municipalities are not equally sized and that these summaries do not
measure how many people were exposed. Rural values marked `ND` are missing,
not zero. Describe missingness before comparing urban and rural IRCA.

Exercise: find a claim that treats these annual aggregates as predictions of
future water quality or as individual water samples. Rewrite it with the
correct unit of analysis and limits.

Completion: a rendered chart and table tied to the CSV, a clear unit of
analysis, source attribution, and an explicit limit on inference.
