"""Integration tests for the actual SQLite analysis script.

Run from the repository root:
    python -m unittest discover -s tests -v
"""
import csv
import sqlite3
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "datasets" / "sales_data.csv"
SQL_FILE = ROOT / "sql" / "sales_analysis.sql"


def execute_script_statements(connection, script):
    """Execute statements one at a time and return each SELECT result."""
    results = []
    statement = ""
    for line in script.splitlines():
        statement += line + "\n"
        if sqlite3.complete_statement(statement):
            sql = statement.strip()
            statement = ""
            if not sql or sql.startswith("--"):
                continue
            cursor = connection.execute(sql)
            if cursor.description:
                results.append((tuple(c[0] for c in cursor.description), cursor.fetchall()))
    if statement.strip():
        raise AssertionError(f"Incomplete SQL statement at end of script: {statement}")
    return results


class SalesSQLIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection = sqlite3.connect(":memory:")
        with DATASET.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        columns = list(rows[0])
        definitions = {
            "order_id": "TEXT", "order_date": "TEXT", "region": "TEXT",
            "sales_rep": "TEXT", "customer_segment": "TEXT", "category": "TEXT",
            "product": "TEXT", "quantity": "INTEGER", "unit_price": "REAL",
            "unit_cost": "REAL",
        }
        schema = ", ".join(f'"{c}" {definitions[c]}' for c in columns)
        cls.connection.execute(f"CREATE TABLE sales_data ({schema})")
        placeholders = ", ".join("?" for _ in columns)
        cls.connection.executemany(
            f"INSERT INTO sales_data VALUES ({placeholders})",
            [[row[c] for c in columns] for row in rows],
        )
        script = SQL_FILE.read_text(encoding="utf-8")
        cls.results = execute_script_statements(cls.connection, script)

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def test_script_executes_all_select_statements(self):
        # Includes sample, coverage, KPI, five grouped reports, and data quality.
        self.assertEqual(len(self.results), 9)

    def test_sql_executive_kpis_reconcile_to_dataset(self):
        columns, rows = self.results[2]
        kpi = dict(zip(columns, rows[0]))
        self.assertEqual(kpi["records"], 1200)
        self.assertEqual(kpi["orders"], 1200)
        self.assertEqual(kpi["units_sold"], 5155)
        self.assertAlmostEqual(kpi["revenue"], 558057.39, places=2)
        self.assertAlmostEqual(kpi["cost"], 343858.98, places=2)
        self.assertAlmostEqual(kpi["profit"], 214198.41, places=2)
        self.assertAlmostEqual(kpi["profit_margin_pct"], 38.38, places=2)
        self.assertAlmostEqual(kpi["average_order_value"], 465.05, places=2)

    def test_sql_monthly_summary_has_24_chronological_months(self):
        columns, rows = self.results[3]
        months = [row[0] for row in rows]
        self.assertEqual(len(months), 24)
        self.assertEqual(months, sorted(months))
        self.assertEqual(sum(row[1] for row in rows), 558057.39)

    def test_sql_dimension_summaries_reconcile_to_total_revenue_and_profit(self):
        for columns, rows in self.results[4:8]:
            revenue_index = columns.index("revenue")
            profit_index = columns.index("profit")
            self.assertAlmostEqual(sum(row[revenue_index] for row in rows), 558057.39, places=2)
            self.assertAlmostEqual(sum(row[profit_index] for row in rows), 214198.41, places=2)

    def test_sql_data_quality_checks_report_no_invalid_values(self):
        columns, rows = self.results[8]
        checks = dict(zip(columns, rows[0]))
        self.assertTrue(all(value == 0 for value in checks.values()))


if __name__ == "__main__":
    unittest.main()
