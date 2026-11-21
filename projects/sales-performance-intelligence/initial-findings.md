# Initial Findings — Sales Performance Intelligence

**Analysis period:** January 2024–December 2025  
**Dataset:** 1,200 synthetic order lines across 1,200 distinct orders  
**Currency:** Unspecified currency units  
**Status:** Descriptive analysis of a generated demonstration dataset; not a real-company performance assessment

## Executive KPI snapshot

| KPI | Result |
|---|---:|
| Records | 1,200 |
| Distinct orders | 1,200 |
| Units sold | 5,155 |
| Revenue | 558,057.39 |
| Cost | 343,858.98 |
| Profit | 214,198.41 |
| Profit margin | 38.38% |
| Average order value | 465.05 |

Calculations use revenue = quantity × unit price; cost = quantity × unit cost; profit = revenue − cost; profit margin = total profit ÷ total revenue.

## Findings from the generated sample

### 1. Revenue and profit leadership are closely contested across regions

- South has the highest revenue: 141,974.44.
- South also has the highest profit: 54,633.31.
- West is a close second in revenue (141,223.79) and profit (54,524.93).
- West has the highest unit volume (1,443), while South has 1,286 units.

**Interpretation:** The regional gap is narrow. A management dashboard should show revenue, profit, and margin together and avoid overstating small differences in generated data.

### 2. Furniture dominates revenue and profit contribution

| Category | Revenue | Profit | Profit margin |
|---|---:|---:|---:|
| Furniture | 348,885.01 | 127,081.58 | 36.43% |
| Electronics | 169,679.10 | 68,329.39 | 40.27% |
| Office Supplies | 39,493.28 | 18,787.44 | 47.57% |

Furniture contributes the largest absolute revenue and profit. Office Supplies has the highest margin percentage but a much smaller revenue base.

**Interpretation:** Margin percentage and profit contribution answer different questions. The dashboard should present both.

### 3. Corporate is the largest segment by revenue

| Segment | Revenue | Profit | Orders |
|---|---:|---:|---:|
| Corporate | 225,255.84 | 87,716.09 | 412 |
| Small Business | 201,150.39 | 76,685.31 | 434 |
| Consumer | 131,651.16 | 49,797.01 | 354 |

Corporate leads revenue and profit, while Small Business has the highest order count. These differences make average order value and order volume useful companion measures.

### 4. Product contribution varies substantially

- Desk is the highest-revenue product: 161,799.54.
- Desk also generates the highest total profit: 55,572.93.
- Notebook Pack has the lowest revenue (2,828.08) and profit (1,886.15), despite 470 units sold.
- Notebook Pack has the highest product margin (66.69%) in this generated sample.

**Interpretation:** High unit volume or margin does not automatically translate into the largest absolute profit contribution.

### 5. Monthly results vary; generated seasonality is not market evidence

- November 2025 records the highest monthly revenue: 39,466.40.
- December 2024 records the second-highest monthly revenue: 31,552.63.
- November 2025 also records the highest monthly profit: 14,652.18.
- Every month contains 50 generated orders by design.

**Interpretation:** The generator intentionally applies a seasonal multiplier to November and December. The resulting peaks are a property of the simulation, not evidence of real seasonal demand. Do not describe them as discovered market seasonality.

## Data-quality and interpretation notes

- The dataset contains 1,200 records and 1,200 distinct order IDs.
- The generated date range is 1 January 2024–31 December 2025.
- Quantities are positive; unit prices and unit costs are non-negative.
- Every row represents one order line and one order in this version.
- The dataset is synthetic and reproducible from a fixed seed.
- No taxes, discounts, shipping, returns, refunds, operating expenses, or real customer/company identifiers are included.
- These are descriptive results from simulated data only. They should not be presented as evidence about a real retailer or used for forecasting.

## Recommended dashboard design

1. KPI row: Revenue, Profit, Profit Margin, Orders, Units Sold, and Average Order Value.
2. Monthly trend: Revenue and Profit by month across 24 months.
3. Regional comparison: Revenue, Profit, Margin, and order volume.
4. Category profitability: Revenue and Profit with margin labels.
5. Customer segments: Revenue, Profit, Orders, and Average Order Value.
6. Product analysis: Revenue, Profit, Units Sold, and Margin.
7. Filters: Date, Region, Category, and Customer Segment.

## Recommended next analysis steps

- Build a Tableau dashboard using the transaction-level dataset, not only pre-aggregated CSVs.
- Add scenario analysis to show how changes in unit cost or selling price affect profit.
- Add a separate multi-line order dataset in a future iteration if basket-level analysis is required.
- Continue reconciling Python, SQLite, and dashboard calculations.
- Keep synthetic-data limitations visible in the project and dashboard.
