# Tableau Executive Dashboard Blueprint

## Objective

Build a portfolio-quality Tableau dashboard that answers five management questions:

1. How much revenue and profit did the fictional retailer generate?
2. How did revenue and profit move across the six-month period?
3. Which regions and categories contribute most to revenue and profit?
4. Which products combine strong sales with strong profitability?
5. How do customer segments compare?

**Source:** `datasets/sales_data.csv`  
**Period:** 1 January–27 June 2025  
**Data status:** Entirely synthetic; all monetary values are unspecified currency units.

## 1. Connect and prepare the data

Connect Tableau to the raw `sales_data.csv` file. Use the raw transaction-level file as the dashboard's single source. Do not use the pre-aggregated output CSVs as the primary source for an interactive dashboard: doing so can prevent filters and calculations from behaving consistently at transaction level.

Confirm the data types:
- `order_date`: Date
- `quantity`, `unit_price`, `unit_cost`: Number (whole or decimal as appropriate)
- IDs and descriptive fields: String

No currency symbol should be applied because the scenario does not specify a currency.

## 2. Create calculated fields

Create these calculated fields in Tableau:

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

Use a fixed desktop canvas of approximately **1440 × 900 px**. Keep a consistent grid, restrained typography, and clear spacing. Use a light neutral background with a dark navy header; reserve accent colors for meaningful comparisons.

### Header
- Title: **Sales Performance Intelligence**
- Subtitle: *Executive overview | January–June 2025*
- Small visible note: *Synthetic demonstration dataset · Currency unspecified*

### KPI row
Five KPI cards:
1. Revenue
2. Profit
3. Profit Margin
4. Orders
5. Units Sold

Expected unfiltered values:
- Revenue: 6,241
- Profit: 2,577
- Profit Margin: 41.29%
- Orders: 24
- Units Sold: 108

### Main analysis area

**Worksheet A — Monthly Performance**
- Columns: Sales Month
- Rows: Revenue and Profit
- Marks: Line
- Show month labels in chronological order.
- Tooltip: revenue, cost, profit, margin, orders, units.

**Worksheet B — Regional Performance**
- Rows: Region
- Columns: Revenue
- Marks: Horizontal bars.
- Sort descending by revenue.
- Tooltip: revenue, profit, margin, orders, units.
- Make profit and margin visible in the tooltip so revenue ranking does not hide profitability differences.

**Worksheet C — Category Performance**
- Rows: Category
- Columns: Revenue
- Show profit and margin in tooltip or a clearly labelled companion measure.
- Sort descending by revenue.

**Worksheet D — Product Performance**
- Scatter plot:
  - X-axis: Revenue
  - Y-axis: Profit
  - Size: Units Sold
  - Label: Product
  - Tooltip: revenue, cost, profit, margin, units, orders.
- This helps distinguish high-revenue products from high-margin or high-profit products.

**Worksheet E — Customer Segment Performance**
- Rows: Customer Segment
- Columns: Revenue
- Tooltip: profit, margin, orders, units, average order value.
- Sort descending by revenue.

## 4. Filters and dashboard actions

Add these dashboard filters:
- Order Date (range)
- Region
- Category
- Customer Segment

Apply each filter to all relevant worksheets using the same data source.

Add a dashboard filter action so selecting a region, category, or segment in a chart filters the other views. Provide a clear way to reset selections.

Keep the KPI cards connected to the same filters. Validate that selecting a single region changes all five KPI values and every relevant chart consistently.

## 5. Design and usability standards

- Use descriptive chart titles rather than generic labels such as “Sheet 1”.
- Use consistent number formatting and two decimal places for percentages.
- Avoid 3D charts, excessive gridlines, decorative gauges, and unnecessary legends.
- Do not encode every measure with a different color.
- Keep labels readable at the full dashboard size.
- Include useful tooltips, but do not use tooltips as a substitute for essential comparisons.
- Add a footer explaining that the dataset is synthetic and does not represent actual business performance.

## 6. Validation checklist

Before publishing, confirm:

- [ ] Unfiltered KPI cards match the expected figures above.
- [ ] Monthly revenue totals 6,241.
- [ ] Monthly profit totals 2,577.
- [ ] Regional revenue totals 6,241.
- [ ] Category revenue totals 6,241.
- [ ] Customer-segment revenue totals 6,241.
- [ ] Product revenue totals 6,241.
- [ ] Regional profit totals 2,577.
- [ ] Category profit totals 2,577.
- [ ] Product profit totals 2,577.
- [ ] All dashboard filters update KPIs and charts consistently.
- [ ] Resetting filters restores the expected unfiltered values.
- [ ] Currency is not misrepresented with an invented symbol.
- [ ] The synthetic-data disclaimer remains visible.

## 7. Publishing and portfolio presentation

Publish to Tableau Public only after the validation checklist passes. Use a clear workbook title and a short project description. Add the public Tableau URL and a dashboard screenshot to the project README after publication.

Do not claim that a Tableau dashboard is published until the public workbook link has been checked.
