# Brayden — Big Ten Athletic Revenue and Financial Reporting

This folder contains my local Milestone 2 draft for **The Business of College Sports**. It examines how money coming into Big Ten athletic programs is represented by different reporting systems. Nothing in this folder has been uploaded to the group repository.

## Files

- [`big_ten_2024_25.csv`](big_ten_2024_25.csv): supplied initial dataset, preserved unchanged; 72 school/measure records for 18 schools.
- [`milestone2.md`](milestone2.md): project overview, scope, sources, interpretive decisions, completed checks, audit plan, and next steps.
- [`check_dataset.py`](check_dataset.py): offline checks against the supplied saved responses.
- [`validation_output.txt`](validation_output.txt): results of those checks and their limitations.
- [`source_checks.csv`](source_checks.csv): 144 comparisons, including missing-value comparisons, between the dataset and saved responses.
- [`audit_annotations.json`](audit_annotations.json): 72 AI-assisted comparison notes, including school caveats, for me to review.
- [`collect_big_ten.py`](collect_big_ten.py): supplied collector; no extra packages required.
- `source_cache/`: supplied dated source responses used to reproduce the data.
- `original_files/`: the original collector README, alternate Desktop script, and separate raw EADA cache. These are supporting files, not additional observations.
- [`ai-chat-log.md`](ai-chat-log.md): summary of AI assistance and review limits.

## Run the checks

From this folder, run:

```bash
python3 check_dataset.py
```

On Windows, `python check_dataset.py` may be used instead. Python 3.9 or newer is recommended. Only built-in Python libraries are needed. Running the checks regenerates the validation output, source-check table, and draft audit annotations.

To reproduce the dataset offline without replacing the original:

```bash
python3 collect_big_ten.py --offline --output reproduced_big_ten_2024_25.csv
```

The reproduced amounts match the supplied CSV. Retrieval labels change because an offline run reads saved snapshots rather than performing the original live retrieval.

## Important limits

My primary focus is revenue. Expense fields remain in the supplied dataset as context, not a separate spending project. Football amounts are components of department activity; do not add them to department totals. Revenue minus expenses is not automatically profit.

A matching cached response does not independently verify the underlying university filing. The audit annotations are AI-assisted drafts, not evidence that I manually reviewed every record. My next step is to review the interpretations and check selected original reports. This submission uses only EADA and Knight-Newhouse; no other financial dataset is included.
