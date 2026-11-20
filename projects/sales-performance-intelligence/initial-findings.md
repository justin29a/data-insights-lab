# Initial Findings — Sales Performance Intelligence

**Analysis period:** 1 January–27 June 2025  
**Dataset:** 24 synthetic order records  
**Currency:** Unspecified currency units  
**Status:** Initial descriptive analysis; not a real-company performance assessment

## Executive KPI snapshot

| KPI | Result |
|---|---:|
| Records | 24 |
| Distinct orders | 24 |
| Units sold | 108 |
| Revenue | 6,241 |
| Cost | 3,664 |
| Profit | 2,577 |
| Profit margin | 41.29% |
| Average order value | 260.04 |

Calculations use revenue = quantity × unit price; cost = quantity × unit cost; profit = revenue − cost; profit margin = total profit ÷ total revenue.

## Findings from the sample

### 1. Revenue leadership and profit leadership differ by region

- North generated the highest revenue: 1,923 (30.8% of total revenue).
- West generated the highest profit: 732 (28.4% of total profit), despite revenue of 1,610.
- East sold the most units (38) but had the lowest regional revenue (1,221).

**Interpretation:** Revenue volume alone does not describe regional profitability. The dashboard should show revenue, profit, and margin together rather than ranking regions on revenue only.

### 2. Furniture leads category revenue; Electronics is close in profit

| Category | Revenue | Profit | Profit margin |
|---|---:|---:|---:|
| Furniture | 3,040 | 1,110 | 36.51% |
| Electronics | 2,415 | 1,083 | 44.84% |
| Office Supplies | 786 | 384 | 48.85% |

Furniture accounts for 48.7% of revenue. Electronics contributes 42.0% of profit despite lower revenue than Furniture. Office Supplies has the highest category margin in this sample, but the lowest revenue.

**Interpretation:** A high margin percentage does not necessarily mean the largest profit contribution. Both margin and absolute profit should be considered.

### 3. Corporate is the largest customer segment by revenue

| Segment | Revenue | Profit | Orders |
|---|---:|---:|---:|
| Corporate | 2,755 | 1,053 | 9 |
| Small Business | 2,152 | 898 | 6 |
| Consumer | 1,334 | 626 | 9 |

Corporate represents 44.1% of revenue. Small Business has fewer orders but contributes 34.5% of revenue.

**Interpretation:** Segment comparisons should include order count and average order value, not revenue alone.

### 4. Product-level results show different types of contribution

- Desk has the highest product revenue (1,600).
- Office Chair has the highest product profit (560).
- Notebook Pack has the lowest product revenue (198) and profit (132), but the highest unit volume (33).

**Interpretation:** Product volume, revenue, and profit tell different stories. The product view should allow users to compare all three.

### 5. Monthly revenue fluctuates across the six-month sample

- February recorded the highest revenue (1,420).
- January recorded the lowest revenue (585).
- April recorded the highest monthly profit (527).
- June revenue was 917.

**Interpretation:** The sample shows variation, but six months and four orders per month are insufficient to infer seasonality or a durable growth trend.

## Data-quality and interpretation notes

- The dataset contains 24 rows and 24 distinct order IDs.
- All quantities are positive; unit prices and unit costs are non-negative.
- The date range is 1 January–27 June 2025.
- The dataset is intentionally small and synthetic.
- It contains no taxes, discounts, shipping, returns, refunds, operating expenses, or actual customer/company identifiers.
- These are descriptive results only. They should not be presented as evidence about a real retailer or used for forecasting.

## Recommended dashboard design

1. KPI row: Revenue, Profit, Profit Margin, Orders, Units Sold.
2. Monthly trend: Revenue and Profit by month.
3. Regional comparison: Revenue, Profit, and Margin.
4. Category profitability: Revenue and Profit with margin labels.
5. Customer segments: Revenue, Profit, Orders, and Average Order Value.
6. Product analysis: Revenue, Profit, Units Sold, and Margin.
7. Filters: Month, Region, Category, and Customer Segment.

## Recommended next analysis steps

- Reconcile Python outputs with SQLite query results.
- Build an Excel workbook with formula checks and pivot tables.
- Build the Tableau dashboard using the validated output tables.
- Expand the dataset with more records and realistic edge cases before attempting advanced analysis.
