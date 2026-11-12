# Instructor Feedback for Milestone 2

This is a promising project with substantial technical infrastructure. The central question is strong: what changes when the same institution’s finances are represented through EADA and Knight-Newhouse? I particularly appreciate that you retain both values rather than forcing them into one supposedly correct total. The project recognizes that differences may result from reporting periods, definitions, institutional practices, source coverage, or extraction choices rather than simple error.

I also appreciate your transparency about the AI-assisted code, documentation, and annotations. The most important remaining work is not necessarily expanding the dataset, but demonstrating your own close engagement with selected records and revising the interpretations in your own terms.

## Initial Custom Dataset

The dataset has a clear structure: each row represents one school, one reporting-period label, and one financial measure. The four measures are total athletic revenue, total athletic expenses, football revenue, and football expenses. Keeping EADA and Knight-Newhouse in separate columns makes the comparison visible without assuming that the two sources measure identical things.

Including all eighteen Big Ten institutions is useful because it preserves problems involving private institutions, recent conference members, and uneven public access rather than silently removing them. The status fields also appropriately distinguish unavailable values from reported zeroes.

I would retain the current 72-record scope. A longer time series would introduce changing definitions, conference realignment, inflation, and additional reporting-period problems before the initial comparison has been fully understood. One carefully audited reporting period is enough for the final project.

## Computation and Preliminary Analysis

The collector and validation script perform meaningful computational work. Caching the responses also makes the extraction reproducible if the live interfaces change.

The 144 matching comparisons establish that the CSV is consistent with the saved responses and the collector’s parsing rules. However, because the validation code reuses the collector’s logic, agreement does not independently confirm that the original fields were interpreted correctly. I suggest describing these as **reproduction and extraction checks**, while reserving **source verification** for comparisons with original institutional or NCAA reports.

Your preliminary analysis already identifies several productive patterns:

- Illinois has substantially different department-revenue totals across the two sources.
- Northwestern uses a different EADA reporting period.
- Knight-Newhouse values are unavailable for several private-school records.
- The selected Knight-Newhouse profiles do not display football-revenue charts for the eighteen schools.
- Some football-expense totals are closely aligned while others differ substantially.
- Eight EADA records report identical department revenue and expense totals, while none of the populated Knight-Newhouse pairs are exactly equal.

That final pattern could be especially useful for investigating reporting conventions. It does not prove that EADA is inaccurate. Instead, it raises questions about how revenues, expenses, and balancing entries are defined and reported.

## Existing-Data Audit

The audit plan is specific and well connected to the custom dataset. Comparing EADA and Knight-Newhouse allows you to investigate two representations of the same institutions without assuming that one provides the authoritative answer.

I especially like the decision to preserve original terms before creating shared categories and to allow a conclusion of “not comparable.” The audit could distinguish among three related questions:

- What does each public system display, and did the code retrieve it consistently?
- Do the labels describe the same measure and period?
- How do selected values connect to institutional, EADA, or NCAA financial documents?

The final analysis should also distinguish among different kinds of missingness. A measure might not appear on the selected public profile, might be unavailable because an institution is private, might exist elsewhere but not have been retrieved, or might have no equivalent in the other source. These are different findings from a genuine reported zero.

Rather than investigating all eighteen institutions equally, I suggest concentrating on a purposive set of cases such as Illinois, Northwestern, USC, and a few unusually close or divergent records. For each case, you might document the reporting dates, original category names, source definitions, underlying reports, and whether comparison is appropriate. You do not need to resolve every discrepancy; a carefully documented unresolved difference is itself an important audit finding.

## Scholarship and Reflection

The EADA, Knight-Newhouse, and provider documentation are essential primary and methodological sources, but the project still needs engagement with two or three published scholarly sources. Relevant scholarship might address college-athletics finance, institutional accounting, NCAA reporting practices, public-record access, or the politics of financial classification. These sources should help you interpret why the systems differ rather than simply being added to the bibliography.

Your current limitations and plans are thoughtful, but the final reflection should explain more fully what you personally learned from examining the evidence. In particular, I would like to see which interpretations you accepted, revised, or rejected after manually reviewing selected records.

The AI documentation should also clarify who or what produced the “supplied” dataset, collector, and cached responses; which parts you ran, read, tested, or modified; and how you verified that the intended fields were collected. Including a few representative prompts and explaining the resulting decisions would make this process more transparent.

Finally, the README says that the folder has not been uploaded to the group repository even though it is now present there. That status language should be updated.

## Priorities for the Final Project

- Retain the current 72-record scope and prioritize depth over adding more reporting periods.
- Manually review a purposive selection of close, divergent, and missing cases.
- Distinguish extraction checks from independent source verification.
- Document when values are comparable, comparable with caution, or not comparable.
- Interpret missingness at the interface, institutional, and reporting levels.
- Clarify the provenance and authorship of the supplied dataset, code, and caches.
- Expand the AI documentation with representative prompts, revisions, and verification decisions.
- Add and apply two or three relevant scholarly sources.
- Write a fuller personal reflection based on your own source review.
- Update the outdated repository-status language.

Overall, the project has a strong question, a coherent comparative dataset, and sophisticated computational scaffolding. The strongest final version will use a small number of carefully investigated discrepancies to show how reporting systems construct athletic finances differently, rather than automatically expanding to hundreds of additional records.
