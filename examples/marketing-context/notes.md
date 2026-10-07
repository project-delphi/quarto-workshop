# Hillstrom email promotion experiment

## Source and provenance

Kevin Hillstrom published the MineThatData E-Mail Analytics And Data Mining Challenge
on March 20, 2008:
https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html

Original CSV URL (the publisher's HTTP download worked; HTTPS certificate validation
failed on the download host):
http://www.minethatdata.com/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv

Retrieved 2026-10-06 using:

```bash
curl -fsSL http://www.minethatdata.com/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv -o hillstrom.csv
```

The local file preserves the original bytes, header, row order, and values:

- 3,964,977 bytes; 64,000 customer rows and 12 columns.
- SHA-256: `0e5893329d8b93cefecc571777672028290ab69865718020c78c7284f291aece`.
- These are the published experiment's customer outcomes, not synthetic teaching rows.
- The retailer is unnamed. Do not invent a company, customer demographics, or email content.
- The campaign decision brief is a classroom scenario built around the published experiment.

## Experiment

The publisher describes customers who had purchased within the preceding twelve
months, randomly assigned approximately one third each to men's merchandise email,
women's merchandise email, or no email. Outcomes cover the two weeks following the
campaign. Assignment is at the customer level, with one assignment and one row per
customer. The arms are independent, not paired. The source does not specify a
percentage discount, coupon, assignment algorithm, email delivery/open status,
campaign costs, gross margin, or later outcomes.

## Data dictionary

| Column | Meaning | Timing / units |
|---|---|---|
| `recency` | Months since last purchase | Before assignment; months |
| `history_segment` | Band of past-year spending | Before assignment; category |
| `history` | Actual spending in the past year | Before assignment; dollars |
| `mens` | Bought men's merchandise in the past year | Before assignment; 0/1 |
| `womens` | Bought women's merchandise in the past year | Before assignment; 0/1 |
| `zip_code` | Urban, suburban, or rural category | Before assignment; raw spelling includes `Surburban` |
| `newbie` | New customer within the past twelve months | Before assignment; 0/1 |
| `channel` | Past-year purchase channel | Before assignment; category |
| `segment` | `Mens E-Mail`, `Womens E-Mail`, or `No E-Mail` | Randomized assignment |
| `visit` | Website visit during follow-up | After assignment; 0/1 |
| `conversion` | Any merchandise purchase during follow-up | After assignment; 0/1 |
| `spend` | Customer spending during follow-up | After assignment; dollars over two weeks |

The publisher specifies dollars without a separate currency code. Retain that unit.
Merchandise labels do not encode customer gender. There is no customer identifier;
do not drop identical attribute profiles as duplicates or invent observed IDs.
If adding a row index for analysis, label it as a locally created index.

## Analysis contract

- Preserve the raw CSV. Perform transformations in executable code.
- Use all assigned customers, including zero spend, in each arm's denominator.
- Primary outcome: two-week mean sales per assigned customer in dollars.
- Primary contrasts: each email arm's mean minus the no-email mean.
- Secondary outcomes: purchase conversion and website visit rates; report absolute
  differences in percentage points separately from relative percentage change.
- Random assignment supports intention-to-treat contrasts under valid implementation
  and no interference. Do not condition causal comparisons on visits or purchases.
- Report uncertainty with a verified methods reference and stated assumptions.
  For resampling, draw independent customer rows separately within each arm, retain
  the control comparison, and state method, seed, and repetitions.
- Check skew and zero spending. Directly compare the email arms before asserting
  superiority. Do not interpret a larger point estimate alone as a proven winner.
- Treat customer subgroup analyses as exploratory unless a plan and independent
  validation are supplied. High purchase propensity alone is not incremental uplift.
- Sales effects are not profit. Future projections need explicit audience and
  transport assumptions. Cost and margin scenarios must be labeled assumptions.
- The observation window cannot establish long-term demand, repeat sales, or retention.

The bibliography supports the experiment description and Quarto authoring. It does
not by itself supply an inferential method. Verify a primary methods reference if
adding confidence intervals or a targeting model.
