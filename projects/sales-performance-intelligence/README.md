# Sales Performance Intelligence

**Project type:** Business Intelligence / Sales Analytics  
**Status:** Initial portfolio release  
**Data:** Synthetic retail transactions (fictional; created for demonstration)

## Business scenario

A fictional multi-region retailer wants a clearer view of sales performance, profitability, product mix, and customer segments. This project establishes a reproducible analysis workflow that turns transaction-level records into management-ready metrics.

> **Data notice:** Every transaction in this project is synthetic. The dataset does not represent a real company, customer, employee, or commercial result.

## Business questions

1. What are total revenue, cost, profit, and profit margin?
2. How do revenue and profit change month by month?
3. Which regions and product categories contribute most to revenue and profit?
4. Which products generate the strongest and weakest profit?
5. How do customer segments compare?

## KPI definitions

| Metric | Definition |
|---|---|
| Revenue | Quantity × Unit price |
| Cost | Quantity × Unit cost |
| Profit | Revenue − Cost |
| Profit margin | Profit ÷ Revenue × 100 |
| Units sold | Sum of quantity |
| Orders | Distinct order IDs |

All monetary values are expressed in **unspecified currency units**. No currency symbol is assumed.

## Repository workflow

| Tool | Purpose |
|---|---|
| Excel | Initial inspection, pivot tables, validation, and summary reporting |
| SQL (SQLite) | Aggregations and business-question queries |
| Python (pandas) | Data validation, calculated fields, and repeatable summaries |
| Tableau | Executive dashboard design and interactive exploration |

## Project files

- [Synthetic sales dataset](../../datasets/sales_data.csv)
- [Data dictionary](../../docs/data_dictionary.md)
- [SQL analysis](../../sql/sales_analysis.sql)
- [Python analysis script](../../python/analyze_sales.py)
- [Initial findings and KPI results](initial-findings.md)
- [Analysis output tables](../../outputs/)

## Run the Python analysis

From the repository root:

```bash
python -m pip install -r requirements.txt
python python/analyze_sales.py
```

The script validates the source data, prints executive KPIs and grouped summaries, and exports six reusable CSV tables to `outputs/` for Excel and Tableau. The committed output tables are the initial calculated results for this sample dataset.

## SQL environment

The SQL file is written for SQLite. Import `datasets/sales_data.csv` into a table named `sales_data`, then run the queries in [sales_analysis.sql](../../sql/sales_analysis.sql).

## Tableau dashboard plan

The planned dashboard has:
- KPI cards for revenue, profit, margin, orders, and units sold
- Monthly revenue and profit trend
- Revenue and profit by region
- Category and product profitability
- Customer-segment comparison
- Filters for date, region, category, and customer segment

A dashboard should only be published after the underlying calculations have been validated.

## Current scope and limitations

This first release establishes the dataset, metric definitions, SQL query set, and Python analysis workflow. It is a small synthetic dataset intended to demonstrate analytical methods, not to support real-world market conclusions. Findings and recommendations should be added only after the analysis has been executed and checked.

## Next improvements

- Validate SQL and Python outputs against independently calculated Excel results.
- Expand the dataset and add edge cases for data-quality testing.
- Build and publish the Tableau dashboard.
- Add evidence-based findings and business recommendations.
- Add screenshots and a reproducible dashboard link.
