# USDT — US Disease Tracker Public Data

This repository stores publicly available data published and maintained by the **US Disease Tracker (USDT)**. It serves as the canonical, open-access archive for disease reporting datasets, enabling researchers, public-health officials, and the general public to access, reproduce, and build upon USDT's efforts.

## About USDT

The US Disease Tracker is an initiative dedicated to collecting, standardizing, and disseminating disease incidence and surveillance data across the United States. By making underlying datasets publicly available, USDT promotes transparency, reproducibility, and collaborative research in public health.

## Repository Contents

Datasets will be added to this repository as they are released. Data include:

- Raw reporting data submitted by jurisdictions, combined into a single file for all geographies
- A data dictionary describing each variable
- Source and methodology notes

## Current Data

<!-- CURRENT_DATA_TABLE_START -->
8 jurisdictions currently submit data directly to USDT:

| State | Jurisdiction ID | Conditions Submitted to USDT | Jurisdiction Website |
|---|---|---|---|
| Connecticut | CT | Measles, Meningococcus, Pertussis | — |
| Idaho | ID | Measles, Meningococcus, Pertussis | — |
| Illinois | IL | Measles, Meningococcus, Pertussis | [Link](https://dph.illinois.gov/topics-services/diseases-and-conditions/infectious-diseases/infectious-diseases-dashboard.html) |
| Massachusetts | MA | Measles, Meningococcus, Pertussis | [Link](https://www.mass.gov/dph-data-library) |
| Michigan | MI | Measles, Meningococcus, Pertussis | — |
| Minnesota | MN | Measles, Meningococcus, Pertussis | — |
| Oregon | OR | Measles, Meningococcus, Pertussis | [Link](https://data.oregon.gov/browse?q=communicable+disease&sortBy=relevance&pageSize=20&page=1) |
| Tennessee | TN | Measles, Meningococcus, Pertussis | — |

**Note:** For jurisdictions not yet submitting directly to USDT (and for conditions not listed above), USDT supplements coverage using state/territory-level data from the CDC's National Notifiable Diseases Surveillance System (NNDSS). Source: [https://www.cdc.gov/nndss/](https://www.cdc.gov/nndss/)

For more info, see [`data/jurisdiction_reference_table.csv`](data/jurisdiction_reference_table.csv).
<!-- CURRENT_DATA_TABLE_END -->

*This section is auto-generated from [`data/jurisdiction_reference_table.csv`](data/jurisdiction_reference_table.csv) by [`scripts/update_readme_current_data.py`](scripts/update_readme_current_data.py), and is refreshed automatically by GitHub Actions whenever that file changes on `main`.*

## Data Usage

All data in this repository is released under the [MIT License](LICENSE) and is free for public use. When using USDT data in publications or der