# Big Ten athletic finances, 2024–25

This package contains a Python collector and a CSV that opens in Excel or Google Sheets.

## Run the script

1. Unzip the package and keep `collect_big_ten.py` beside the `source_cache` folder.
2. Open a terminal in that folder.
3. Run `python3 collect_big_ten.py` (on Windows, `py collect_big_ten.py` may work instead).
4. Open `big_ten_2024_25.csv`.

No extra Python packages or paid API keys are required. Python 3.9 or newer is recommended.

To reproduce the included CSV without internet, run:

```text
python3 collect_big_ten.py --offline
```

To choose another output filename:

```text
python3 collect_big_ten.py --output my_big_ten_data.csv
```

## What is one row?

One row is one school, one year, and one measure. The 18 Big Ten members in 2024–25 each have four rows: total athletic revenue, total athletic expenses, football revenue, and football expenses. That makes 72 records. The EADA and Knight-Newhouse amounts are kept in separate columns on the same row. Amounts are US dollars; blanks are missing, not zero.

The November 5, 2026 run collected all 72 EADA amounts and 48 Knight-Newhouse amounts. The remaining 24 Knight-Newhouse fields are blank with a status explaining their absence. The saved-copy run reproduced the same amounts and notes. Illinois figures were spot-checked against the source responses, and the output was checked for duplicate records, incorrect years, missing source references, and missing-versus-zero handling.

## Sources and important audit notes

- EADA: https://ope.ed.gov/athletics/#/institution/list
- Knight-Newhouse: https://knightnewhousedata.org/
- Knight-Newhouse definitions: https://knightnewhousedata.org/about-the-data

The script reads the public data behind EADA's institution pages and the exact numbers embedded in Knight-Newhouse's historical charts. Each record includes its source URLs, source field/chart name, collection timestamp, and retrieval method.

**Year labels:** EADA provides a 2024–25 reporting period, while Knight-Newhouse labels the fiscal year by its ending year, 2025. EADA's survey-year field can say 2024 for this period. These labels are preserved in separate columns. The script checks that the EADA period starts in 2024 and ends in 2025, and selects 2025 in Knight-Newhouse. It never substitutes another year. A Knight-Newhouse year label alone does not establish exact matching start/end dates; review the original reports when investigating differences.

**Download limits:** Knight-Newhouse rejected direct automated downloads in this environment. Its public HTML pages were retrieved using Firecrawl on November 5, 2026, and included in `source_cache`. A normal run tries direct downloads; if a request fails, it uses the dated saved copy and marks that in the CSV. Offline mode uses saved copies for both sources. Saved copies are reproducible snapshots, not a promise of fresh data on later runs. Without a saved copy, a failed request produces blanks with a status, not invented figures. You can replace a Knight cache with a newly saved public profile HTML inside the same JSON envelope, retaining the actual source URL and retrieval date.

**Source coverage:** The selected Knight-Newhouse institutional profiles provide total athletic revenue, total athletic expenses, and football spending, but no football revenue chart. Northwestern and USC's profiles do not provide the requested financial charts. Those fields remain blank. USC is included as a 2024–25 Big Ten member even though its Knight-Newhouse profile URL still contains `pac-12`.

**Comparability:** These sources use different reporting systems and definitions. A difference does not prove an error. Department totals use EADA's grand totals, including amounts not allocated by sex/sport. Football amounts are components of department figures; do not add them to department totals. The file deliberately does not label a revenue-minus-expense result as profit or claim the sources have been reconciled.

**Your assignment:** This is a collected starting dataset. Read the records and source definitions, investigate differences, and add your own audit observations. The automated audit notes describe known source limitations; they do not replace your close review.
