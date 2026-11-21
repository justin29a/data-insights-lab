"""Sales Performance Intelligence — reproducible pandas analysis.

Run from the repository root:
    python -m pip install -r requirements.txt
    python python/analyze_sales.py

The script validates the input, calculates business metrics, prints summaries,
and writes analysis tables to outputs/. Source data is synthetic.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "datasets" / "sales_data.csv"
OUTPUT_DIR = ROOT / "outputs"

REQUIRED_COLUMNS = {
    "order_id", "order_date", "region", "sales_rep",
    "customer_segment", "category", "product",
    "quantity", "unit_price", "unit_cost",
}
DIMENSION_COLUMNS = [
    "region", "sales_rep", "customer_segment", "category", "product"
]
NUMERIC_COLUMNS = ["quantity", "unit_price", "unit_cost"]


def load_data(path: Path) -> pd.DataFrame:
    """Load the CSV and fail early when required fields are incomplete or invalid."""
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    if df.empty:
        raise ValueError("The dataset contains no records.")
    if df["order_date"].isna().any():
        raise ValueError("Invalid or missing order_date values detected.")
    if df[NUMERIC_COLUMNS].isna().any().any():
        raise ValueError("Missing or non-numeric quantity, unit_price, or unit_cost.")
    if df[NUMERIC_COLUMNS].isin([float("inf"), float("-inf")]).any().any():
        raise ValueError("Infinite quantity, unit_price, or unit_cost values detected.")
    if (df["quantity"] <= 0).any():
        raise ValueError("Quantity must be greater than zero.")
    if (df[["unit_price", "unit_cost"]] < 0).any().any():
        raise ValueError("Unit price and unit cost cannot be negative.")
    if df["order_id"].isna().any() or df["order_id"].astype(str).str.strip().eq("").any():
        raise ValueError("Missing or blank order_id values detected.")
    for column in DIMENSION_COLUMNS:
        if df[column].isna().any() or df[column].astype(str).str.strip().eq("").any():
            raise ValueError(f"Missing or blank values detected in {column}.")

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
    """Aggregate revenue, cost, profit, units, orders, and margin by a dimension."""
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
    if dimension == "sales_month":
        return summary.sort_values(dimension)
    return summary.sort_values(["revenue", dimension], ascending=[False, True])


def build_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Return one-row executive KPI table."""
    revenue = df["revenue"].sum()
    profit = df["profit"].sum()
    orders = df["order_id"].nunique()
    return pd.DataFrame([{
        "records": len(df),
        "orders": orders,
        "units_sold": df["quantity"].sum(),
        "revenue": revenue,
        "cost": df["cost"].sum(),
        "profit": profit,
        "profit_margin_pct": profit / revenue * 100 if revenue else float("nan"),
        "average_order_value": revenue / orders if orders else float("nan"),
        "data_start_date": df["order_date"].min().date().isoformat(),
        "data_end_date": df["order_date"].max().date().isoformat(),
    }])


def write_outputs(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Write clean CSV outputs for Excel, Tableau, and further analysis."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tables = {
        "kpi_summary": build_kpis(df),
        "monthly_performance": summarize(df, "sales_month"),
        "region_performance": summarize(df, "region"),
        "category_performance": summarize(df, "category"),
        "segment_performance": summarize(df, "customer_segment"),
        "product_performance": summarize(df, "product"),
    }
    for name, table in tables.items():
        table.to_csv(OUTPUT_DIR / f"{name}.csv", index=False)
    return tables


def main() -> None:
    raw = load_data(DATA_FILE)
    df = add_metrics(raw)
    tables = write_outputs(df)

    print("\nSALES PERFORMANCE — EXECUTIVE KPIs")
    print("---------------------------------")
    print(tables["kpi_summary"].to_string(index=False, float_format=lambda x: f"{x:,.2f}"))
    print("\nNote: currency is unspecified; all source records are synthetic.")

    for key, heading in [
        ("monthly_performance", "MONTHLY PERFORMANCE"),
        ("region_performance", "PERFORMANCE BY REGION"),
        ("category_performance", "PERFORMANCE BY CATEGORY"),
        ("segment_performance", "PERFORMANCE BY CUSTOMER SEGMENT"),
        ("product_performance", "PRODUCT PERFORMANCE"),
    ]:
        print(f"\n{heading}")
        print("-" * len(heading))
        print(tables[key].to_string(index=False, float_format=lambda x: f"{x:,.2f}"))

    print(f"\nSaved {len(tables)} analysis tables to: {OUTPUT_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
