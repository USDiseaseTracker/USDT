# Data Folder

This folder contains USDT's disease surveillance datasets and supporting reference data.

## Contents

- `USDT_NNDSS_data.csv` — Combined disease case/death counts by jurisdiction, time period, and age group, drawn from NNDSS (national) and USDT (jurisdiction-collected) sources. 20,714 records, 20 columns.
- `reference/jurisdiction_reference_table.csv` — Reference table of jurisdictions reporting to USDT, their data source, the conditions they cover, and sub-jurisdiction geography type.
- `data_dictionary.csv` — Column-level documentation for both files above (data type, allowed values, examples, and missing-value notes).

## Data Dictionary

See `data_dictionary.csv` for full details. Summary of key fields in `USDT_NNDSS_data.csv`:

| Column | Description |
|---|---|
| mmwr_year | MMWR epidemiological year |
| mmwr_month | MMWR month (populated when time_unit = month) |
| mmwr_week | MMWR week 1-53 (populated when time_unit = week) |
| report_period_start / report_period_end | Start/end date of the reporting period |
| date_type | How the report period was assigned (`cccd` or `jurisdiction date hierarchy`) |
| time_unit | Temporal resolution: `month`, `week`, or `year` |
| disease_name | Disease/condition reported |
| disease_subtype | Subtype/serogroup, or `total` |
| reporting_jurisdiction | Specific reporting entity (state or sub-state unit) |
| state | Parent state/territory postal abbreviation |
| geo_unit | Geographic resolution: `state_and_territories` or `sub_state` |
| geo_name | Standardized geography code |
| age_group | Age group for the count, or `total` |
| count | Number of cases or deaths (may be negative, reflecting corrections) |
| confirmation_status | `confirmed` or `confirmed and probable` |
| outcome | `cases` or `deaths` |
| data_source | `NNDSS` or `USDT` |
| data_status | Review/publication status |
| current_upload_timestamp | Timestamp of most recent upload/refresh |

Key fields in `reference/jurisdiction_reference_table.csv`: `jurisdiction_name`, `jurisdiction_id`, `data_source`, `conditions_included`, `subjurisdiction_type`, `website_dashboard_link`.

## Notes

- `reporting_jurisdiction` and `geo_name` may refer to sub-state geographies (e.g. public health districts, regions, counties) depending on how each jurisdiction reports; `state` always gives the parent state/territory.
- Negative `count` values are valid and represent downward revisions to previously reported totals.
- NNDSS records are state/territory level only; USDT records include both state-level and sub-state-level data.
