# Milestone 2: Initial Custom Dataset and Audit Plan

**Student:** Chenglin Chu  
**Project:** College Football Guarantee Games  
**Group Theme:** The Business of College Sports

## Project Overview

This project studies college football guarantee games, especially the financial relationship that can be hidden behind an ordinary game record. A standard football dataset can show that two teams played, where the game occurred, and the final score, but it may not show that one institution agreed to pay another institution to participate in the matchup. My custom dataset adds that financial context to FBS–FCS games.

In response to feedback on Milestone 1, I narrowed the initial sample to the **2024 season** and to games in which an **FBS team hosted an FCS team**. One row represents one game. This narrower scope makes it possible to check the sporting record and payout evidence more carefully instead of building a larger dataset with uneven documentation.

The current initial dataset contains **50 manually checked records**, meeting the lower end of the assignment target of approximately 50–100 records. I stopped the initial version at 50 so that each added game could still be checked against a payout source and a game record rather than expanding the sample with uneven evidence. Later versions can continue toward 75–100 records using the same inclusion rules.

## Definition and Inclusion Rules

For this project, a **guarantee game** is a matchup in which a larger program hosts another program and there is credible public evidence that the visiting school was promised or reported to receive financial compensation for playing the game.

For this initial sample, a record is included when:

1. the game was played during the 2024 season;
2. the home team was classified as FBS and the visiting team was classified as FCS;
3. a public source reported a payout or a contract-based guarantee for the matchup; and
4. the date and final score could be checked against a game record or official athletics source.

An FBS–FCS matchup by itself is not enough to establish that it is a guarantee game. The financial relationship needs supporting evidence. Missing information is left blank rather than coded as zero.

## Initial Dataset

The structured dataset is stored in `guarantee_games.csv`.

### Fields

| Field | Description |
|---|---|
| `season` | Football season |
| `game_date` | Date the game was played |
| `home_team` | Hosting institution |
| `away_team` | Visiting institution |
| `home_level` | Home team's subdivision classification |
| `away_level` | Away team's subdivision classification |
| `location` | City and state of the game |
| `home_score` | Final points scored by the home team |
| `away_score` | Final points scored by the visiting team |
| `score_difference` | Absolute difference between the two final scores |
| `contract_amount_usd` | Amount stated in a contract or contract-based source, when available |
| `reported_amount_usd` | Amount reported by a journalist or secondary source |
| `actual_payment_evidence` | Evidence that money was actually transferred, when available |
| `payment_status` | Description of what kind of payout evidence is currently available |
| `contract_date` | Date a contract was executed, when available |
| `cancellation_terms` | Relevant cancellation language, when available |
| `payout_source_type` | Type of source supporting the payout figure |
| `payout_source_url` | URL for the payout evidence |
| `game_source_url` | URL used to verify the game record |
| `notes` | Context that cannot be represented well in a numeric field |
| `uncertainty_notes` | Unresolved questions or limits of the evidence |

A major interpretive decision was to separate `contract_amount_usd`, `reported_amount_usd`, and `actual_payment_evidence`. These values can refer to different things. A journalist's reported payout does not automatically prove that the same amount appears in a signed contract or that the transfer was completed. For example, Southern Illinois' 2024 trip to BYU was reported as producing $560,000 in total, but that figure includes a $425,000 BYU guarantee and $135,000 connected to the previously scheduled Kansas game. Keeping these amounts distinct prevents a complicated financial arrangement from being flattened into one number.

## Data Sources

I used multiple types of sources because no single source contains all of the information needed for this project.

- **HERO Sports** provides a 2024 compilation of reported FCS-versus-FBS payouts. I treat these as *reported amounts*, not automatically as contractual or completed payments.
- **FBSchedules** is useful when its reporting is based on obtained game contracts or school announcements.
- **Official university athletics pages and box scores** are used to check game dates, locations, and final scores.
- **CollegeFootballData (CFBD)** will be the main existing dataset audited during the next stage of the project.

Each row preserves payout and game source URLs so that the record can be checked again later.

## Transformation 1: Cultural Material to Working Representation

The first transformation begins with public cultural materials that were not created as one unified dataset: game schedules, official box scores, contract reporting, school announcements, and sports journalism about guarantee payments.

For each candidate game, I identify the two schools, check their FBS/FCS classifications, record the game date and result, and locate payout evidence. I also make notes when a source creates ambiguity. This produces a working representation in which the sporting event and the financial evidence can be compared side by side.

This step involves interpretation. A payout reported in an article may be based on a contract, a school statement, or another report, and those sources do not all provide the same level of certainty. I therefore preserve the source and the uncertainty instead of treating every dollar amount as equivalent.

## Transformation 2: Working Representation to Structured Data

The second transformation converts those working notes into standardized CSV records. Team roles are separated into home and away fields, institutional levels are standardized as `FBS` and `FCS`, dates use `YYYY-MM-DD`, dollar amounts receive separate fields based on evidence type, and the score margin is stored as an absolute numeric value.

I also preserve qualitative information in `notes` and `uncertainty_notes`. This is important because some details—such as a cancellation-related payment or a payout that has not been matched to an underlying contract—would be lost if the dataset contained only numeric fields.

## Computational Process

The file `check_dataset.py` provides a reproducible computational check of the initial CSV. The script:

- counts the total number of records;
- counts records with contractual, reported, or actual-payment evidence;
- identifies rows with no payout amount;
- recalculates the expected score difference and flags mismatches;
- checks that every row fits the FBS-home/FCS-away scope; and
- detects duplicate game records.

For the current 50-row version, the script reports **0 score-difference errors, 0 records outside the defined subdivision scope, and 0 duplicate records**. It also makes the source limitation visible: most current payout figures are reported amounts, while only a small number have been matched to contract-based evidence and none yet contain independent evidence of a completed money transfer.

Computation therefore supports consistency checking, but it does not decide what a financial source means. I still manually review the evidence before deciding whether a number belongs in `contract_amount_usd`, `reported_amount_usd`, or another field.

## Audit and Connection Plan

I will audit **CollegeFootballData (CFBD)** as the existing representation of college football games. CFBD's Games API represents a game through fields such as season, date, venue, home and away teams, conference and classification, points, line scores, attendance, and other sporting metadata. Its documentation states that games, scores, records, and matchups have broad historical coverage, while also warning that a supported range does not guarantee that every team, game, subdivision, or field is complete.

My audit will investigate:

1. which CFBD fields represent each guarantee game in my sample;
2. whether the date, team names, classification, venue, and score agree with the sources used in my custom dataset;
3. how CFBD documents its coverage and missing data;
4. whether any selected games or fields show inconsistencies; and
5. what changes when the financial records in my dataset are placed alongside CFBD's sporting record.

The central audit question is:

> **How does CollegeFootballData represent FBS–FCS guarantee games, and what financial and institutional relationships become invisible when these games are represented primarily through standard sporting fields?**

I do not expect CFBD to function as a financial database. The purpose of the audit is instead to examine what kind of cultural object a "game" becomes when a dataset is designed around schedules and results, and what another representation can make visible.

## Initial Observations

Several patterns are already visible in the initial data. Reported payouts vary substantially across games, and many of the games ended with large score differences. However, payout size and score difference alone cannot establish that a game was harmful or unfair. They describe only part of the institutional relationship.

The research process also shows that "payout" is not a single self-explanatory variable. A figure can describe a contractual guarantee, a journalist's reported amount, a cancellation-related payment, or potentially an actual transfer. Treating all of these as identical would erase important context. This is why the dataset records both evidence type and uncertainty.

## Reflection

What is working best is the connection between the custom dataset and the audit. A normal game record is easy to recognize, while adding financial evidence changes the interpretation of that same event. The source-by-source process also makes provenance visible because each row can be traced back to the material used to construct it.

The biggest difficulty is verification. Scores and dates are relatively easy to confirm, but payment information is distributed across contract reporting, school announcements, public-record requests, and journalism. Some reported payout figures do not expose the underlying contract, and evidence of an agreed amount is not the same as evidence that the payment was actually completed. Rather than hiding that problem, I now treat uncertainty and missingness as part of the dataset.

The project changed from the broader idea in Milestone 1 by narrowing the initial sample to one season and one matchup type. This change was made so that I can research the financial evidence more carefully. Feedback that would be useful is whether a reported payout with a clearly preserved source is sufficient for inclusion in the final dataset, or whether the final version should require contract-level evidence for every record.

## Next Steps

My next steps are to:

1. expand the sample beyond the current 50 records toward 75–100 using the same inclusion rules;
2. replace reported payout figures with contract-based evidence when accessible without deleting the original reported value;
3. collect contract dates and cancellation terms where the source supports them;
4. use the CFBD API to retrieve the corresponding standard game records computationally;
5. standardize team names and match CFBD records to the custom dataset by date and team;
6. document discrepancies and missing fields found during the audit; and
7. analyze how the financial representation changes the interpretation of games that otherwise look like ordinary schedule/results records.

I may use Python/API requests and pattern matching to make record matching more efficient, but financial evidence will continue to be manually verified because different documents can use the same monetary language to mean different things.

## Scholarly Context

**Ballou and Nordstrom (2020)** study the safety implications of FCS teams playing guarantee games against stronger FBS opponents. Their work is useful because it shows why a guarantee game cannot be interpreted only through payout and final score. Athlete risk is part of the broader institutional context, and my data should not make claims about harm without additional evidence.

**Faure and Cranor (2010)** examine why FCS institutions participate in "big money" games and identify both financial motivations and possible costs, including lopsided losses and injury concerns. Their work helps frame the payout as part of an institutional decision rather than simply a number attached to a game.

**Toma (2010)** places guarantee games within the broader financial structure of intercollegiate athletics and discusses how smaller programs use these games as a revenue strategy while larger programs benefit from additional home games. This helps connect my individual dataset to the group's larger theme of how money moves through college sports.

## References

Ballou, D. E., & Nordstrom, H. E. (2020). Safety of college football student-athletes: Playing guarantee games against superior opponents. *Journal for the Study of Sports and Athletes in Education, 14*(2), 83–99. https://doi.org/10.1080/19357397.2020.1768035

Faure, C. E., & Cranor, C. (2010). Pay for slay: An examination of the repercussions of the big money game on the little guy in college football. *Journal of Issues in Intercollegiate Athletics, 3*, 194–210. https://scholarcommons.sc.edu/jiia/vol3/iss1/11/

Toma, J. D. (2010). Intercollegiate athletics, institutional aspirations, and why legitimacy is more compelling than sustainability. *Journal of Intercollegiate Sport, 3*(1), 51–68. https://doi.org/10.1123/jis.3.1.51

## Project Files

- `guarantee_games.csv` — initial structured custom dataset
- `check_dataset.py` — computational consistency-checking script
- `milestone2.md` — documentation, audit plan, reflection, and next steps
