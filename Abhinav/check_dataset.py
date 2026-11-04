"""A few checks for my Big Ten athletic spending dataset.
Run this file in the same folder as the two CSV files.
"""

import csv
from pathlib import Path

FOLDER = Path(__file__).parent
DATA_FILE = FOLDER / "athletic_spending.csv"
CHECKS_FILE = FOLDER / "source_checks.csv"
OUTPUT_FILE = FOLDER / "validation_output.txt"


def read_csv(file):
    if not file.exists():
        raise FileNotFoundError(f"Missing {file.name}. Put it next to check_dataset.py.")
    with file.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def blank(value):
    return value is None or str(value).strip() == ""


def main():
    rows = read_csv(DATA_FILE)
    source_checks = read_csv(CHECKS_FILE)
    output = []

    def report(message):
        print(message)
        output.append(message)

    report(f"Total records: {len(rows)}")
    schools = {r["institution"] for r in rows}
    years = sorted({int(r["fiscal_year"]) for r in rows})
    report(f"Big Ten schools in this sample: {len(schools)}")
    report(f"Years in this sample: {years[0]}-{years[-1]}")
    report("Full project period: 2015-2025")

    categories = [r["source_category"] for r in rows]
    football_total = categories.count("Total Football Spending")
    coaching = categories.count("Total Football Coaching Salaries")
    report(f"Athletic department expense records: {len(rows) - football_total - coaching}")
    report(f"Football spending total records: {football_total}")
    report(f"Football coaching pay records: {coaching}")

    amounts = [r for r in rows if not blank(r["amount_usd"])]
    missing = [r["record_id"] for r in rows if blank(r["amount_usd"])]
    report(f"Records with a dollar amount: {len(amounts)}")
    report(f"Records missing a dollar amount: {len(missing)}")
    report(f"Missing amount IDs: {', '.join(missing) if missing else 'none'}")
    report(f"Records with a source link: {sum(not blank(r['source_url']) for r in rows)}")
    report(f"Records with a limitation note: {sum(not blank(r['interpretive_limit']) for r in rows)}")

    seen = set()
    duplicates = []
    problems = []
    for r in rows:
        record = r["record_id"]
        key = (r["institution"], r["fiscal_year"], r["source_category"])
        if key in seen:
            duplicates.append(record)
        seen.add(key)

        if not 2015 <= int(r["fiscal_year"]) <= 2025:
            problems.append(f"{record}: year outside my project range")
        if blank(r["institution"]) or blank(r["source_category"]):
            problems.append(f"{record}: missing school or category")
        if not r["source_url"].startswith(("https://", "http://")):
            problems.append(f"{record}: missing or invalid source link")
        if blank(r["interpretive_limit"]):
            problems.append(f"{record}: no limitation note")

        amount = r["amount_usd"]
        if blank(amount):
            if r["source_value_status"] != "source_displays_N/A":
                problems.append(f"{record}: blank amount needs an explanation")
        else:
            try:
                if int(amount) < 0:
                    problems.append(f"{record}: negative amount")
            except ValueError:
                problems.append(f"{record}: amount is not a whole number")

        pct = r["reported_share_pct"]
        if not blank(pct):
            try:
                if not 0 <= float(pct) <= 100:
                    problems.append(f"{record}: percentage outside 0-100")
            except ValueError:
                problems.append(f"{record}: invalid percentage")

    report(f"Duplicate school/year/category records: {len(duplicates)}")
    report(f"Other data problems: {len(problems)}")

    # Match the recorded amounts to the values in my public-table check file.
    by_id = {r["record_id"]: r for r in rows}
    differences = []
    for check in source_checks:
        record = by_id.get(check["record_id"])
        if record is None:
            differences.append(f"{check['record_id']}: not found in main CSV")
            continue
        published = check["published_amount_usd"]
        if published == "N/A":
            published = ""
        if record["amount_usd"] != published:
            differences.append(f"{check['record_id']}: amount does not match")
        published_pct = check["published_share_pct"]
        if not blank(published_pct) and record["reported_share_pct"] != published_pct:
            differences.append(f"{check['record_id']}: percentage does not match")

    report(f"Rows compared in source_checks.csv: {len(source_checks)}")
    report(f"Rows still needing an individual source check: {len(rows) - len(source_checks)}")
    report(f"Differences in source checks: {len(differences)}")

    for school in ("University of Illinois Urbana-Champaign", "Purdue University"):
        expense_rows = [r for r in rows if r["institution"] == school
                        and r["fiscal_year"] == "2024"
                        and r["unit_of_analysis"] == "One school, one year, one department expense category"]
        total_pct = sum(float(r["reported_share_pct"]) for r in expense_rows)
        report(f"{school}: {len(expense_rows)} FY2024 categories, {total_pct:.2f}% total share")

    for problem in duplicates + problems + differences:
        report("CHECK: " + problem)

    report("")
    report("These checks look for CSV errors and compare recorded numbers with public tables.")
    report("They do not prove the university's original financial reports are correct.")
    report("Football totals overlap other spending categories, and NIL estimates are different from expenses.")
    OUTPUT_FILE.write_text("\n".join(output) + "\n", encoding="utf-8")
    print("\nSaved results in validation_output.txt")


if __name__ == "__main__":
    main()
