# London data

Real, published visit counts from the Association of Leading Visitor
Attractions (ALVA), the five sights' visitor facts, Visit London's churches,
their map coordinates and the London borough boundaries. Every CSV row carries
its `source`, `url` and `retrieved` date. Visits are counts reported by each
attraction to ALVA; one row is one attraction (and, in `visits.csv`, one year).

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

## churches.csv

The ten cathedrals and churches on Visit London's "Cathedrals and churches in
London" page (<https://www.visitlondon.com/things-to-do/sightseeing/london-attraction/historic/cathedrals-and-churches-in-london>),
in page order, retrieved 2026-10-31. Visit London is the city's official visitor
guide; the list is its editorial choice of places tourists like, not a ranking.
It holds no visitor numbers.

| Column | Meaning |
|---|---|
| `church` | name as Visit London heads it |
| `type` | Visit London's heading: Cathedral, Gothic church or Church |
| `visit_london` | the church's Visit London page where the list links one; otherwise the list itself |

## sights.csv

The facts behind the guide's "Sights at a glance" table, the partner brief and
the flyer, for the five sights in `visits.csv`. Long format: one row per sight
and fact, each with its own source.

| `fact` | `value` | Source |
|---|---|---|
| `price_band` | `Free` (free general admission; special exhibitions may charge) or `Paid` | ALVA 2025 admissions code, as in `attractions.csv` (`p=423`, retrieved 2026-10-30) |
| `nearest_tube` | the Underground station the sight's own visitor page names as nearest, or the closest it lists | each sight's visitor or getting-here page; the National Gallery names none, so TfL's StopPoint search around the Gallery's own map point gives it |
| `official_page` | the sight's official visitor page, for "Read more" links | that page |

The visitor pages were checked on 2026-11-01. The British Museum's and Historic
Royal Palaces' sites answer scripts (such as `curl`) with `403 Forbidden`, so an
automated link check can report them as broken: open them in a browser.

## places.csv

Map coordinates (WGS84 latitude and longitude, 5 decimals) of the five sights and
the ten churches in `churches.csv`, from each place's Wikidata item (coordinate
location, P625; Wikidata is CC0), retrieved 2026-11-01. `kind` is `sight` or
`church`; `place` uses the names in `sights.csv` and `churches.csv`. Where a
sight's own page publishes coordinates they agree to within about 10 m (British
Museum, National Gallery).

## london-boroughs.geojson

The 33 London local authority districts (32 boroughs and the City of London),
`LAD24CD` codes `E09000001`–`E09000033`, from ONS, *Local Authority Districts
(December 2024) Boundaries UK BGC* (generalised to 20 m, clipped to the coastline
at Mean High Water, so the tidal Thames is a gap between boroughs), unchanged from
the ONS Open Geography Portal feature service query
<https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Local_Authority_Districts_December_2024_Boundaries_UK_BGC/FeatureServer/0/query?where=LAD24CD%20LIKE%20%27E09%25%27&outFields=LAD24CD,LAD24NM&outSR=4326&f=geojson>,
retrieved 2026-11-01 (SHA-256 `6abd0326…ca31f20`). Licence
(<https://www.ons.gov.uk/methodology/geography/licences>, checked 2026-11-01):
Source: Office for National Statistics licensed under the Open Government Licence
v.3.0. Contains OS data © Crown copyright and database right 2024.
