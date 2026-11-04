# Milestone 2: Initial Custom Dataset and Audit Plan

**Student:** Abhinav Penaganti  
**Project:** Big Ten Athletic Spending  
**Group Theme:** The Business of College Sports

## Project Overview

For my part of the group project, I wanted to look at where athletic departments spend their money after they bring it in. Brayden is focusing more on where the money comes from, so I thought looking at spending would work well with his topic. I am mainly interested in things like coaching salaries, facilities, recruiting, scholarships and other expenses related to athletes.

My research question is: **How do Big Ten athletic departments report their spending, and what do those categories tell us about where the money goes?**

I also want to look at what we *cannot* tell from those numbers. For example, a university might report millions of dollars in coaching expenses, but a total like that doesn't tell us exactly who received the money. My instructor's feedback helped me think more about the difference between a reported expense, an actual payment and an estimated NIL value. I don't want to treat those as if they measure the same thing.

## Initial Dataset

My dataset is called `athletic_spending.csv`. I used the **Audit and Augment Existing Data** approach because I started with financial information published by Knight-Newhouse and added my own categories and notes about what the numbers mean.

My larger project will look at Big Ten schools from **2015 through 2025**. For this first dataset, I made a smaller sample of **86 records from 13 current Big Ten schools**, covering selected years from **2020 through 2025**. This fits the assignment's goal of starting with about 50 to 100 records before trying to collect much more data.

I organized the sample in three parts:

1. **24 athletic department expense records.** I recorded 12 expense categories for Illinois and Purdue in 2024. These include coaching, recruiting, athletic student aid, meals, facilities and other expenses.
2. **26 football spending records.** I included total football spending for 13 schools in 2023 and 2024.
3. **36 football coaching salary records.** I included six schools from 2020 to 2025 so I could follow one type of spending over several years.

I chose a mix of detailed categories and broader totals because I wanted to see how much information we lose when spending gets grouped together. The sample is not random, and it isn't a complete record of every Big Ten school or year.

**Each row represents one school, one fiscal year and one spending category or reported total.** It is not a record of a payment to one person. I kept the names used by the source instead of renaming everything to fit my own categories.

## What I Included in the CSV

Each record has the school, year, spending category and reported dollar amount. I also included the source URL so someone else could look up the number.

The main columns are:

| Column | What it means |
|---|---|
| `record_id` | An ID so I can find a row again |
| `institution` | The school |
| `fiscal_year` | The financial reporting year |
| `source_category` | The category name used by Knight-Newhouse |
| `amount_usd` | The reported amount in dollars |
| `reported_share_pct` | A category's share of expenses when the report provides it |
| `payer_actor` | Who appears to be paying, based on the category |
| `recipient_or_beneficiary` | Who or what appears to benefit |
| `interpretation` | My explanation of what the category covers |
| `interpretive_limit` | What the number doesn't tell us |
| `verification_level` | How far the source check has gone |
| `source_url` | Link to the original public report or school page |

I left a value blank if the source showed N/A. I did not enter zero because zero would mean there was no spending. One example is Purdue's 2024 total football spending record, which has no published amount in the selected report.

## Data Sources

I mainly used the [Knight-Newhouse College Athletics Database](https://knightnewhousedata.org/). It provides public spending data for major college athletic programs and explains where its figures come from. The database uses financial information reported by universities through the NCAA, but its categories are still a way of organizing that information.

The reports I used most were:

- [2024 athletic department expense categories](https://knightnewhousedata.org/reports/58d7a6f8)
- [2023 and 2024 football spending comparison](https://knightnewhousedata.org/reports/3c45c499)
- [Knight-Newhouse data definitions](https://knightnewhousedata.org/about-the-data)
- [Knight-Newhouse FAQ](https://knightnewhousedata.org/faq)

I included links to the individual school pages for the coaching salary records. Some of those values still need to be checked one by one against the source pages.

I originally planned to use The NIL Standard and The Sideline as well. I still want to compare their NIL information later, but I did not mix their estimates into the spending amounts in this CSV. An NIL estimate might describe what a player is believed to be worth. It does not necessarily show an amount paid by a university or another company.

## How I Turned the Sources Into Data

I started by choosing a small number of schools, years and financial measures instead of downloading everything at once. For Illinois and Purdue, I used the published 2024 expense categories and kept their original names. Then I added football spending totals and football coaching salary figures for a comparison across schools and years.

I had to decide what one data item should be. I decided on one school, one year and one category because the public reports usually summarize spending in that way. I also added columns explaining what the category means, who is involved where the report gives enough detail, and what information is missing.

For example, **Facilities, Debt Service, and Equipment** combines several types of costs. It doesn't tell me how much was spent on building something new compared with paying off debt or buying equipment. The category **Competition Guarantees - Expenses** is another example. It shows an annual expense, but it doesn't tell me which individual games led to those payments. Chenglin's project is looking at individual guarantee games, so our projects cover different levels of the same kind of financial relationship.

I kept football totals and football coaching salaries separate from the department expense categories. They overlap with other spending figures, so adding them together would count some expenses twice. This was one of the bigger decisions I had to make when organizing the dataset.

## Computational Process

I used Python to check my CSV. The script is in `check_dataset.py`, and it runs in VS Code without any extra packages. It checks how many rows I have, whether amounts are missing, whether school and category combinations appear more than once, and whether the year, amount and source fields are formatted correctly.

I also made `source_checks.csv`, which has 50 rows comparing figures in my dataset with the amounts and percentages in published Knight-Newhouse tables. My code looks for differences between those two files. The results are saved in `validation_output.txt`.

The script found:

- 86 total records from 13 schools
- 85 records with a dollar amount and one record with N/A
- 24 department expense records, 26 football totals and 36 football coaching salary records
- 50 rows in the public-table check file with no differences found
- 0 duplicate school/year/category combinations
- 0 other formatting or structural problems

For Illinois and Purdue, the 12 published department expense percentages in 2024 add up to 100% for each school.

This is useful because I don't have to check every CSV cell for basic mistakes by hand. The limitation is that the script only compares what is in my files. It does not prove that the universities reported everything correctly. I also have not checked the original university accounting documents, and the 36 coaching salary records still need individual source review.

## Audit Plan

For my audit, I want to focus on how Knight-Newhouse reports spending and what the larger categories leave out. My main question is: **When a university reports one spending total, how much can we tell about who paid the money and who received it?**

I plan to look more closely at the definitions behind a few categories, especially coaching compensation, facilities, recruiting and athletic student aid. I want to compare those definitions with the public numbers and, where available, the original university financial reports. I also want to see whether schools use the same categories in the same way.

Another part of my audit will involve NIL. The NIL Standard and The Sideline report information about athlete deals and valuations, while Knight-Newhouse focuses on university athletic finances. Before comparing those sources, I need to understand who created each number, whether it is an estimate or reported expense, and whether any real payment is documented. I would keep those different measures in separate columns or tables rather than adding them together.

## What I Noticed So Far

One thing I noticed is how different the same category looks across schools. In 2024, Illinois reported **$47,667,874** for facilities, debt service and equipment, while Purdue reported **$30,025,623**. Illinois also reported **$34,593,992** for coaches compensation compared with **$23,298,385** at Purdue.

I thought the differences were interesting, but I don't think the amounts alone explain why one school spends more. For example, the facilities category includes multiple kinds of costs, and the report doesn't show the individual contracts behind the total.

I also learned that a blank value is not the same as zero. If I changed Purdue's missing 2024 football total to zero, someone looking at the data might think Purdue stopped spending money on football, which would not be supported by the source.

## Reflection

At first, I thought this project would mostly involve collecting spending numbers and comparing schools. After going through the categories, I realized there is more to think about. A school might report a large amount under coaching or facilities, but that one number doesn't explain the full financial relationship. It also made me more careful about comparing reported expenses with estimated NIL values because they are not measuring the same thing.

The hardest part is deciding which categories are comparable and how much I can say about them. I want to keep the original category names so readers know exactly what was reported. I also added notes when the source doesn't identify the person or organization receiving the money. My current sample leaves out some schools and years, so I still have more work to do before making broader comparisons.

## Next Steps

After this initial dataset, I want to expand to **500 to 1,000 or more records** using the same general approach. My goal is to cover Big Ten athletic spending from **2015 through 2025**, depending on which years and schools have comparable reports.

I plan to use Python to import more Knight-Newhouse tables, clean up school names, match records by fiscal year and category, and check missing or duplicate entries. If there are official exports available, I would start with those instead of scraping pages. I will also keep a file showing how category names changed between years so I don't accidentally compare two different kinds of expenses.

I expect a few problems when I scale up. Some schools joined the Big Ten later than others, and private schools do not always have the same public reporting coverage. The definitions of financial categories can also change over time. COVID years might look different from other years as well. My code will help find strange or missing values, but I will still need to go back to the sources to understand why those differences appear.

For the final group website, I want my part to show how different Big Ten schools spend money while also explaining what the totals leave out. This should connect with Brayden's revenue research without repeating it, and it will keep my topic separate from Vedant's player outcomes and Chenglin's game payments.

## Scholarly Context

Lawrence, Gabriel and Tuttle (2010) discuss why comparing athletic expenses can be difficult when schools organize and report costs differently. This connects to my decision to keep the source categories and document what each one means. Jones (2020) looks at the quality of college athletics financial data using Benford's Law. That reading also connects to why I want to check my data instead of assuming all the numbers are equally reliable.

## References

- Knight-Newhouse College Athletics Database. [About the Data](https://knightnewhousedata.org/about-the-data).
- Knight-Newhouse College Athletics Database. [2024 expense report](https://knightnewhousedata.org/reports/58d7a6f8).
- Knight-Newhouse College Athletics Database. [2023-2024 football spending report](https://knightnewhousedata.org/reports/3c45c499).
- Knight-Newhouse College Athletics Database. [Frequently Asked Questions](https://knightnewhousedata.org/faq).
- Lawrence, H. J., Gabriel, E. A., & Tuttle, L. E. (2010). Using Activity-Based Costing to Create Transparency and Consistency in Accounting for Division I Intercollegiate Athletics. *Journal of Intercollegiate Sport, 3*(2), 366-381. https://doi.org/10.1123/jis.3.2.366
- Jones, W. A. (2020). A Benford Analysis of National Collegiate Athletic Association Division I Finance Data. *Journal of Sports Economics, 21*(3), 234-255. https://doi.org/10.1177/1527002519887430

## Project Files

- `athletic_spending.csv`: the 86-record dataset
- `source_checks.csv`: 50 comparisons with published tables
- `check_dataset.py`: my Python validation script
- `validation_output.txt`: the script's saved results
- `README.md`: folder instructions
- `milestone2.md`: this document
