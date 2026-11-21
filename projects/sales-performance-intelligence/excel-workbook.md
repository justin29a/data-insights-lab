# Excel Executive Workbook

## Purpose

The Excel workbook is the spreadsheet reporting layer for the **Sales Performance Intelligence** case study. It is designed to let a reviewer move from executive KPIs to supporting detail and basic data-quality checks without changing the source dataset.

## Workbook structure

| Worksheet | Purpose |
|---|---|
| Executive Dashboard | KPI cards, region/category selectors, and headline charts |
| Raw Data | The 24 synthetic transaction records in a formatted Excel table |
| Monthly Analysis | Monthly revenue, cost, profit, and performance trends |
| Regional Analysis | Revenue and profitability by region |
| Category Analysis | Revenue and units by product category |
| Product Analysis | Product-level sales and profitability |
| Customer Analysis | Comparison by customer segment |
| Data Quality | Basic checks on source completeness and validity |
| Read Me | Metric definitions, assumptions, provenance, and usage notes |

## Executive metrics

- **Revenue:** quantity multiplied by unit price, summed across records.
- **Cost:** quantity multiplied by unit cost, summed across records.
- **Profit:** revenue minus cost.
- **Profit margin:** total profit divided by total revenue.
- **Orders:** distinct order IDs.
- **Units sold:** sum of quantity.

The source dataset currently contains 24 records and 24 distinct order IDs. It covers January–June 2025. The figures are in unspecified currency units because no currency was provided in the fictional scenario.

## Interactivity and limitations

The dashboard includes region and category selectors that update its KPI calculations. The monthly and regional charts are overall views and do not currently respond to those selectors. This distinction is intentional and should be kept clear when presenting the workbook.

## Data provenance

All transactions, customers, sales representatives, products, and business context are fictional and were created for portfolio demonstration. The dataset is not a representation of a real company or actual commercial performance.

## Reproducibility

The repository also includes:
- `datasets/sales_data.csv` — source data
- `python/analyze_sales.py` — pandas analysis and CSV output generation
- `sql/sales_analysis.sql` — SQLite queries for business analysis

Run the Python analysis from the repository root:

```bash
python -m pip install -r requirements.txt
python python/analyze_sales.py
```

The script writes six summary CSV files to `outputs/`.

## Publication status

The workbook was generated as a companion deliverable and structurally checked after saving. Its formulas have not yet been independently recalculated in Microsoft Excel or Google Sheets, and the binary workbook is not yet committed to this repository. Do not treat the workbook as a fully formula-validated or repository-hosted artifact until those checks and publication are complete.
