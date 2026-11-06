#!/usr/bin/env python3
"""Collect four 2024–25 financial measures for all 18 Big Ten schools.

Run: python3 collect_big_ten.py
Reproduce the supplied data without internet: python3 collect_big_ten.py --offline
Uses only Python's standard library. See README.md for source limitations.
"""

import argparse
import csv
import html
import json
import re
import ssl
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen


YEAR = "2024-25"
KNIGHT_YEAR = "2025"
BASE = Path(__file__).resolve().parent

# School name, federal EADA institution ID, Knight-Newhouse profile path.
# These are the 18 Big Ten members in 2024–25, regardless of website grouping.
SCHOOLS = [
    ("Illinois", 145637, "big-ten/university-illinois-urbana-champaign"),
    ("Indiana", 151351, "big-ten/indiana-university-bloomington"),
    ("Iowa", 153658, "big-ten/university-iowa"),
    ("Maryland", 163286, "big-ten/university-maryland-college-park"),
    ("Michigan", 170976, "big-ten/university-michigan"),
    ("Michigan State", 171100, "big-ten/michigan-state-university"),
    ("Minnesota", 174066, "big-ten/university-minnesota-twin-cities"),
    ("Nebraska", 181464, "big-ten/university-nebraska-lincoln"),
    ("Northwestern", 147767, "big-ten/northwestern-university"),
    ("Ohio State", 204796, "big-ten/ohio-state-university"),
    ("Oregon", 209551, "big-ten/university-oregon"),
    ("Penn State", 214777, "big-ten/pennsylvania-state-university"),
    ("Purdue", 243780, "big-ten/purdue-university"),
    ("Rutgers", 186380, "big-ten/rutgers-state-university-new-jersey-new-brunswick"),
    ("UCLA", 110662, "big-ten/university-california-los-angeles"),
    ("USC", 123961, "pac-12/university-southern-california"),
    ("Washington", 236948, "big-ten/university-washington"),
    ("Wisconsin", 240444, "big-ten/university-wisconsin-madison"),
]

# The full EADA department totals include amounts not allocated to teams.
# Do not substitute "Total Expenses Men's and Women's Teams" for the grand total.
METRICS = {
    "total_athletic_revenue": (
        "Revenues & Expenses Summary", "Grand Total Revenues (Lines 12+13)",
        "bar-charts-institution-total-athletic-revenues"),
    "total_athletic_expenses": (
        "Revenues & Expenses Summary", "Grand Total Expenses (Lines 8+10)",
        "bar-charts-institution-total-athletic-expenses"),
    "football_revenue": ("Total Revenues by Team", "Football", None),
    "football_expenses": (
        "Total Expenses by Team", "Football",
        "bar-charts-institution-total-football-spending"),
}

YEAR_NOTE = (
    "The year labels differ: EADA provides a 2024-25 reporting period, while "
    "Knight-Newhouse labels the fiscal year by its ending year, 2025. "
    "Check the actual reporting period before comparing figures."
)


def plain(value):
    """Remove markup while preserving a source's words."""
    return " ".join(html.unescape(re.sub(r"<[^>]*>", " ", value or "")).split())


def dollars(value):
    """A missing value stays missing; a reported zero stays zero."""
    text = plain(value).replace("$", "").replace(",", "").strip()
    if text.startswith("(") and text.endswith(")"):
        text = "-" + text[1:-1]
    return int(text) if re.fullmatch(r"-?\d+", text) else None


def download(url, cache_file, offline):
    """Try the public page; if it fails, use an explicitly dated saved copy."""
    if not offline:
        try:
            context = ssl.create_default_context()
            # Some macOS Python installs lack the system certificate bundle.
            if Path("/etc/ssl/cert.pem").exists():
                context.load_verify_locations("/etc/ssl/cert.pem")
            request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(request, timeout=35, context=context) as response:
                body = response.read().decode("utf-8-sig")
            if cache_file.name.startswith("eada_"):
                data = json.loads(body)
                if "Header" not in data or "Groups" not in data:
                    raise ValueError("EADA response is not an institution record")
                # Save only the financial screens and essential report metadata.
                keep = ("ID", "Name", "SurveyYear", "ReportingYearStart", "ReportingYearEnd")
                data = {"Header": {k: data["Header"].get(k) for k in keep},
                        "Groups": [g for g in data["Groups"] if g["ID"] == 3]}
                body = json.dumps(data)
            elif 'data-drupal-selector-chart=' not in body:
                raise ValueError("Knight-Newhouse response contains no chart data")
            record = {"url": url, "retrieved_at": datetime.now(timezone.utc).isoformat(),
                      "retrieval_method": "direct HTTP", "body": body}
            cache_file.write_text(json.dumps(record), encoding="utf-8")
            return record, "live"
        except Exception as error:
            print(f"  Download unavailable: {type(error).__name__}; checking saved copy.")
    if cache_file.exists():
        record = json.loads(cache_file.read_text(encoding="utf-8"))
        if record["url"] != url:
            raise ValueError(f"Saved source URL does not match: {cache_file.name}")
        return record, "saved snapshot"
    return None, "unavailable"


def eada_values(record, unit_id):
    if record is None:
        return {}, {}, "download_unavailable"
    data = json.loads(record["body"])
    header = data["Header"]
    if int(header["ID"]) != unit_id:
        return {}, header, "wrong_institution"
    start, end = header["ReportingYearStart"][:10], header["ReportingYearEnd"][:10]
    if not (start.startswith("2024-") and end.startswith("2025-")):
        return {}, header, "wrong_reporting_period"
    values = {}
    for metric, (screen_name, row_name, _) in METRICS.items():
        matches = []
        for group in data["Groups"]:
            for screen in group["Screens"]:
                if screen["ScreenName"] == screen_name:
                    for row in screen["Rows"]:
                        cells = row["Cells"]
                        if any(plain(c["Html"]) == row_name for c in cells):
                            matches.append(dollars(cells[-1]["Html"]))
        if len(matches) > 1:
            raise ValueError(f"Ambiguous EADA field: {metric}")
        values[metric] = matches[0] if matches else None
    return values, header, "ok"


class ChartParser(HTMLParser):
    """Read exact chart numbers embedded in the public HTML (not rounded pie labels)."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.charts = {}
        self.title_parts = []
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.in_title = True
        if "data-drupal-selector-chart" in attrs and "data-chart" in attrs:
            self.charts[attrs["data-drupal-selector-chart"]] = json.loads(attrs["data-chart"])

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, text):
        if self.in_title:
            self.title_parts.append(text)


def knight_values(record):
    if record is None:
        return {}, "download_unavailable"
    parser = ChartParser()
    parser.feed(record["body"])
    profile_name = plain("".join(parser.title_parts).split("|")[0]).casefold()
    values = {}
    for metric, (_, _, chart_id) in METRICS.items():
        if chart_id is None:
            continue  # The profile has football spending, not a football revenue chart.
        chart = parser.charts.get(chart_id)
        if not chart:
            continue
        years = [str(y) for y in chart["xAxis"][0]["categories"]]
        if KNIGHT_YEAR not in years:
            continue  # Never substitute the newest year for the requested year.
        # Match the institution series; never use the conference or FBS median.
        series = [s for s in chart["series"] if profile_name and
                  plain(s["name"]).casefold().startswith(profile_name)]
        if len(series) != 1:
            raise ValueError("Cannot identify the institution's own chart series")
        value = series[0]["data"][years.index(KNIGHT_YEAR)]
        if isinstance(value, dict):
            value = value.get("y")
        if value is not None and not isinstance(value, (int, float)):
            raise ValueError("Unexpected Knight-Newhouse amount")
        values[metric] = value
    return values, "ok"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Use the included saved source pages")
    parser.add_argument("--output", type=Path, default=BASE / "big_ten_2024_25.csv")
    args = parser.parse_args()
    cache = BASE / "source_cache"
    cache.mkdir(exist_ok=True)
    rows = []
    for school, unit_id, profile in SCHOOLS:
        print(f"Collecting {school}...")
        eada_url = f"https://ope.ed.gov/athletics/api/institution/{unit_id}"
        knight_url = f"https://knightnewhousedata.org/fbs/{profile}"
        eada_record, eada_mode = download(eada_url, cache / f"eada_{unit_id}.json", args.offline)
        knight_record, knight_mode = download(knight_url, cache / f"knight_{unit_id}.json", args.offline)
        ev, header, es = eada_values(eada_record, unit_id)
        kv, ks = knight_values(knight_record)
        for metric, (screen, field, chart) in METRICS.items():
            e, k = ev.get(metric), kv.get(metric)
            notes = [YEAR_NOTE, "Source definitions may differ; differences do not establish an error."]
            if metric.startswith("football"):
                notes.append("Football is included within department totals; do not add them together.")
            e_status = es if es != "ok" else ("collected" if e is not None else "field_not_found")
            k_status = ks if ks != "ok" else ("collected" if k is not None else "not_shown_for_2025")
            if metric == "football_revenue" and ks == "ok":
                k_status = "not_shown_on_profile"
                notes.append("The Knight-Newhouse profile does not provide a football revenue chart.")
            if school in ("Northwestern", "USC") and k is None:
                notes.append("Private school: requested financial figures were not found on this profile.")
            if school == "USC":
                notes.append("USC was a Big Ten member in 2024-25; its source URL still contains pac-12.")
            rows.append({
                "school": school, "reporting_year": YEAR, "measure": metric,
                "eada_amount_usd": e, "knight_amount_usd": k,
                "eada_period_start": str(header.get("ReportingYearStart", ""))[:10],
                "eada_period_end": str(header.get("ReportingYearEnd", ""))[:10],
                "eada_survey_year": header.get("SurveyYear", ""), "knight_year_label": KNIGHT_YEAR,
                "eada_status": e_status, "knight_status": k_status,
                "eada_source": eada_url, "eada_field": f"{screen}: {field}",
                "knight_source": knight_url, "knight_chart": chart or "",
                "eada_retrieved_at": eada_record["retrieved_at"] if eada_record else "",
                "knight_retrieved_at": knight_record["retrieved_at"] if knight_record else "",
                "eada_retrieval": eada_mode, "knight_retrieval": knight_mode,
                "audit_notes": " ".join(notes),
            })
        time.sleep(0.15)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} records to {args.output}")
    for source in ("eada", "knight"):
        count = sum(r[f"{source}_amount_usd"] is not None for r in rows)
        print(f"{source}: {count}/{len(rows)} amounts collected. Blanks are not zeros.")


if __name__ == "__main__":
    main()
