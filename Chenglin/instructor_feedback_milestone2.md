# Instructor Feedback for Milestone 2

I really like how substantially you narrowed this project after Milestone 1. Limiting the initial dataset to the 2024 season and to FBS-home/FCS-away games gives you a coherent unit of analysis and makes it possible to investigate the financial evidence behind each matchup.

The most promising idea here is that a game can be represented in several different ways. A conventional sports dataset makes the schedule and result visible, while your custom data attempts to represent the financial arrangement and uncertainty behind the same event. Your distinction among a reported payout, contractual guarantee, and evidence of an actual transfer is especially important. Those categories prevent the word “payout” from flattening several different claims into one apparently certain number.

I would not prioritize expanding from 50 to 75 or 100 records unless additional records become necessary for a specific comparison. Instead, focus on verifying the existing sample, developing its cultural interpretation, and completing the CollegeFootballData audit.

## Initial Custom Dataset

Your documentation clearly defines a qualifying record, but it does not fully explain why these particular fifty games were selected. The `reported_amount_usd` values are ordered from $760,000 to $375,000, suggesting that the dataset may contain the first or highest-paying fifty games from the HERO Sports compilation. If so, that is a meaningful sampling decision rather than a neutral stopping point.

I would suggest documenting:

- How many 2024 FBS-home/FCS-away games appeared in the source list
- Whether these are the fifty highest reported payouts
- Whether any candidate games were excluded and why
- Whether every eligible game had a publicly reported payout
- What this sample allows you to claim about guarantee games more broadly

A sample of the largest publicly reported payouts could be useful and defensible. It would mean framing the findings as an analysis of higher-paying, publicly documented games rather than a representative account of every 2024 guarantee game.

### Financial Evidence and Provenance

I appreciate the care with which you distinguish different forms of financial evidence. At present, however, 48 of the 50 records rely on the same HERO Sports compilation, only two contain a contract amount, and none contains independent evidence of a completed transfer. This does not make the dataset invalid, but its clearest current object is **reported guarantee amounts**, not verified payments.

A clearly sourced reported payout is sufficient for inclusion if it remains accurately labeled. Requiring contracts for every game may be unrealistic and could create a new bias toward institutions whose records are easier to obtain. Instead, preserve the layers of evidence:

- Reported amount from a secondary compilation
- Contract amount verified through a document or contract-based report
- School announcement or official statement
- Evidence of an actual transfer
- Unresolved or contradictory evidence

You could verify a smaller purposive subset in depth, perhaps including high, middle, and lower reported amounts or unusual cases. This would let you assess how reliably the compilation represents underlying agreements without requiring fifty public-record investigations.

Because 48 rows point to one URL, document who created the HERO Sports list, how its author obtained the figures, whether it cites contracts or institutions, and whether it has been updated. This makes provenance visible at both the row and source level.

### Dataset Structure

The dataset structure is thoughtful and well documented. The fields for `contract_date`, `cancellation_terms`, and `actual_payment_evidence` are currently empty, which I assume reflects evidence you hoped to obtain rather than evidence presently available. Explain that these are planned or evidence-dependent fields. If they remain empty, you could retain them to document unavailable evidence or remove them from the publication dataset and discuss their absence in the essay.

The absolute `score_difference` is useful for measuring closeness, but it removes the direction of the result. Your score fields preserve that information, including Idaho’s victory over Wyoming. You might add `home_team_won` or `fcs_team_won` if upsets become relevant to the analysis.

### Cultural Interpretation and Competing Perspectives

Your dataset is already careful about financial uncertainty, but it records less about how guarantee games are culturally and institutionally framed. A payment does not have one self-evident meaning. The same game might be described as revenue, exposure, competitive opportunity, necessary sacrifice, institutional partnership, or an unfair transfer of athletic risk.

I would not assign one label such as `fair` or `exploitative` to every game. Those judgments cannot be established from payout and score alone. Instead, examine a smaller source-rich subset and record:

- Who describes or justifies the arrangement
- Which institution is presented as benefiting
- Which benefits are named, such as revenue, exposure, competition, or recruiting
- Which costs or risks are acknowledged
- Whether the visiting institution is represented as an active decision-maker
- Whether different sources offer competing interpretations
- What evidence supports the classification
- How confident you are in the interpretation

Because one game may support several claims from different actors, a related table such as `game_interpretations.csv` may work better than adding one definitive field to every game row. One row could represent one interpretive claim, with fields such as `game_id`, `speaker`, `source`, `frame`, `evidence`, `confidence`, and `alternative_reading`.

This would allow you to investigate not only how much money was reportedly involved, but how institutions and media make these relationships culturally meaningful. It would also preserve disagreement instead of presenting your interpretation as an objective property of the game.

## Computational Work

The validation script is a meaningful computational contribution. I especially like that it recalculates score differences, tests the FBS/FCS scope, checks duplicates, and reports different levels of payout evidence.

For the final stage, preserve the original team names alongside names standardized for CFBD matching. Also record match status and cases requiring manual resolution so that all matched records do not appear equally certain.

## Auditing CollegeFootballData

The CFBD audit plan is specific and well connected to the custom dataset. It compares the same games across two representations rather than introducing an unrelated dataset.

The absence of payout data from CFBD is important, but it is expected because CFBD primarily represents sporting records. I would avoid treating this as simply missing information or an API failure. Its schema constructs a college football game through teams, dates, venues, scores, classifications, and statistics. Your custom dataset represents the same event as a financial and institutional relationship.

The audit could examine:

- Whether each sampled game is present
- Whether names, classifications, dates, venues, and scores agree
- Which records are difficult to match
- Which fields are missing or inconsistent
- Which financial relationships cannot be represented in CFBD
- What changes when your financial evidence is joined to the standard game record

This supports a stronger argument about how database design constructs a college football game as a cultural object.

Similarly, payout size or score difference alone cannot prove that a matchup was harmful or unfair. Descriptive questions are a good starting point:

- How are reported payouts distributed?
- Which games were close, lopsided, or won by the FCS visitor?
- Is there an exploratory relationship between reported guarantee and score difference?
- How often can a reported amount be traced to stronger evidence?
- How do institutions explain the benefits or risks of selected games?

## Scholarship, Reflection, and AI Use

Your scholarship meaningfully informs the project. The sources help explain why guarantee games involve institutional revenue, competitive imbalance, and athlete safety without assuming that one variable can represent all three.

Your reflection is also strong. The Southern Illinois/BYU example is particularly useful because the reported $560,000 total does not describe one straightforward guarantee from one game. I would develop that example in the final essay.

I did not see an AI-use statement. If you used AI for research, code, writing, or classification, explain what it contributed and how you checked its outputs. If you did not use AI, a brief statement confirming that would also clarify the methodology.

## Priorities for the Final Project

- Explain how the fifty games were selected.
- Treat current amounts as reported guarantees unless stronger evidence supports another label.
- Verify a strategic subset rather than requiring contracts for every record.
- Investigate the provenance and methods of the HERO Sports compilation.
- Add a small interpretive claims table or another transparent method for encoding competing perspectives.
- Match the records to CFBD while preserving naming changes and uncertainty.
- Interpret CFBD’s schema rather than treating missing financial fields only as errors.
- Use scholarship and selected cases to contextualize quantitative patterns.
- Add an AI-use statement.

Overall, this is a strong and carefully scoped project. You have a defensible unit of analysis, substantial documentation, meaningful computation, relevant scholarship, and a well-connected audit plan. The main opportunity is to move from documenting financial uncertainty to encoding and analyzing how institutions culturally frame these financial relationships.
