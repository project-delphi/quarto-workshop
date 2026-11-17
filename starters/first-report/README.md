# A first report

The starter project for the chapter "A First Report, by Hand" of the book
*Prompt, Check, Publish* ("Un primer informe, a mano" in *Pide, revisa, publica*). Copy this folder out of the repository before you use it:

```bash
cp -R ~/quarto-workshop/starters/first-report ~/first-report
cd ~/first-report
uv run quarto render report.qmd
```

`report.qmd` reads `data/visits.csv` and renders `report.html`. One of its numbers is wrong
on purpose: the chapter asks you to find it by checking the report against the data.

`data/visits.csv` holds five rows of ALVA's published 2025 visit counts (real, cited data:
each row has its `source`, `url` and `retrieved` date), taken unchanged from
`examples/london/data/attractions.csv`. ALVA counts only its member attractions.
