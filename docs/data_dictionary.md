# Data Dictionary — Sales Performance Intelligence

## Dataset overview

- **File:** `datasets/sales_data.csv`
- **Grain:** One row represents one order line; this generated release contains one line per order.
- **Period:** January 2024–December 2025 (24 months).
- **Records:** 1,200 synthetic order lines across 1,200 distinct orders.
- **Currency:** Unspecified currency units.
- **Provenance:** Artificially generated with a fixed seed for reproducibility; not real business data.
- **Generator:** `python/generate_sales_data.py`.

## Source fields

| Field | Type | Description |
|---|---|---|
| `order_id` | Text | Unique synthetic order identifier |
| `order_date` | Date (YYYY-MM-DD) | Date the order was placed |
| `region` | Text | North, South, East, or West |
| `sales_rep` | Text | One of eight fictional sales representatives |
| `customer_segment` | Text | Consumer, Corporate, or Small Business |
| `category` | Text | Electronics, Furniture, or Office Supplies |
| `product` | Text | One of twelve fictional catalog product names |
| `quantity` | Integer | Number of units in the order line |
| `unit_price` | Decimal | Selling price per unit, with small generated variation |
| `unit_cost` | Decimal | Cost per unit, with small generated variation |

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
| Average order value | Revenue divided by distinct orders |

## Generation design and limitations

1. The dataset is synthetic and deterministic: the generator uses a fixed seed and a documented pseudo-random number sequence.
2. The generator creates 50 orders per month for 24 months. Each order has one order line; multi-line baskets are not modeled in this release.
3. Product mix, customer segments, order quantities, unit prices, and unit costs are generated from controlled ranges. Seasonal multipliers introduce variation but do not represent measured real-world seasonality.
4. Taxes, discounts, shipping, returns, refunds, operating expenses, inventory, customer-level identifiers, and payment data are not represented.
5. Currency is intentionally unspecified.
6. This dataset is suitable for demonstrating data cleaning, aggregation, visualization, and reproducible analysis. It must not be used to make claims about an actual retailer or to train a production forecasting model.
7. A zero-revenue group should have an undefined margin rather than a division-by-zero result.
