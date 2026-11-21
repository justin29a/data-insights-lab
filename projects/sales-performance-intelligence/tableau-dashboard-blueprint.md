# Tableau Executive Dashboard Blueprint

## Objective

Build a portfolio-quality Tableau dashboard that helps management explore revenue, profitability, product mix, and customer segments over a two-year simulated period.

**Source:** `datasets/sales_data.csv`  
**Period:** January 2024–December 2025  
**Data status:** Entirely synthetic; all monetary values are unspecified currency units.

## 1. Connect and prepare the data

Connect Tableau to the raw `sales_data.csv` file. Use the raw transaction-level file as the dashboard's single source. Do not use the pre-aggregated output CSVs as the primary source for an interactive dashboard: doing so can prevent filters and calculations from behaving consistently at transaction level.

Confirm the data types:
- `order_date`: Date
- `quantity`, `unit_price`, `unit_cost`: Number
- IDs and descriptive fields: String

No currency symbol should be applied because the scenario does not specify a currency.

## 2. Create calculated fields

**Revenue**
```tableau
[quantity] * [unit_price]
```

**Cost**
```tableau
[quantity] * [unit_cost]
```

**Profit**
```tableau
[Revenue] - [Cost]
```

**Profit Margin**
```tableau
IF SUM([Revenue]) = 0 THEN NULL
ELSE SUM([Profit]) / SUM([Revenue])
END
```
Format as a percentage with two decimal places.

**Orders**
```tableau
COUNTD([order_id])
```

**Units Sold**
```tableau
SUM([quantity])
```

**Average Order Value**
```tableau
IF COUNTD([order_id]) = 0 THEN NULL
ELSE SUM([Revenue]) / COUNTD([order_id])
END
```

**Sales Month**
```tableau
DATETRUNC('month', [order_date])
```

## 3. Dashboard layout

Use a fixed desktop canvas of approximately **1440 × 900 px** or a device-adaptable layout. Keep a consistent grid, restrained typography, and clear spacing. Use a light neutral background with a dark navy header; reserve accent colors for meaningful comparisons.

### Header
- Title: **Sales Performance Intelligence**
- Subtitle: *Executive overview | January 2024–December 2025*
- Visible note: *Synthetic demonstration dataset · Currency unspecified*

### KPI row
Six KPI cards:
1. Revenue — 558,057.39
2. Cost — 343,858.98
3. Profit — 214,198.41
4. Profit Margin — 38.38%
5. Orders — 1,200
6. Units Sold — 5,155

Also show Average Order Value (465.05) in the segment detail or as a secondary KPI.

### Main analysis area

**Worksheet A — Monthly Performance**
- Columns: Sales Month
- Rows: Revenue and Profit
- Marks: Line
- Show all 24 months in chronological order.
- Tooltip: revenue, cost, profit, margin, orders, units.
- Include a subtle annotation that November/December demand multipliers are part of the simulation design, not observed market seasonality.

**Worksheet B — Regional Performance**
- Rows: Region
- Columns: Revenue
- Marks: Horizontal bars.
- Sort descending by revenue.
- Tooltip: revenue, profit, margin, orders, units.

**Worksheet C — Category Performance**
- Compare revenue and profit by category.
- Show margin as a labelled secondary measure or tooltip.
- Sort descending by revenue.

**Worksheet D — Product Performance**
- Scatter plot:
  - X-axis: Revenue
  - Y-axis: Profit
  - Size: Units Sold
  - Label: Product
  - Tooltip: revenue, cost, profit, margin, units, orders.

**Worksheet E — Customer Segment Performance**
- Compare revenue and profit by customer segment.
- Tooltip: margin, orders, units, average order value.
- Sort descending by revenue.

## 4. Filters and dashboard actions

Add these dashboard filters:
- Order Date (range)
- Region
- Category
- Customer Segment

Apply each filter to all relevant worksheets using the same data source. Add dashboard filter actions so selecting a region, category, or segment filters other views. Provide a clear reset action.

Keep KPI cards connected to the same filters. Validate that selecting one region changes KPI values and charts consistently.

## 5. Design and usability standards

- Use descriptive chart titles.
- Use consistent number formatting and two decimal places for percentages.
- Avoid 3D charts, excessive gridlines, decorative gauges, and unnecessary legends.
- Use accessible contrast and do not rely on color alone to communicate status.
- Keep labels readable at full dashboard size.
- Include useful tooltips without hiding essential comparisons.
- Keep the synthetic-data disclaimer visible.

## 6. Validation checklist

Before publishing, confirm:
- [ ] Unfiltered revenue = 558,057.39.
- [ ] Unfiltered cost = 343,858.98.
- [ ] Unfiltered profit = 214,198.41.
- [ ] Unfiltered margin = 38.38%.
- [ ] Distinct orders = 1,200 and units sold = 5,155.
- [ ] Monthly revenue totals 558,057.39.
- [ ] Monthly profit totals 214,198.41.
- [ ] Regional, category, segment, and product revenue each reconcile to 558,057.39.
- [ ] Regional, category, segment, and product profit each reconcile to 214,198.41.
- [ ] All filters update KPIs and charts consistently.
- [ ] Resetting filters restores unfiltered values.
- [ ] No invented currency symbol appears.
- [ ] Synthetic-data and simulated-seasonality disclaimers remain visible.

## 7. Publishing and portfolio presentation

Publish to Tableau Public only after the validation checklist passes. Add the public Tableau URL and a dashboard screenshot to the project README after publication. Do not claim that a Tableau dashboard is published until the public workbook link has been checked.
