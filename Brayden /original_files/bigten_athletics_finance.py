#!/usr/bin/env python3
"""
Big Ten athletic finances, 2024-25: EADA and Knight-Newhouse side by side.

WHAT THIS SCRIPT DOES
    Collects four measures for each of the 18 Big Ten schools:
        1. Total athletic revenue      3. Football revenue
        2. Total athletic expenses     4. Football expenses
    and writes one CSV with 72 rows (18 schools x 4 measures). The amounts from
    the two sources stay in separate columns. They are never blended.

TWO WAYS TO RUN IT (Python 3.9 or newer, nothing to install)
    Download fresh copies from the two websites:
        python3 bigten_athletics_finance.py

    Read copies you saved earlier (use this if the websites block the script):
        python3 bigten_athletics_finance.py --saved-dir saved_sources/2026-11-05

    The folder name must be the date the copies were saved. That date becomes
    the collection date in the CSV.

THE RULES THIS SCRIPT FOLLOWS
    * Only 2024-25 is accepted. EADA records must run from 2024 into 2025, and
      Knight-Newhouse values must sit under the year label "2025". Any other
      year leaves the cell blank. There is no fallback to another year.
    * Totals are whole-department grand totals, never team subtotals.
    * Conference and subdivision medians on Knight-Newhouse pages are ignored.
    * A reported $0 stays 0. A missing figure stays blank, and the status and
      audit_notes columns say why.
    * No number is estimated, calculated or typed in by this script.
"""

import argparse
import csv
import datetime
import json
import re
import sys
import urllib.error
import urllib.request
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

# ---------------------------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------------------------

# The two labels the sources use for the same year. See PERIOD_NOTE below.
EADA_START_YEAR = 2024
EADA_END_YEAR = 2025
KNIGHT_YEAR_LABEL = "2025"

EADA_API = "https://ope.ed.gov/athletics/api/institution/{unitid}"
EADA_HOME = "https://ope.ed.gov/athletics/#/institution/list"
KNIGHT_PAGE = "https://knightnewhousedata.org/fbs/big-ten/{slug}"
KNIGHT_DEFINITIONS = "https://knightnewhousedata.org/about-the-data"

OUTPUT_CSV = "bigten_athletics_finance_2024_25.csv"

# unitid = the federal ID that EADA uses for a school.
# knight_slug = the end of the school's Knight-Newhouse web address.
# knight_name = how Knight-Newhouse names the school in its charts.
SCHOOLS = [
    {"school": "Illinois", "unitid": 145637, "knight_slug": "university-illinois-urbana-champaign", "knight_name": "University of Illinois Urbana-Champaign"},
    {"school": "Indiana", "unitid": 151351, "knight_slug": "indiana-university-bloomington", "knight_name": "Indiana University, Bloomington"},
    {"school": "Iowa", "unitid": 153658, "knight_slug": "university-iowa", "knight_name": "University of Iowa"},
    {"school": "Maryland", "unitid": 163286, "knight_slug": "university-maryland-college-park", "knight_name": "University of Maryland, College Park"},
    {"school": "Michigan", "unitid": 170976, "knight_slug": "university-michigan", "knight_name": "University of Michigan"},
    {"school": "Michigan State", "unitid": 171100, "knight_slug": "michigan-state-university", "knight_name": "Michigan State University"},
    {"school": "Minnesota", "unitid": 174066, "knight_slug": "university-minnesota-twin-cities", "knight_name": "University of Minnesota, Twin Cities"},
    {"school": "Nebraska", "unitid": 181464, "knight_slug": "university-nebraska-lincoln", "knight_name": "University of Nebraska-Lincoln"},
    {"school": "Northwestern", "unitid": 147767, "knight_slug": "northwestern-university", "knight_name": "Northwestern University"},
    {"school": "Ohio State", "unitid": 204796, "knight_slug": "ohio-state-university", "knight_name": "The Ohio State University"},
    {"school": "Oregon", "unitid": 209551, "knight_slug": "university-oregon", "knight_name": "University of Oregon"},
    {"school": "Penn State", "unitid": 214777, "knight_slug": "pennsylvania-state-university", "knight_name": "Pennsylvania State University"},
    {"school": "Purdue", "unitid": 243780, "knight_slug": "purdue-university", "knight_name": "Purdue University"},
    {"school": "Rutgers", "unitid": 186380, "knight_slug": "rutgers-state-university-new-jersey-new-brunswick", "knight_name": "Rutgers, The State University of New Jersey-New Brunswick"},
    {"school": "UCLA", "unitid": 110662, "knight_slug": "university-california-los-angeles", "knight_name": "University of California, Los Angeles"},
    {"school": "USC", "unitid": 123961, "knight_slug": "university-southern-california", "knight_name": "University of Southern California"},
    {"school": "Washington", "unitid": 236948, "knight_slug": "university-washington", "knight_name": "University of Washington"},
    {"school": "Wisconsin", "unitid": 240444, "knight_slug": "university-wisconsin-madison", "knight_name": "University of Wisconsin-Madison"},
]

# measure -> (where it is in EADA, which Knight-Newhouse chart holds it).
# Knight-Newhouse has no football revenue measure, so that chart is None.
MEASURES = {
    "Total athletic revenue": {
        "eada_field": "Revenues & Expenses Summary, line 14: Grand Total Revenues",
        "knight_chart": "bar-charts-institution-total-athletic-revenues",
        "knight_field": "Total Athletic Revenues",
    },
    "Total athletic expenses": {
        "eada_field": "Revenues & Expenses Summary, line 11: Grand Total Expenses",
        "knight_chart": "bar-charts-institution-total-athletic-expenses",
        "knight_field": "Total Athletic Expenses",
    },
    "Football revenue": {
        "eada_field": "Total Revenues by Team: Football row, Total column",
        "knight_chart": None,
        "knight_field": "",
    },
    "Football expenses": {
        "eada_field": "Total Expenses by Team: Football row, Total column",
        "knight_chart": "bar-charts-institution-total-football-spending",
        "knight_field": "Total Football Spending",
    },
}

PERIOD_NOTE = (
    "Period labels: EADA labels this survey year {eada_label} and its dates run "
    "{start} to {end}; Knight-Newhouse labels the same fiscal year 2025 because "
    "its year label is the year the fiscal year ends. These are the same year, "
    "not a mismatch. EADA's download page separately lists this data as "
    "'academic year 2024-25'."
)
KNIGHT_DATES_NOTE = (
    "Knight-Newhouse gives a year label, not school-specific start and end dates."
)
DEFINITION_NOTE = {
    "Total athletic revenue": (
        "Definitions differ: EADA is the Equity in Athletics grand total. "
        "Knight-Newhouse uses NCAA financial reports and subtracts 'Less Transfers "
        "to the Institution'. Expect the two amounts to differ."
    ),
    "Total athletic expenses": (
        "Definitions differ: EADA is the Equity in Athletics grand total. "
        "Knight-Newhouse uses NCAA financial reports and adds 'Excess Transfers to "
        "the Institution'. Expect the two amounts to differ."
    ),
    "Football revenue": "EADA team-level football figure.",
    "Football expenses": (
        "EADA is total football expenses by team, not the smaller 'operating "
        "(game-day) expenses' figure. Knight-Newhouse is NCAA line 42, football "
        "operating expenses including student aid."
    ),
}
KNIGHT_NO_FOOTBALL_REVENUE = (
    "Knight-Newhouse does not publish football revenue. Its football measures are "
    "spending, coaching salaries and coaching severance. Blank on purpose; no "
    "substitute used."
)


# ---------------------------------------------------------------------------
# GETTING THE SOURCE FILES
# ---------------------------------------------------------------------------

def download(url):
    """Download one web address. Returns (text, None) or (None, why it failed)."""
    request = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (BigTenFinanceStudy; Python)"}
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            return response.read().decode("utf-8", errors="replace"), None
    except urllib.error.HTTPError as error:
        return None, f"the site answered HTTP {error.code}"
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        return None, f"could not connect ({getattr(error, 'reason', error)})"


def get_source(kind, school, saved_dir, new_copy_dir):
    """
    Return (text, problem_status, problem_reason) for one school and one source.

    kind is "eada" or "knight". With --saved-dir we only read the saved file.
    Otherwise we download and keep a copy, so every run leaves a dated record.
    """
    if kind == "eada":
        url = EADA_API.format(unitid=school["unitid"])
        relative_path = Path("eada") / f"{school['unitid']}.json"
    else:
        url = KNIGHT_PAGE.format(slug=school["knight_slug"])
        relative_path = Path("knight_newhouse") / f"{school['knight_slug']}.html"

    if saved_dir:
        path = saved_dir / relative_path
        if not path.exists():
            return None, "saved_copy_missing", f"No saved copy at {path}."
        return path.read_text(encoding="utf-8"), "", ""

    text, failure = download(url)
    if failure:
        return None, "download_blocked", f"Automated download failed: {failure}."
    path = new_copy_dir / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return text, "", ""


# ---------------------------------------------------------------------------
# SMALL HELPERS
# ---------------------------------------------------------------------------

def money_to_int(text):
    """
    "$1,234" -> 1234, "$0" -> 0, "-$5" -> -5, and "", "N/A" or None -> None.
    Returning None rather than 0 is what keeps blanks and real zeros different.
    """
    cleaned = strip_tags(str(text if text is not None else "")).replace("$", "").replace(",", "")
    return int(cleaned) if re.fullmatch(r"-?\d+", cleaned) else None


def strip_tags(text):
    """Remove HTML tags and extra spaces from a piece of text."""
    no_tags = re.sub(r"<[^>]+>", " ", unescape(str(text)))
    return re.sub(r"\s+", " ", no_tags).strip()


# ---------------------------------------------------------------------------
# READING EADA
# ---------------------------------------------------------------------------

def parse_eada(text, school):
    """
    Read one EADA record. Returns a dictionary with amounts by measure, the
    original labels and dates, and any notes the school itself filed.
    Screens are found by NAME because numbering differs: schools with coed
    teams, such as Ohio State, use different screen numbers.
    """
    result = {"amounts": {}, "status": "", "reason": "", "survey_year": "",
              "start": "", "end": "", "caveats": {"revenue": [], "expense": []},
              "supplemental": ""}
    try:
        record = json.loads(text)
        header = record["Header"]
        screens = {screen["ScreenName"]: screen
                   for group in record["Groups"] for screen in group["Screens"]}
    except (json.JSONDecodeError, KeyError, TypeError):
        result.update(status="parse_problem",
                      reason="The EADA file was not the expected data, so nothing was read from it.")
        return result

    if header.get("ID") != school["unitid"]:
        result.update(status="parse_problem",
                      reason=f"The EADA record is for ID {header.get('ID')}, not {school['unitid']}.")
        return result

    result["survey_year"] = str(header.get("SurveyYear", ""))
    result["start"] = str(header.get("ReportingYearStart", ""))[:10]
    result["end"] = str(header.get("ReportingYearEnd", ""))[:10]

    # The year check. EADA's site always serves its newest survey, so once a
    # newer year is posted this leaves cells blank instead of mixing in that year.
    if result["start"][:4] != str(EADA_START_YEAR) or result["end"][:4] != str(EADA_END_YEAR):
        result.update(status="wrong_period",
                      reason=f"The EADA record covers {result['start']} to {result['end']}, not 2024-25. Not used.")
        return result

    revenue = screens.get("Total Revenues by Team", {"Rows": []})
    expense = screens.get("Total Expenses by Team", {"Rows": []})
    summary = screens.get("Revenues & Expenses Summary", {"Rows": []})

    result["amounts"] = {
        "Total athletic revenue": summary_grand_total(summary, "Grand Total Revenues ("),
        "Total athletic expenses": summary_grand_total(summary, "Grand Total Expenses ("),
        "Football revenue": football_total(revenue),
        "Football expenses": football_total(expense),
    }

    # Cross-check: both places EADA shows a grand total must agree.
    pairs = [("Total athletic revenue", revenue), ("Total athletic expenses", expense)]
    for measure, screen in pairs:
        by_team = by_team_grand_total(screen)
        if by_team != result["amounts"][measure]:
            result["amounts"][measure] = None
            result["reason"] += (f" {measure}: the summary and by-team grand totals "
                                 "disagree, so the figure was left blank.")

    result["caveats"]["revenue"] = caveats(revenue)
    result["caveats"]["expense"] = caveats(expense)
    supplemental_screen = screens.get("Supplemental Information", {"Rows": []})
    notes = [strip_tags(cell["Html"]) for row in supplemental_screen["Rows"] for cell in row["Cells"]]
    notes = [note for note in notes if note and note != "Supplemental Information"
             and not note.startswith("No Supplemental Information")]
    result["supplemental"] = " ".join(notes)
    return result


def summary_grand_total(screen, label_start):
    """Find a grand total line in the summary. Its amount is in the last cell."""
    for row in screen["Rows"]:
        cells = [strip_tags(cell["Html"]) for cell in row["Cells"]]
        if len(cells) >= 3 and cells[1].startswith(label_start):
            return money_to_int(cells[-1])
    return None


def by_team_grand_total(screen):
    """Find the 'Grand Total' row. A one-cell row starting that way is a footnote."""
    for row in screen["Rows"]:
        cells = [strip_tags(cell["Html"]) for cell in row["Cells"]]
        if len(cells) >= 2 and cells[0].startswith("Grand Total"):
            return money_to_int(cells[-1])
    return None


def football_total(screen):
    """Find the Football row. Its last cell is the team's total."""
    for row in screen["Rows"]:
        cells = [strip_tags(cell["Html"]) for cell in row["Cells"]]
        if cells and cells[0] == "Football":
            return money_to_int(cells[-1])
    return None


def caveats(screen):
    """Return caveats the school wrote: rows with one cell, without the heading."""
    found = []
    for row in screen["Rows"]:
        if len(row["Cells"]) == 1:
            note = strip_tags(row["Cells"][0]["Html"])
            if note and note != "CAVEAT":
                found.append(note)
    return found


# ---------------------------------------------------------------------------
# READING KNIGHT-NEWHOUSE
# ---------------------------------------------------------------------------

class ChartFinder(HTMLParser):
    """Collect the data stored in each chart on a Knight-Newhouse page."""

    def __init__(self):
        super().__init__()
        self.charts = {}

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        chart_name = attributes.get("data-drupal-selector-chart")
        if chart_name and attributes.get("data-chart"):
            try:
                self.charts[chart_name] = json.loads(attributes["data-chart"])
            except json.JSONDecodeError:
                pass


def parse_knight(text, school):
    """
    Read one Knight-Newhouse page. Returns amounts by measure, or a status that
    explains why there are none. A block page has neither charts nor the
    'not available' message, so it is reported as a problem, never as a zero.
    """
    result = {"amounts": {}, "status": "", "reason": "", "conference": "", "category_sum": None}
    finder = ChartFinder()
    finder.feed(text)
    plain_text = strip_tags(text)

    conference = re.search(r"Conference:\s*([A-Za-z0-9 -]+?)\s+Undergraduate", plain_text)
    result["conference"] = conference.group(1) if conference else ""

    not_public = re.search(r"Athletics financial data is not available[^.]*\.", plain_text)
    if not_public:
        result.update(status="institution_not_disclosed",
                      reason=f"Knight-Newhouse states: \"{not_public.group(0)}\"")
        return result

    if school["knight_name"] not in plain_text or not finder.charts:
        result.update(status="parse_problem",
                      reason="The page had no chart data for this school. It may be a block page.")
        return result

    for measure, details in MEASURES.items():
        if details["knight_chart"]:
            chart = finder.charts.get(details["knight_chart"])
            result["amounts"][measure] = knight_value(chart, school["knight_name"])

    # Optional cross-check against the page's revenue categories.
    pie = finder.charts.get("charts-institution-revenues")
    if pie and pie.get("series"):
        result["category_sum"] = sum(point[1] or 0 for point in pie["series"][0]["data"])
    return result


def knight_value(chart, school_name):
    """
    Take the school's own series, then the value under the year label "2025".
    Charts also hold conference and FBS medians, which are skipped by name.
    """
    if not chart:
        return None
    x_axis = chart["xAxis"][0] if isinstance(chart["xAxis"], list) else chart["xAxis"]
    years = [str(year) for year in x_axis.get("categories", [])]
    if KNIGHT_YEAR_LABEL not in years:
        return None
    position = years.index(KNIGHT_YEAR_LABEL)
    for series in chart["series"]:
        name = strip_tags(series.get("name", ""))
        if name.startswith(school_name) and "Median" not in name:
            value = series["data"][position]
            return None if value is None else int(value)
    return None


# ---------------------------------------------------------------------------
# BUILDING THE ROWS
# ---------------------------------------------------------------------------

def amount_status(amount, source_status, default_missing):
    """Choose the status for one amount. Note that 0 counts as reported."""
    if source_status:
        return source_status
    if amount is None:
        return default_missing
    return "reported_zero" if amount == 0 else "reported"


def build_rows(saved_dir, new_copy_dir, today):
    """Collect all sources and return the 72 rows."""
    rows = []
    collection_date = saved_dir.name if saved_dir else today
    method = f"saved copy dated {saved_dir.name}" if saved_dir else "automated download"

    for school in SCHOOLS:
        print(f"Reading {school['school']}...")

        text, status, reason = get_source("eada", school, saved_dir, new_copy_dir)
        eada = parse_eada(text, school) if text else {
            "amounts": {}, "status": status, "reason": reason, "survey_year": "", "start": "",
            "end": "", "caveats": {"revenue": [], "expense": []}, "supplemental": ""}

        text, status, reason = get_source("knight", school, saved_dir, new_copy_dir)
        knight = parse_knight(text, school) if text else {
            "amounts": {}, "status": status, "reason": reason, "conference": "", "category_sum": None}

        for measure, details in MEASURES.items():
            eada_amount = eada["amounts"].get(measure)
            knight_amount = knight["amounts"].get(measure)
            eada_status = amount_status(eada_amount, eada["status"], "not_reported_by_school")

            # Football revenue is unavailable from Knight-Newhouse for every
            # school, unless we could not read the page in the first place.
            knight_missing = knight["status"]
            if details["knight_chart"] is None and knight_missing in ("", "institution_not_disclosed"):
                knight_missing = "not_published_by_source"
            knight_status = amount_status(knight_amount, knight_missing, "year_not_available")

            rows.append({
                "school": school["school"],
                "measure": measure,
                "eada_amount": "" if eada_amount is None else eada_amount,
                "knight_newhouse_amount": "" if knight_amount is None else knight_amount,
                "eada_status": eada_status,
                "knight_newhouse_status": knight_status,
                "eada_survey_year_label": eada["survey_year"],
                "eada_reporting_start": eada["start"],
                "eada_reporting_end": eada["end"],
                "knight_newhouse_fiscal_year_label": KNIGHT_YEAR_LABEL,
                "eada_source_field": details["eada_field"],
                "knight_newhouse_source_field": details["knight_field"],
                "eada_source_link": EADA_API.format(unitid=school["unitid"]),
                "eada_site": EADA_HOME,
                "knight_newhouse_source_link": KNIGHT_PAGE.format(slug=school["knight_slug"]),
                "knight_newhouse_definitions_link": KNIGHT_DEFINITIONS,
                "eada_collection_date": collection_date,
                "knight_newhouse_collection_date": collection_date,
                "collection_method": method,
                "audit_notes": audit_notes(measure, eada, knight, eada_amount, knight_amount, school),
            })
    return rows


def audit_notes(measure, eada, knight, eada_amount, knight_amount, school):
    """Write the plain-language notes for one row."""
    notes = []

    # Period labels, using this school's own dates.
    if eada["survey_year"]:
        notes.append(PERIOD_NOTE.format(eada_label=eada["survey_year"], start=eada["start"], end=eada["end"]))
        if eada["start"][5:] != "07-01" or eada["end"][5:] != "06-30":
            notes.append("This school's EADA year is not the usual July 1 to June 30.")
    notes.append(KNIGHT_DATES_NOTE)
    notes.append(DEFINITION_NOTE[measure])

    # Why any figure is blank.
    if eada["status"] or eada["reason"]:
        notes.append(f"EADA: {eada['reason'].strip()}")
    if knight["status"]:
        notes.append(f"Knight-Newhouse: {knight['reason']}")
    if measure == "Football revenue" and knight["status"] in ("", "institution_not_disclosed"):
        notes.append(KNIGHT_NO_FOOTBALL_REVENUE)
    if not eada["status"] and eada_amount is None:
        notes.append("EADA: this figure was not found in the 2024-25 record, so it is blank.")
    if (not knight["status"] and MEASURES[measure]["knight_chart"] and knight_amount is None):
        notes.append("Knight-Newhouse: no value under year label 2025, so it is blank. No other year was used.")

    # Things a reader might otherwise take for mistakes.
    if knight["conference"] and knight["conference"] != "Big Ten":
        notes.append(f"Knight-Newhouse's page lists this school's conference as {knight['conference']}. "
                     "Kept here because this study defines the 18-school Big Ten list.")
    if "revenue" in measure:
        partner = measure.replace("revenue", "expenses")
    else:
        partner = measure.replace("expenses", "revenue")
    if eada_amount is not None and eada_amount == eada["amounts"].get(partner):
        notes.append("EADA revenue equals EADA expenses here, exactly as the school reported. "
                     "Schools sometimes report revenue allocated up to expenses, so this may not "
                     "measure money earned.")
    if eada_amount is not None and knight_amount is not None and eada_amount != knight_amount:
        difference = knight_amount - eada_amount
        notes.append(f"Knight-Newhouse minus EADA = {difference:,} dollars.")

    # A category total that disagrees with the headline figure is worth a look.
    if measure == "Total athletic revenue" and knight_amount is not None and knight["category_sum"] is not None:
        if knight["category_sum"] != knight_amount:
            notes.append(f"Knight-Newhouse's revenue categories for 2025 add up to {int(knight['category_sum']):,}, "
                         f"but its Total Athletic Revenues figure is {knight_amount:,}. The stated total is used; "
                         "the difference was not resolved.")

    # The school's own words, kept in full.
    side = "revenue" if "revenue" in measure else "expense"
    for caveat in eada["caveats"][side]:
        notes.append(f"EADA caveat filed by school: {caveat}")
    if eada["supplemental"]:
        notes.append(f"EADA supplemental note filed by school: {eada['supplemental']}")
    return " ".join(notes)


# ---------------------------------------------------------------------------
# CHECKING AND SAVING
# ---------------------------------------------------------------------------

def check_rows(rows):
    """Basic checks on the finished table. Returns a list of problems."""
    problems = []
    if len(rows) != 72:
        problems.append(f"Expected 72 rows, found {len(rows)}.")
    pairs = {(row["school"], row["measure"]) for row in rows}
    if len(pairs) != 72:
        problems.append("Some school and measure pairs are missing or repeated.")
    for row in rows:
        for source, amount_key, status_key in (("EADA", "eada_amount", "eada_status"),
                                               ("Knight-Newhouse", "knight_newhouse_amount", "knight_newhouse_status")):
            label = f"{row['school']} / {row['measure']} / {source}"
            blank = row[amount_key] == ""
            has_figure_status = row[status_key] in ("reported", "reported_zero")
            if blank == has_figure_status:
                problems.append(f"{label}: amount and status do not match.")
            if row[amount_key] == 0 and row[status_key] != "reported_zero":
                problems.append(f"{label}: a zero lost its reported_zero status.")
    return problems


def write_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Collect 2024-25 Big Ten athletic finances.")
    parser.add_argument("--saved-dir", type=Path,
                        help="Folder of saved copies, named with its date, e.g. saved_sources/2026-11-05")
    parser.add_argument("--output", default=OUTPUT_CSV, help="Name of the CSV to write")
    args = parser.parse_args()

    today = datetime.date.today().isoformat()
    if args.saved_dir:
        # The folder name is the collection date, so it has to be a real date.
        try:
            datetime.date.fromisoformat(args.saved_dir.resolve().name)
        except ValueError:
            sys.exit(f"Please name the saved folder with its date, like 2026-11-05. Got: {args.saved_dir}")
        if not args.saved_dir.is_dir():
            sys.exit(f"Folder not found: {args.saved_dir}")
        args.saved_dir = args.saved_dir.resolve()

    new_copy_dir = Path("saved_sources") / today
    rows = build_rows(args.saved_dir, new_copy_dir, today)

    # If anything was blocked, do not overwrite a good CSV with a blank one.
    statuses = [row[key] for row in rows for key in ("eada_status", "knight_newhouse_status")]
    blocked = sum(status in ("download_blocked", "saved_copy_missing", "parse_problem") for status in statuses)
    output = Path(args.output)
    if blocked:
        output = output.with_name(output.stem + "_INCOMPLETE" + output.suffix)

    problems = check_rows(rows)
    write_csv(rows, output)

    print(f"\nWrote {len(rows)} rows to {output}")
    for status in sorted(set(statuses)):
        print(f"  {status}: {statuses.count(status)} cells")
    if blocked:
        print(f"\n{blocked} cells could not be collected, so the file is marked INCOMPLETE.")
        print("Those cells are blank; no numbers were guessed. If the websites blocked the script,")
        print("follow 'If the websites block the script' in the README and use --saved-dir.")
    if problems:
        print("\nCHECKS FAILED:")
        for problem in problems:
            print(f"  {problem}")
        sys.exit(1)
    print("\nChecks passed: 72 unique rows, and every blank has a status explaining it.")


if __name__ == "__main__":
    main()
