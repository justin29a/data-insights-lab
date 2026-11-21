# Excel Executive Workbook — Publication Status

## Current status

The Excel workbook described in the earlier version of this document was built against the original 24-row January–June 2025 sample. The source dataset has since been expanded and replaced with a deterministic 1,200-order dataset covering January 2024–December 2025.

**The earlier workbook is now a legacy snapshot and must not be used as the current dashboard deliverable.** Its source data and KPI values do not match the current repository dataset. A refreshed workbook must be generated and independently recalculated before it is presented as current.

## Required workbook structure

| Worksheet | Purpose |
|---|---|
| Executive Dashboard | KPI cards, date/region/category selectors, and headline charts |
| Raw Data | All 1,200 synthetic order lines in a formatted Excel table |
| Monthly Analysis | 24-month revenue, cost, profit, and margin trends |
| Regional Analysis | Revenue and profitability by region |
| Category Analysis | Revenue, profit, and margin by category |
| Product Analysis | Product-level sales and profitability |
| Customer Analysis | Comparison by customer segment |
| Data Quality | Completeness, validity, uniqueness, and reconciliation checks |
| Read Me | Metric definitions, assumptions, provenance, and usage notes |

## Current executive metrics

- **Revenue:** 558,057.39
- **Cost:** 343,858.98
- **Profit:** 214,198.41
- **Profit margin:** 38.38%
- **Orders:** 1,200
- **Units sold:** 5,155
- **Average order value:** 465.05

All monetary values are in unspecified currency units.

## Data provenance and limitations

All transactions, products, sales representatives, and business context are fictional. The dataset is generated with a fixed seed. November and December multipliers are deliberate simulation parameters, not evidence of real-world seasonality. Each order currently has one line item. Taxes, discounts, shipping, returns, refunds, operating expenses, and real customer/company identifiers are absent.

## Reproducibility

From the repository root:

```bash
python -m pip install -r requirements.txt
python python/generate_sales_data.py
python python/analyze_sales.py
```

The generator recreates the deterministic source CSV; the analysis script writes six summary CSVs to `outputs/`.

## Publication checklist

A refreshed workbook is not considered complete until:
- Its raw-data sheet contains all 1,200 current rows.
- KPI formulas reconcile to the figures above.
- Monthly, regional, category, product, and segment totals reconcile to the Python and SQLite outputs.
- Filter behavior is tested in Excel or Google Sheets.
- Formula recalculation is verified in a spreadsheet application.
- The current workbook binary is committed or otherwise clearly published with a working link.
