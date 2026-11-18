# Data

Two files. `bank-full.csv` is real public data, kept byte for byte as downloaded; never edit
it. `synthetic_business.csv` is invented. Acme Signals is a fictional company.

## bank-full.csv: UCI Bank Marketing

- **What it is.** Direct-marketing phone campaigns of a Portuguese bank, May 2008 to
  November 2010, one row per client contacted. The target `y` records whether the client
  subscribed to a term deposit. The file is "ordered by date" (`bank-names.txt` in the
  download).
- **Source.** UCI Machine Learning Repository, *Bank Marketing*, dataset 222:
  <https://archive.ics.uci.edu/dataset/222/bank+marketing>.
- **Download.** <https://archive.ics.uci.edu/static/public/222/bank+marketing.zip>.
  `bank-full.csv` is inside the inner archive `bank.zip`. It is semicolon-delimited, with
  text values in double quotes.
- **Retrieved.** 2026-11-18.
- **Licence.** The dataset page states: "This dataset is licensed under a Creative Commons
  Attribution 4.0 International (CC BY 4.0) license."
  (<https://creativecommons.org/licenses/by/4.0/legalcode>, checked 2026-11-18).
- **Dataset citation**, as UCI gives it: Moro, S., Rita, P., & Cortez, P. (2014). Bank
  Marketing [Dataset]. UCI Machine Learning Repository. <https://doi.org/10.24432/C5K306>
- **Paper.** Moro, S., Cortez, P., & Rita, P. (2014). A data-driven approach to predict the
  success of bank telemarketing. *Decision Support Systems*, 62, 22–31.
  <https://doi.org/10.1016/j.dss.2014.03.001>
- **SHA-256.** `d1513ec63b385506f7cfce9f2c5caa9fe99e7ba4e8c3fa264b3aaf0f849ed32d`
  (`acme_eval.data.EXPECTED_SHA256`).
- **Size.** 45,211 rows and 17 columns: 16 inputs and the target `y`. No values are missing;
  some categories are the text `unknown`. `tests/test_data.py` checks the checksum, the row
  and column counts and the column names, so these figures fail the tests if the file changes.

### `duration` is excluded

`duration` is only known after the call has ended, by which time the outcome is known too.
The dataset page's variables table says of it: "Important note: this attribute highly
affects the output target (e.g., if duration=0 then y='no'). Yet, the duration is not known
before a call is performed. Also, after the end of the call y is obviously known. Thus, this
input should only be included for benchmark purposes and should be discarded if the
intention is to have a realistic predictive model." `acme_eval.data.load()` drops it, and
`tests/test_models.py` checks that no model version uses it.

### Data dictionary

Descriptions follow `bank-names.txt`, the description file in `bank.zip`. (The dataset page's
table lists the 17 variables from both of the dataset's files: it calls the day column
`day_of_week`, but this file's `day` is the day of the month.)

| Column | Type | Description |
|---|---|---|
| `age` | integer | Age, in years |
| `job` | text | Type of job: `admin.`, `blue-collar`, `entrepreneur`, `housemaid`, `management`, `retired`, `self-employed`, `services`, `student`, `technician`, `unemployed`, `unknown` |
| `marital` | text | Marital status: `married`, `divorced` (divorced or widowed), `single` |
| `education` | text | `primary`, `secondary`, `tertiary`, `unknown` |
| `default` | text | Has credit in default? `yes`/`no` |
| `balance` | integer | Average yearly balance, in euros |
| `housing` | text | Has a housing loan? `yes`/`no` |
| `loan` | text | Has a personal loan? `yes`/`no` |
| `contact` | text | Contact communication type: `cellular`, `telephone`, `unknown` |
| `day` | integer | Last contact day of the month |
| `month` | text | Last contact month of year: `jan` … `dec` |
| `duration` | integer | Last contact duration, in seconds. **Excluded: known only after the call** |
| `campaign` | integer | Number of contacts during this campaign for this client, including the last contact |
| `pdays` | integer | Days since the client was last contacted in a previous campaign; `-1` means not previously contacted |
| `previous` | integer | Number of contacts before this campaign for this client |
| `poutcome` | text | Outcome of the previous campaign: `unknown`, `other`, `failure`, `success` |
| `y` | text | Target: has the client subscribed to a term deposit? `yes`/`no` (coded 1/0 by `acme_eval.data.load()`) |

## synthetic_business.csv

**SYNTHETIC: INVENTED FOR TEACHING, NOT REAL COMPANY DATA.** Monthly figures for Acme
Signals, a fictional two-person company, January to October 2026, written by
`scripts/make_synthetic_business.py` with a fixed seed (`uv run python
scripts/make_synthetic_business.py` rewrites the same file). It is the only synthetic file.

| Column | Description |
|---|---|
| `month` | Calendar month, `YYYY-MM` |
| `customers` | Paying customers (banks) at the end of the month |
| `pilots` | Banks trialling the model at the end of the month |
| `monthly_recurring_revenue_gbp` | Subscription revenue for the month, in pounds |
| `calls_ranked` | Contacts the model ranked for customers and pilots that month |
