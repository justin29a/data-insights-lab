# Data Dictionary — Sales Performance Intelligence

## Dataset overview

- **File:** `datasets/sales_data.csv`
- **Grain:** One row represents one order line in this demonstration dataset.
- **Period:** January–June 2025.
- **Records:** 24 synthetic rows.
- **Currency:** Unspecified currency units.
- **Provenance:** Artificially created for this portfolio project; not real business data.

## Source fields

| Field | Type | Description |
|---|---|---|
| `order_id` | Text | Unique order identifier in this sample |
| `order_date` | Date (YYYY-MM-DD) | Date the order was placed |
| `region` | Text | Sales region: North, South, East, or West |
| `sales_rep` | Text | Fictional sales representative |
| `customer_segment` | Text | Consumer, Corporate, or Small Business |
| `category` | Text | Product category |
| `product` | Text | Product name |
| `quantity` | Integer | Number of units in the order line |
| `unit_price` | Decimal | Selling price per unit |
| `unit_cost` | Decimal | Cost per unit |

## Derived measures

| Measure | Calculation |
|---|---|
| Revenue | `quantity * unit_price` |
| Cost | `quantity * unit_cost` |
| Profit | `revenue - cost` |
| Profit margin (%) | `profit / revenue * 100` |
| Sales month | Month extracted from `order_date` |
| Orders | Count of distinct `order_id` values |
| Units sold | Sum of `quantity` |

## Assumptions and limitations

1. Each row is treated as a separate order line; the sample currently has one line per order.
2. Unit prices and costs are assumed to be constant for each row.
3. Taxes, discounts, shipping, returns, refunds, and operating expenses are not represented.
4. Currency is intentionally unspecified.
5. The dataset is small and synthetic. It is suitable for demonstrating analysis techniques, not forecasting or making real commercial decisions.
6. A zero-revenue group should have an undefined margin rather than a division-by-zero result.
