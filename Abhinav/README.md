# Abhinav Penaganti | IS 310 Milestone 2

This is my part of our group project, The Business of College Sports. I am looking at where Big Ten athletic departments spend their money and how those expenses show up in public financial reports.

## Files

- `athletic_spending.csv`: my initial dataset with 86 spending records from 13 current Big Ten schools.
- `check_dataset.py`: Python script I used to look for missing amounts, duplicate rows and other data problems.
- `validation_output.txt`: the results from running the script.
- `source_checks.csv`: a separate file comparing 50 dataset entries with amounts from published Knight-Newhouse tables.
- `milestone2.md`: my project description, sources, decisions, audit plan and next steps.

## Running my code

Open this folder in VS Code, open the terminal and run:

```bash
python3 check_dataset.py
```

On Windows, use `python check_dataset.py` instead.

Both CSV files need to be in the same folder as the Python file. The script prints the results and saves them in `validation_output.txt`. I only used Python's built-in libraries, so there is nothing extra to install.

## A few things about the data

My overall project looks at fiscal years 2015 to 2025. The 86 rows in this first dataset are a smaller sample from 2020 to 2025. Some rows show athletic department expense categories, while others show football spending totals or football coaching salaries. Those amounts overlap, so they should not all be added together.

I also kept NIL estimates separate. An estimated athlete value is not the same thing as money an athletic department reported spending.

The source links and my notes are included in the CSV. The 50 entries in `source_checks.csv` match the public Knight-Newhouse tables, but this does not mean I checked the original university accounting files. The other 36 entries still need their own source checks.

## Group GitHub page

This folder belongs in `is310-fall-2026-group-b3/Abhinav/`.

The group README should link to my write-up:

`[Abhinav: Big Ten athletic spending](Abhinav/milestone2.md)`
