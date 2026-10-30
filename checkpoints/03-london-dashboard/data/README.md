# London data

Real, published visit counts from the Association of Leading Visitor
Attractions (ALVA). Every row carries its `source`, `url` and `retrieved` date.
Retrieved 2026-10-30. Visits are counts reported by each attraction to ALVA;
one row is one attraction (and, in `visits.csv`, one year).

## attractions.csv

The ten London attractions with the most visits in ALVA's
"Visits made in 2025 to visitor attractions in membership with ALVA"
(<https://www.alva.org.uk/details.cfm?p=423>; the archive copy at `p=620` is
identical). Only ALVA members are listed, so this is not every London sight.

| Column | Meaning |
|---|---|
| `rank_uk` | ALVA rank among all UK members in 2025 |
| `attraction` | site name as ALVA publishes it |
| `area` | ALVA region (all `London`) |
| `visits_2025` | total visits in 2025 |
| `charge_code` | ALVA 2025 admissions code |
| `admission` | the code's label: 1 Paid (all pay), 2 Free, 3 Free (pay parking), 4 Free (paid exhibitions), 5 Other |
| `note` | ALVA notes that change how to read the count |

## visits.csv

Long format: one row per attraction per year, 2015–2025, for the British
Museum, Natural History Museum (South Kensington), Tate Modern, Tower of London
and National Gallery. ALVA pages: `details.cfm?p=` 606 (2015), 607, 608, 609,
610 (2019), 615 (2020), 616, 617, 618, 619 (2024), 423 (2025).

- `alva_name` keeps the name as published that year (for example
  "NHM (South Kensington)" in 2017–2019, "National Gallery, The" in 2019).
- 2020–2021 are COVID-19 pandemic years; they are not comparable with other years.
- From 2024 the Natural History Museum count includes visitors to its reopened
  gardens (ALVA 2024 note v), so 2024–2025 are not like-for-like with earlier years.
