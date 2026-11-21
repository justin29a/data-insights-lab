"""Unit tests for the Sales Performance Intelligence analysis functions.

Run from the repository root:
    python -m unittest discover -s tests -v
"""
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from python.analyze_sales import add_metrics, build_kpis, load_data, summarize


VALID_CSV = """order_id,order_date,region,sales_rep,customer_segment,category,product,quantity,unit_price,unit_cost
A-1,2025-01-05,North,Ada,Consumer,Electronics,Mouse,2,25,10
A-2,2025-01-06,South,Bo,Corporate,Furniture,Chair,1,100,60
"""


class SalesAnalysisTests(unittest.TestCase):
    def load_csv(self, content):
        handle = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", encoding="utf-8", delete=False)
        try:
            handle.write(content)
            handle.close()
            return load_data(Path(handle.name))
        finally:
            Path(handle.name).unlink(missing_ok=True)

    def test_metrics_and_executive_kpis(self):
        df = add_metrics(self.load_csv(VALID_CSV))
        kpi = build_kpis(df).iloc[0]
        self.assertEqual(kpi["records"], 2)
        self.assertEqual(kpi["orders"], 2)
        self.assertEqual(kpi["units_sold"], 3)
        self.assertEqual(kpi["revenue"], 150)
        self.assertEqual(kpi["cost"], 80)
        self.assertEqual(kpi["profit"], 70)
        self.assertAlmostEqual(kpi["profit_margin_pct"], 46.6666667, places=5)
        self.assertEqual(kpi["average_order_value"], 75)

    def test_monthly_summary_is_chronological(self):
        df = add_metrics(self.load_csv(VALID_CSV))
        result = summarize(df, "sales_month")
        self.assertEqual(result["sales_month"].tolist(), ["2025-01"])
        self.assertEqual(result.iloc[0]["revenue"], 150)
        self.assertEqual(result.iloc[0]["profit"], 70)

    def test_missing_required_column_is_rejected(self):
        broken = VALID_CSV.replace(",unit_cost", "")
        with self.assertRaisesRegex(ValueError, "Missing required columns"):
            self.load_csv(broken)

    def test_invalid_date_is_rejected(self):
        broken = VALID_CSV.replace("2025-01-05", "not-a-date")
        with self.assertRaisesRegex(ValueError, "order_date"):
            self.load_csv(broken)

    def test_non_positive_quantity_is_rejected(self):
        broken = VALID_CSV.replace(",2,25,10", ",0,25,10")
        with self.assertRaisesRegex(ValueError, "Quantity"):
            self.load_csv(broken)

    def test_negative_price_is_rejected(self):
        broken = VALID_CSV.replace(",2,25,10", ",2,-25,10")
        with self.assertRaisesRegex(ValueError, "cannot be negative"):
            self.load_csv(broken)

    def test_blank_dimension_is_rejected(self):
        broken = VALID_CSV.replace("North,Ada", ",Ada")
        with self.assertRaisesRegex(ValueError, "region"):
            self.load_csv(broken)

    def test_infinite_numeric_value_is_rejected(self):
        broken = VALID_CSV.replace(",2,25,10", ",2,inf,10")
        with self.assertRaisesRegex(ValueError, "Infinite"):
            self.load_csv(broken)


if __name__ == "__main__":
    unittest.main()
