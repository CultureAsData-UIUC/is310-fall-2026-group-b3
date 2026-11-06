# Milestone 2: Initial Custom Dataset and Audit Plan

**Student:** Brayden  
**Project:** Big Ten Athletic Revenue and Financial Reporting  
**Group Theme:** The Business of College Sports  
**Status:** My local AI-assisted draft for review; not uploaded.

## Project Overview

My project examines how money coming into Big Ten athletic programs is reported and what changes when the same institution is described by different financial reporting systems. The research question is: **How do EADA and Knight-Newhouse represent Big Ten athletic revenue, and what can their differences reveal about the limits of comparing financial totals?**

The group studies how money moves through college sports. This part focuses on incoming money and its representation. It complements Abhinav’s spending project and Chenglin’s guarantee-game project without repeating their questions.

This initial submission uses two sources: EADA and Knight-Newhouse. It compares institution-level figures for 2024–25. It does not include conference-level financial data. The two sources retain their own definitions and values rather than being combined into a single revenue figure.

## Definition and Inclusion Rules

My initial sample covers the 18 Big Ten member schools in 2024–25. One row represents **one school, one reporting-year label, and one financial measure**, with the two sources retained in separate columns.

The inclusion rules are:

1. Include all 18 schools in the chosen Big Ten cohort, including private schools with incomplete source coverage.
2. Use the supplied EADA records whose reporting dates begin in 2024 and end in 2025.
3. Select the value labeled 2025 from each available Knight-Newhouse historical chart; do not substitute another year or a conference median.
4. Preserve missing figures as blank cells with source-status information, rather than replacing them with zero.
5. Keep source labels, dates, retrieval information, and URLs so a comparison can be revisited.

My study is a bounded comparison, not a random sample or a complete history of Big Ten finances.

## Initial Dataset

The supplied `big_ten_2024_25.csv` contains **72 records: 18 schools × four measures**. The measures are total athletic revenue, total athletic expenses, football revenue, and football expenses. Revenue is the main topic; expenses provide context for interpreting the revenue figures and should not become a separate spending analysis.

The two sources are columns within each row, not two independent records. Thus, 72 rows do not mean 144 independent observations. There are 72 populated EADA amount cells and 48 populated Knight-Newhouse amount cells.

The original CSV has been preserved unchanged. The added `audit_annotations.json` augments it with comparison decisions, reporting-period cautions, and caveats extracted from the supplied EADA responses. Those notes are AI-assisted drafts that I still need to review; automatic collection and annotations do not by themselves establish close manual engagement with all 72 items.

### Fields

| Field | Description |
|---|---|
| `school` | Short institution name used in the study |
| `reporting_year` | Study period label, 2024–25 |
| `measure` | Department or football revenue/expense measure |
| `eada_amount_usd` | EADA amount, in nominal US dollars |
| `knight_amount_usd` | Knight-Newhouse amount, in nominal US dollars; blank when unavailable |
| `eada_period_start`, `eada_period_end` | Dates reported in the EADA response |
| `eada_survey_year` | Original EADA survey-year label |
| `knight_year_label` | Selected Knight-Newhouse chart label, 2025 |
| `eada_status`, `knight_status` | Whether an amount was collected or why it is absent |
| `eada_source`, `knight_source` | Links to the source response or institutional profile |
| `eada_field`, `knight_chart` | Source field or chart used for extraction |
| `eada_retrieved_at`, `knight_retrieved_at` | Retrieval timestamps recorded in the supplied cache |
| `eada_retrieval`, `knight_retrieval` | Original retrieval mode |
| `audit_notes` | Supplied notes about interpretation and coverage |

The companion annotations add a comparison decision, reasons, school caveats where present, authorship, and verification scope. They distinguish a contextual comparison from a case where no numeric comparison is possible.

## Data Sources

### EADA

The [Equity in Athletics Data Analysis Cutting Tool](https://ope.ed.gov/athletics/) is operated by the US Department of Education. Its overview describes annual reporting by coeducational postsecondary institutions receiving Title IV funding and offering intercollegiate athletics.

The supplied collector reads the institution responses behind the site. It uses department grand totals from the Revenues & Expenses Summary and football figures from the team revenue and expense screens. It does not substitute game-day operating expenses for total football expenses.

### Knight-Newhouse

The [Knight-Newhouse College Athletics Database](https://knightnewhousedata.org/) provides institutional profiles and historical charts. Its [methodology](https://knightnewhousedata.org/about-the-data) explains that financial figures come from NCAA Membership Financial Reporting System reports, not EADA financial reports. It also describes differences in institutional interpretation and limitations in public disclosure.

The supplied cache contains public profile HTML and embedded chart values. The collector selects the institution series rather than a conference or subdivision median. The exact chart values are preferable to rounded visual labels.

## Computational Work and Completed Checks

The supplied collector uses Python’s built-in libraries to parse cached JSON and HTML responses. Running it offline reproduced all 72 records, amounts, dates, statuses, and supplied notes. Only EADA retrieval-mode labels changed, from the original live collection to saved-snapshot use.

The added `check_dataset.py` checks the dataset against the supplied saved responses. It verifies the school/measure pairs, source amounts, dates, selected Knight year, and consistency between populated values and collection statuses. It also extracts school caveats for the draft annotations.

Results saved in `validation_output.txt`:

- 72 unique records from 18 schools.
- 72 EADA amounts and 48 Knight-Newhouse amounts.
- 144 matching saved-response comparisons, including 24 missing Knight values.
- No structural or extraction mismatches detected by these checks.
- Northwestern’s four rows use September 1, 2024–August 31, 2025; the other 68 rows use July 1, 2024–June 30, 2025.

These are reproducibility and extraction checks. They reuse the collector’s parsing functions and do not independently establish that university reports are correct. Agreement with a saved source response is not the same as agreement with the original institutional accounting record.

## Interpretive Decisions and Initial Observations

**Different totals are not automatically mistakes.** Illinois’s department revenue is $174,612,181 in the supplied EADA record and $194,761,178 in the selected Knight-Newhouse chart. Both values are retained. The difference motivates a reporting-definition audit; it does not establish that one is wrong or identify the reason for the difference.

**Matching year labels do not prove identical reporting periods.** Northwestern has a different EADA period from the other schools. Knight-Newhouse’s year label alone does not verify the school’s precise start and end dates. Such comparisons need period checks before numerical conclusions are drawn.

**Missingness has different meanings.** The selected Knight profiles lack a football-revenue chart for all 18 schools. Six additional blanks concern the three other measures at Northwestern and USC. The supplied status codes say these figures were not shown; they should not be interpreted as zero revenue or spending. The collector has not established that every missing value is absent from every possible source.

**Nested amounts cannot be summed.** Football revenue is part of athletic-department activity, not an extra amount to add to department revenue. The comparison therefore keeps department totals and football figures separate.

**School language matters.** The saved EADA screens contain school caveats where reported. These are preserved in the companion annotations rather than replaced with a universal explanation. Caveats can provide leads for source review, but do not automatically reconcile the two systems.

## Audit Plan

My audit will investigate **what the revenue figures include, how they were produced, and when two figures can reasonably be compared**.

First, I plan to review a purposive set of cases: Illinois as an example of differing totals, Northwestern as a period and coverage case, USC as a private-school coverage case, and additional schools selected for differences or explanatory caveats. For each case, inspect the cached EADA response alongside the public profile, and record the exact field labels, dates, and relevant school notes.

Second, I plan to consult the reporting instructions and, where accessible, original university NCAA financial reports. Check the department revenue and football-revenue figures against those materials. Record document title, page or line, URL, reporting period, and the result. The current saved-response checks must remain separate from these future underlying-report checks. An unresolved difference should remain unresolved rather than be explained by assumption.

Third, I plan to investigate which revenue categories are combined or omitted by each system. Before assigning a standardized category, preserve the original term and document the evidence for the mapping. Record decisions not to compare when scope, definition, or reporting period differs. A broad total does not by itself show individual donors, contracts, payers, or recipients.

Finally, I plan to document the comparison decisions for EADA and Knight-Newhouse, including cases where reporting periods, definitions, or unavailable figures prevent a meaningful numeric comparison.

## Limitations and Reflection Points for Review

The work so far shows that a clean table can conceal differences in definition, coverage, and reporting periods. Computational checks help locate those differences, but cannot determine their meaning on their own.

I have not yet manually verified all records, read every original report, or independently confirmed every AI-generated interpretation. Before submission, I need to review the cases and annotations, correct interpretations as needed, and add a short reflection based on my review. The close source work requested in the instructor feedback remains distinct from the completed automated extraction checks.

## Next Steps

I plan to complete and document the selected original-report checks, then revise my comparison decisions based on evidence. I will keep a record of corrections and unresolved cases.

After I understand the initial period, I plan to expand to additional comparable years using Python and available exports or saved responses. At four measures across 18 schools, eight reporting periods could provide 576 school/measure records, although missingness and membership changes may limit meaningful comparisons. Expansion is a target, not a claim that these observations have already been collected.

Record membership by the relevant year, retain source category names, detect changes in reporting definitions, and check reporting-period overlap. Use automation to identify candidates and inconsistencies while reserving judgment about comparability for source-based review.

The final presentation should explain where reported revenue comes from and what its categories reveal or conceal, connecting to the group’s spending and payment projects without treating revenue, expenses, valuations, and payments as interchangeable.

## Sources Used

The dataset uses only these two sources. The methodology and FAQ links below explain Knight-Newhouse’s own data; they are supporting documentation from the same source, not additional datasets.

- US Department of Education. [Equity in Athletics Data Analysis Cutting Tool (EADA)](https://ope.ed.gov/athletics/). Institution-level athletic revenue and expense figures.
- [Knight-Newhouse College Athletics Database](https://knightnewhousedata.org/). Institution-level historical chart figures. Supporting documentation: [About the Data](https://knightnewhousedata.org/about-the-data) and [Frequently Asked Questions](https://knightnewhousedata.org/faq).

## AI Assistance

AI organized the supplied files, checked offline reproduction, created validation and annotation code, and drafted this documentation. Source amounts in the supplied CSV were not replaced with generated figures. See `ai-chat-log.md` for a summary. I am keeping this folder local until I have reviewed it.
