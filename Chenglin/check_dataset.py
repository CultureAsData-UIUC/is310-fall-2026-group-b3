import csv
from pathlib import Path

DATA_FILE = Path(__file__).with_name("guarantee_games.csv")


def is_blank(value):
    return value is None or str(value).strip() == ""


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {DATA_FILE.name}. Put this script in the same folder as the CSV."
        )

    with DATA_FILE.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Total records: {len(rows)}")

    verified_contract_amounts = sum(not is_blank(r.get("contract_amount_usd")) for r in rows)
    reported_amounts = sum(not is_blank(r.get("reported_amount_usd")) for r in rows)
    actual_payment_evidence = sum(not is_blank(r.get("actual_payment_evidence")) for r in rows)

    print(f"Records with contract amount: {verified_contract_amounts}")
    print(f"Records with reported amount: {reported_amounts}")
    print(f"Records with actual-payment evidence: {actual_payment_evidence}")

    missing_any_payment_amount = [
        r for r in rows
        if is_blank(r.get("contract_amount_usd")) and is_blank(r.get("reported_amount_usd"))
    ]
    print(f"Records with no payment amount yet: {len(missing_any_payment_amount)}")

    score_errors = []
    for r in rows:
        try:
            expected = abs(int(r["home_score"]) - int(r["away_score"]))
            recorded = int(r["score_difference"])
            if expected != recorded:
                score_errors.append((r["game_date"], r["home_team"], r["away_team"], expected, recorded))
        except (ValueError, TypeError, KeyError):
            score_errors.append((r.get("game_date"), r.get("home_team"), r.get("away_team"), "invalid", r.get("score_difference")))

    print(f"Score-difference problems: {len(score_errors)}")
    for error in score_errors:
        print("  ", error)

    invalid_levels = []
    for r in rows:
        if r.get("home_level") != "FBS" or r.get("away_level") != "FCS":
            invalid_levels.append((r.get("game_date"), r.get("home_team"), r.get("away_team")))

    print(f"Rows outside FBS-home/FCS-away scope: {len(invalid_levels)}")
    for item in invalid_levels:
        print("  ", item)

    seen = set()
    duplicates = []
    for r in rows:
        key = (r.get("game_date"), r.get("home_team"), r.get("away_team"))
        if key in seen:
            duplicates.append(key)
        seen.add(key)

    print(f"Duplicate game records: {len(duplicates)}")
    for item in duplicates:
        print("  ", item)


if __name__ == "__main__":
    main()
