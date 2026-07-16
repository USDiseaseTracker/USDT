# Data Folder

This folder contains USDT's disease surveillance datasets and supporting reference data.

## Contents

- `USDT_disease_data.csv` — Combined disease case/death counts by jurisdiction, time period, and age group, drawn from NNDSS (national) and USDT (jurisdiction-collected) sources.
- `reference/jurisdiction_reference_table.csv` — Reference table of jurisdictions reporting to USDT, their data source, the conditions they cover, and sub-jurisdiction geography type.
- `USDT_data_dictionary.csv` — Column-level documentation for both files above (data type, allowed values, examples, missing-value notes, and how each field compares to the official USDT submission spec).
- `disease_reference.csv` — Per-disease valid options (outcome, confirmation status, valid age groups, valid subtypes, CSTE reference) for all 10 diseases tracked by USDT.

## Data Dictionary

See `USDT_data_dictionary.csv` for full details. Summary of key fields in `USDT_disease_data.csv`:

| Column | Description |
|---|---|
| mmwr_year | MMWR epidemiological year |
| mmwr_month | MMWR month (populated when time_unit = month) |
| mmwr_week | MMWR week 1-53 (populated when time_unit = week) |
| report_period_start / report_period_end | Start/end date of the reporting period |
| date_type | How the report period was assigned (`cccd`, `jurisdiction date hierarchy`, or `date of death` for pediatric influenza deaths) |
| time_unit | Temporal resolution: `week`, `month`, or `year` |
| disease_name | Disease/condition reported |
| disease_subtype | Subtype/serogroup, or `total` |
| reporting_jurisdiction | Specific reporting entity (state or sub-state unit) |
| state | Parent state/territory postal abbreviation |
| geo_unit | Geographic resolution: `state_and_territories` or `sub_state` |
| geo_name | Standardized geography code |
| age_group | Age group for the count, or `total` |
| count | Number of cases or deaths (may be negative, reflecting corrections) |
| confirmation_status | `confirmed` or `confirmed and probable` |
| outcome | `cases` |
| data_source | `USDT` or `NNDSS` (for jurisdictions not yet submitting data to USDT) |
| data_status | Review/publication status |
| current_upload_timestamp | Timestamp of most recent upload/refresh |

## Diseases Tracked

USDT currently tracks 10 diseases: measles, pertussis, invasive meningococcal disease, hepatitis A, acute hepatitis B, perinatal hepatitis B, mumps, mpox, varicella, and influenza-associated pediatric mortality (`pediatric flu mortality`). See `disease_reference.csv` for each disease's valid age groups, subtypes, confirmation status, and outcome per the official standard.

## Official Data Standard

Field definitions and valid values are governed by USDT's public data standards repository: [USDiseaseTracker/USDiseaseTracker-Docs](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs) (spec version 2.0.1, updated 2026-06-30). Key references there:

- [Data Technical Specifications](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/blob/main/guides/data-technical-specs.md) — field-by-field submission requirements
- [Validation Rules](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/blob/main/guides/validation.md) — cross-field and logical validation rules
- [Data dictionary (CSV)](https://github.com/USDiseaseTracker/USDiseaseTracker-Docs/blob/main/examples-and-templates/disease_tracking_data_dictionary.csv) — official field/value reference

## Notes

- `reporting_jurisdiction` and `geo_name` may refer to sub-state geographies (e.g. public health districts, regions, counties) depending on how each jurisdiction reports; `state` always gives the parent state/territory.
- Negative `count` values are valid and represent downward revisions to previously reported totals. The raw submission spec requires positive, non-zero counts; negatives appear only in this published/corrected dataset.
- NNDSS records are state/territory level only; USDT records include both state-level and sub-state-level data.
- This combined dataset deviates from the raw USDT jurisdiction submission spec in a few ways — see the `notes_on_deviation_from_spec` column in `USDT_data_dictionary.csv` for details. Notably: `time_unit` includes `month`/`year` (spec is weekly-only), `geo_unit` uses two broad categories instead of the spec's granular list, `pediatric flu mortality` still reports `outcome = deaths` (spec now uses `cases`), `measles` appears under both `confirmed` and `confirmed and probable` (spec requires `confirmed` only), and `disease_subtype` includes a combined `ACWY` value not in the raw spec's serogroup list.
