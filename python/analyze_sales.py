"""Sales Performance Intelligence — reproducible pandas analysis.

Run from the repository root:
    python -m pip install -r requirements.txt
    python python/analyze_sales.py

The source dataset is synthetic and uses unspecified currency units.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "datasets" / "sales_data.csv"

REQUIRED_COLUMNS = {
    "order_id", "order_date", "region", "sales_rep",
    "customer_segment", "category", "product",
    "quantity", "unit_price", "unit_cost",
}


def load_data(path: Path) -> pd.DataFrame:
    """Load the CSV and validate required fields and basic data quality."""
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    numeric_columns = ["quantity", "unit_price", "unit_cost"]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    if df["order_date"].isna().any():
        raise ValueError("Invalid or missing order_date values detected.")
    if df[numeric_columns].isna().any().any():
        raise ValueError("Missing or non-numeric quantity, unit_price, or unit_cost.")
    if (df["quantity"] <= 0).any():
        raise ValueError("Quantity must be greater than zero.")
    if (df[["unit_price", "unit_cost"]] < 0).any().any():
        raise ValueError("Unit price and unit cost cannot be negative.")
    if df["order_id"].isna().any() or df["order_id"].astype(str).str.strip().eq("").any():
        raise ValueError("Missing or blank order_id values detected.")

    return df


def add_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Create transaction-level metrics used throughout the analysis."""
    result = df.copy()
    result["revenue"] = result["quantity"] * result["unit_price"]
    result["cost"] = result["quantity"] * result["unit_cost"]
    result["profit"] = result["revenue"] - result["cost"]
    result["sales_month"] = result["order_date"].dt.to_period("M").astype(str)
    return result


def summarize(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    """Aggregate revenue, cost, profit, units, and orders by a dimension."""
    summary = (
        df.groupby(dimension, dropna=False)
        .agg(
            revenue=("revenue", "sum"),
            cost=("cost", "sum"),
            profit=("profit", "sum"),
            units_sold=("quantity", "sum"),
            orders=("order_id", "nunique"),
        )
        .reset_index()
    )
    summary["profit_margin_pct"] = (
        summary["profit"].div(summary["revenue"].where(summary["revenue"].ne(0)))
        .mul(100)
    )
    return summary.sort_values("revenue", ascending=False)


def main() -> None:
    raw = load_data(DATA_FILE)
    df = add_metrics(raw)

    total_revenue = df["revenue"].sum()
    total_cost = df["cost"].sum()
    total_profit = df["profit"].sum()
    margin = (total_profit / total_revenue * 100) if total_revenue else float("nan")

    print("\nSALES PERFORMANCE — OVERALL KPIs")
    print("--------------------------------")
    print(f"Rows: {len(df):,}")
    print(f"Orders: {df['order_id'].nunique():,}")
    print(f"Units sold: {df['quantity'].sum():,.0f}")
    print(f"Revenue: {total_revenue:,.2f}")
    print(f"Cost: {total_cost:,.2f}")
    print(f"Profit: {total_profit:,.2f}")
    print(f"Profit margin: {margin:,.2f}%")
    print("\nNote: currency is unspecified; dataset is synthetic.")

    for dimension, heading in [
        ("sales_month", "MONTHLY PERFORMANCE"),
        ("region", "PERFORMANCE BY REGION"),
        ("category", "PERFORMANCE BY CATEGORY"),
        ("customer_segment", "PERFORMANCE BY CUSTOMER SEGMENT"),
        ("product", "PRODUCT PERFORMANCE"),
    ]:
        print(f"\n{heading}")
        print("-" * len(heading))
        print(summarize(df, dimension).to_string(index=False, float_format=lambda x: f"{x:,.2f}"))


if __name__ == "__main__":
    main()
