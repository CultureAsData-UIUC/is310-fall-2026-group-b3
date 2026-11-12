# Instructor Feedback for Milestone 2

I really like how this project has developed into an investigation of both athletic spending and the categories through which spending becomes visible.

The strongest part of the submission is your recognition that a financial total is not a transparent description of where money went. Your fields for `payer_actor`, `recipient_or_beneficiary`, `interpretation`, `financial_relationship`, and `interpretive_limit` attempt to document what a category makes visible and what it obscures. You also correctly keep department expense categories, total football spending, coaching compensation, and NIL estimates conceptually separate rather than adding unlike measures together.

I would not prioritize expanding it to 500–1,000 records. I think the more productive next step would be to investigate how Knight-Newhouse constructs its categories, clarify which comparisons each part of your current sample can support, and verify a strategic subset against the underlying institutional reports.

## Initial Custom Dataset

The current CSV combines three related but differently sampled bodies of data:

- 24 department-expense records covering twelve categories for Illinois and Purdue in 2024
- 26 total football-spending records covering thirteen schools in 2023 and 2024
- 36 football-coaching-salary records covering six schools from 2020 through 2025

Keeping these records in one long-format file can work, especially because `source_category` and `unit_of_analysis` distinguish them. However, the three subsets cannot be treated as though they provide equal coverage of the same schools and years. I would suggest documenting why Illinois and Purdue were selected for the detailed category comparison, why the salary series contains those six schools, and why the football totals contain thirteen institutions.

You might add a field such as `analysis_subset` with values like `department_categories`, `football_total`, and `football_coaching_compensation`. This would make it easier to filter the data correctly and prevent someone from accidentally summing overlapping records. Separate tables are another option, but they are not required if the shared file and documentation make the distinctions clear.

### Big Ten Membership and Institutional Coverage

The phrase “13 current Big Ten schools” needs some clarification. The conference now includes eighteen institutions, but membership changed during the period you are studying. Knight-Newhouse also bases its historical conference groupings on membership during each fiscal reporting year. Oregon, Washington, UCLA, and USC joined for the 2025 fiscal year, while private institutions such as Northwestern do not have the same public financial coverage.

I would suggest documenting:

- Which Big Ten institutions are absent from each subset
- Whether the absence is caused by private-school disclosure limits, conference membership dates, unavailable reports, or your sampling decision
- Whether `conference_membership_that_year` was checked for every fiscal year rather than assigned from current membership
- Whether the unit of comparison is the historical Big Ten or institutions that belong to the conference today

This missingness is not simply a problem to fix. It could become part of the audit because public-record laws and conference realignment shape which institutions can be compared.

### Source Categories and Interpretive Fields

I appreciate that you preserve Knight-Newhouse's source categories and separately explain what they appear to represent. This makes the transformation from published financial table to your structured dataset visible.

At the same time, fields such as `payer_actor`, `recipient_or_beneficiary`, and `financial_relationship` are your interpretations rather than values directly reported by the source. I would suggest making that distinction explicit in the documentation and perhaps adding the source definition or the specific NCAA reporting line used to support each interpretation.

Some categories combine several financial relationships. For example, facilities, debt service, and equipment combines building costs, debt payments, leases, maintenance, overhead, and equipment. Coaching compensation can include university payments as well as certain contractually guaranteed third-party payments. Your `interpretive_limit` field already identifies these problems well. In the final essay, one or two detailed examples could show readers why an apparently straightforward category cannot answer “who received the money?” without further evidence.

### NIL Comparisons

I agree with your decision not to combine NIL estimates with institutional athletic-spending figures. Estimated athlete valuation, third-party NIL compensation, institutional revenue sharing, scholarship support, and university-reported expenses are different measurements produced for different purposes.

If you retain NIL data, treat it as a comparison of provenance and representation rather than as directly comparable monetary values. Ask who created each measure, what evidence it uses, what unit it represents, and which forms of payment it excludes. You might preserve NIL as a separate table or analytical subset rather than incorporating it into the institutional spending totals.

This comparison is optional. The existing spending data and Knight-Newhouse audit already provide enough material for the final project.

## Computation

The validation script is useful and well designed. The fifty matches establish that those values were transcribed consistently from the public Knight-Newhouse tables. They do not independently verify the university's original financial reporting, and you clearly recognize this in the documentation. I might describe these as **transcription or table checks** rather than source verification so readers understand exactly what was tested.

The remaining 36 coaching-salary records still need individual review. That does not mean all of them must be traced through original accounting documents before the project is complete. You could verify that each value appears on the linked Knight-Newhouse page and then select a smaller number of revealing records for deeper comparison with institutional or NCAA financial reports.

Your Illinois and Purdue example demonstrates both the appeal and limitation of financial comparison. Illinois reports more than Purdue in facilities, debt service, and equipment and in coaches’ compensation, but those aggregate totals do not reveal which contracts, projects, people, or accounting practices produced the difference.

Rather than analyzing all 86 records together, you might develop comparisons within the appropriate subsets:
- Illinois and Purdue across the same twelve 2024 department categories
- Total football spending across the same thirteen schools in 2023 and 2024
- Coaching compensation over time for the same six schools
- Missing or unavailable values across institutions and years
- Changes coinciding with altered definitions or conference membership

These comparisons would let you identify patterns without adding overlapping totals or implying that every subset has the same coverage. Ideally, the computation should support comparisons that the dataset structure can defend rather than producing one summary across incompatible records.

## Auditing Knight-Newhouse

Knight-Newhouse is a strong audit target because it is not merely a neutral container of university figures. Its data come primarily from NCAA Membership Financial Reporting System reports released through public-record requests, while Knight-Newhouse groups and presents those line items through its own categories and reporting interface.

Your audit could investigate several related transformations:

- How university-reported NCAA line items become Knight-Newhouse categories
- Which categories combine multiple line items
- Whether institutions interpret NCAA reporting rules differently
- How category definitions change over time
- Which schools are absent because their records are not publicly available
- How conference membership is assigned across fiscal years
- Whether values displayed in current dollars are comparable over time

The final point is especially important for your 2020–2025 coaching series. Knight-Newhouse displays current dollars by default and offers inflation adjustment as an option. You do not necessarily need to adjust the amounts, but you should state whether your analysis uses nominal or inflation-adjusted dollars and avoid interpreting every change as a change in real spending.

The source also notes changes to financial categories over time. For example, some categories and reporting lines changed in fiscal year 2025. Your plan to preserve a record of category-name changes is therefore important. The audit could identify whether a visible increase or decrease reflects actual spending, a new reporting definition, or both.

## Scholarship and Reflection

The scholarship is relevant and already connected to your project decisions. Both sources are sufficiently well-integrated at this stage; though you might add another source only if it directly supports the specific argument you develop.

Your reflection also identifies the central conceptual shift in the project. You began by planning to collect and compare spending figures, but the category definitions made you ask what those numbers actually represent and what relationships remain hidden. That is a strong direction for the final essay. I would develop it through a few concrete records rather than trying to resolve every uncertainty through scale.

I did not see an AI-use statement in the submission. If you used AI for coding, research, writing, or developing categories, the final documentation should explain how it was used and how you checked the outputs. If you did not use AI, a brief statement confirming that would still make the process clear.

## Priorities for the Final Project

For the next stage, I would suggest prioritizing:

- Documenting why each of the three subsets includes different schools, years, and categories.
- Clarifying historical Big Ten membership and the effects of private-school and public-record coverage.
- Making the distinction between source-reported fields and your interpretive fields explicit.
- Treating the fifty matches as transcription checks and verifying the remaining linked values.
- Auditing how Knight-Newhouse transforms NCAA financial reports into its published categories.
- Documenting category-definition changes and whether your longitudinal figures use current or inflation-adjusted dollars.
- Building the final analysis from comparable subsets rather than summing or comparing all records together.
- Adding an AI-use statement.

Overall, this is a strong and thoughtful submission. The project does not need hundreds of additional rows as its most compelling contribution will be showing how athletic spending becomes structured through institutional reports, public-record access, changing definitions, and Knight-Newhouse's categories, and how those structures shape what we can conclude about where the money goes.
