"""Generate the deterministic synthetic retail dataset.

Run from the repository root:
    python python/generate_sales_data.py

The generator intentionally uses a small linear-congruential PRNG so the
committed CSV can be reproduced without external data or random packages.
All entities and transactions are fictional.
"""
from __future__ import annotations

import csv
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FILE = ROOT / "datasets" / "sales_data.csv"

SEED = 20261121
PRODUCTS = [
    ("Wireless Mouse", "Electronics", 25, 10),
    ("Keyboard", "Electronics", 45, 18),
    ("Monitor", "Electronics", 210, 145),
    ("Laptop Stand", "Electronics", 68, 37),
    ("USB-C Hub", "Electronics", 52, 27),
    ("Desk", "Furniture", 320, 210),
    ("Office Chair", "Furniture", 180, 110),
    ("Bookshelf", "Furniture", 240, 150),
    ("Notebook Pack", "Office Supplies", 6, 2),
    ("Printer Paper Box", "Office Supplies", 28, 16),
    ("Ink Cartridge", "Office Supplies", 42, 24),
    ("Desk Organizer", "Office Supplies", 19, 8),
]
REGIONS = ["North", "South", "East", "West"]
SALES_REPS = ["Ada", "Daniel", "Maya", "Noah", "Grace", "Ethan", "Zara", "Liam"]
SEGMENTS = ["Consumer", "Corporate", "Small Business"]
FIELDS = [
    "order_id", "order_date", "region", "sales_rep", "customer_segment",
    "category", "product", "quantity", "unit_price", "unit_cost",
]


class DeterministicRandom:
    """32-bit LCG matching the committed dataset generation sequence."""

    def __init__(self, seed: int) -> None:
        self.state = seed

    def random(self) -> float:
        self.state = (self.state * 1664525 + 1013904223) & 0xFFFFFFFF
        return self.state / 4294967296

    def choice(self, values):
        return values[int(self.random() * len(values))]


def generate_rows():
    rng = DeterministicRandom(SEED)
    order_number = 0
    for year in (2024, 2025):
        for month in range(1, 13):
            for _ in range(50):
                order_number += 1
                order_date = date(year, month, 1) + timedelta(days=int(rng.random() * 28))
                region = rng.choice(REGIONS)
                sales_rep = rng.choice(SALES_REPS)
                segment_roll = rng.random()
                if segment_roll < 0.30:
                    segment = "Consumer"
                elif segment_roll < 0.65:
                    segment = "Corporate"
                else:
                    segment = "Small Business"
                product, category, base_price, base_cost = rng.choice(PRODUCTS)
                seasonal = 1.28 if month in (11, 12) else (0.86 if month == 1 else 1.0)
                segment_multiplier = (
                    1.45 if segment == "Corporate"
                    else 1.15 if segment == "Small Business"
                    else 0.90
                )
                quantity = max(
                    1,
                    min(18, round((1 + rng.random() * 5) * seasonal * segment_multiplier)),
                )
                unit_price = round(base_price * (0.96 + rng.random() * 0.08) + 1e-10, 2)
                unit_cost = round(base_cost * (0.97 + rng.random() * 0.06) + 1e-10, 2)
                yield [
                    f"ORD-{20000 + order_number:05d}",
                    order_date.isoformat(),
                    region,
                    sales_rep,
                    segment,
                    category,
                    product,
                    quantity,
                    f"{unit_price:.2f}",
                    f"{unit_cost:.2f}",
                ]


def main() -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(FIELDS)
        writer.writerows(generate_rows())
    print(f"Generated 1,200 synthetic order lines: {OUTPUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
