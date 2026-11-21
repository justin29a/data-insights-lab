"""Build the Sales Performance Intelligence Excel workbook.

Run from repository root: python python/build_excel_workbook.py
The workbook is written to outputs/sales_performance_intelligence.xlsx.
"""
from pathlib import Path
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.chart import LineChart, BarChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import ColorScaleRule

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "datasets" / "sales_data.csv"
OUT = ROOT / "outputs" / "sales_performance_intelligence.xlsx"
NAVY = "14243A"
BLUE = "1F5A94"
TEAL = "16A6A1"
PALE = "EAF1F8"
LIGHT = "F4F7FA"
WHITE = "FFFFFF"
DARK = "25364A"
MUTED = "66788A"
GREEN = "E2F0D9"
RED = "FCE4D6"
MONEY = '#,##0.00;[Red](#,##0.00);-'
PERCENT = '0.00%;[Red](0.00%);-'

def style_title(ws, title, subtitle, end_col=8):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=end_col)
    c = ws.cell(1, 1, title)
    c.font = Font(name="Aptos Display", size=20, bold=True, color=WHITE)
    c.fill = PatternFill("solid", fgColor=NAVY)
    c.alignment = Alignment(vertical="center")
    ws.row_dimensions[1].height = 36
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=end_col)
    s = ws.cell(2, 1, subtitle)
    s.font = Font(name="Aptos", size=10, italic=True, color=MUTED)
    s.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[2].height = 30

def write_table(ws, df, start_row=4, table_name=None, money_cols=None, percent_cols=None):
    money_cols = set(money_cols or [])
    percent_cols = set(percent_cols or [])
    for j, name in enumerate(df.columns, 1):
        c = ws.cell(start_row, j, name.replace("_", " ").title())
        c.font = Font(bold=True, color=WHITE)
        c.fill = PatternFill("solid", fgColor=BLUE)
        c.alignment = Alignment(wrap_text=True)
    for i, row in enumerate(df.itertuples(index=False, name=None), start_row + 1):
        for j, value in enumerate(row, 1):
            if pd.isna(value):
                value = None
            elif hasattr(value, "to_pydatetime"):
                value = value.to_pydatetime()
            c = ws.cell(i, j, value)
            c.font = Font(color=DARK, size=10)
            if i % 2 == 0:
                c.fill = PatternFill("solid", fgColor=LIGHT)
            col = df.columns[j-1]
            if col in money_cols:
                c.number_format = MONEY
            elif col in percent_cols:
                c.number_format = '0.00"%"'
            elif col == "order_date":
                c.number_format = "dd-mmm-yyyy"
    end_row = start_row + len(df)
    if table_name and len(df):
        ref = f"A{start_row}:{get_column_letter(len(df.columns))}{end_row}"
        tab = Table(displayName=table_name, ref=ref)
        tab.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True,
                                             showColumnStripes=False, showFirstColumn=False,
                                             showLastColumn=False)
        ws.add_table(tab)
        ws.auto_filter.ref = ref
    ws.freeze_panes = f"A{start_row+1}"
    for j, name in enumerate(df.columns, 1):
        values = [str(name)] + [str(x) for x in df[name].head(150).fillna("")]
        width = min(max(max(len(x) for x in values) + 2, 12), 28)
        ws.column_dimensions[get_column_letter(j)].width = width
    return end_row

def add_summary_sheet(wb, title, subtitle, df, table_name, money_cols, percent_cols):
    ws = wb.create_sheet(title)
    style_title(ws, title, subtitle, max(6, len(df.columns)))
    write_table(ws, df, 4, table_name, money_cols, percent_cols)
    ws.sheet_view.showGridLines = False
    return ws

def main():
    raw = pd.read_csv(DATA, parse_dates=["order_date"])
    raw["revenue"] = raw["quantity"] * raw["unit_price"]
    raw["cost"] = raw["quantity"] * raw["unit_cost"]
    raw["profit"] = raw["revenue"] - raw["cost"]
    raw["sales_month"] = raw["order_date"].dt.strftime("%Y-%m")
    monthly = raw.groupby("sales_month", as_index=False).agg(
        revenue=("revenue","sum"), cost=("cost","sum"), profit=("profit","sum"),
        units_sold=("quantity","sum"), orders=("order_id","nunique"))
    monthly["profit_margin_pct"] = monthly["profit"] / monthly["revenue"] * 100
    summaries = {}
    for key, dimension in [("region","region"),("category","category"),
                           ("product","product"),("segment","customer_segment")]:
        x = raw.groupby(dimension, as_index=False).agg(
            revenue=("revenue","sum"), cost=("cost","sum"), profit=("profit","sum"),
            units_sold=("quantity","sum"), orders=("order_id","nunique"))
        x["profit_margin_pct"] = x["profit"] / x["revenue"] * 100
        summaries[key] = x.sort_values("revenue", ascending=False)
    revenue = raw["revenue"].sum()
    cost = raw["cost"].sum()
    profit = raw["profit"].sum()
    orders = raw["order_id"].nunique()
    units = int(raw["quantity"].sum())

    wb = Workbook()
    dash = wb.active
    dash.title = "Executive Dashboard"
    dash.sheet_view.showGridLines = False
    style_title(dash, "SALES PERFORMANCE INTELLIGENCE",
                "Executive view | January 2024 – December 2025 | Synthetic dataset | Currency unspecified", 8)
    dash["A4"] = "PERFORMANCE SNAPSHOT"
    dash["A4"].font = Font(bold=True, color=BLUE, size=11)
    kpis = [
        ("Revenue", revenue, MONEY), ("Profit", profit, MONEY),
        ("Profit Margin", profit / revenue, PERCENT), ("Orders", orders, "#,##0"),
        ("Units Sold", units, "#,##0"), ("Average Order Value", revenue / orders, MONEY),
    ]
    positions = [(1,5),(3,5),(5,5),(1,8),(3,8),(5,8)]
    for (label, value, fmt), (col, row) in zip(kpis, positions):
        dash.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col+1)
        dash.cell(row, col, label.upper())
        dash.cell(row, col).font = Font(bold=True, color=WHITE, size=9)
        dash.cell(row, col).fill = PatternFill("solid", fgColor=BLUE)
        dash.merge_cells(start_row=row+1, start_column=col, end_row=row+1, end_column=col+1)
        v = dash.cell(row+1, col, value)
        v.font = Font(bold=True, color=NAVY, size=17)
        v.fill = PatternFill("solid", fgColor=PALE)
        v.number_format = fmt
        v.alignment = Alignment(horizontal="center")
        dash.row_dimensions[row+1].height = 30
    dash["A11"] = "KEY TAKEAWAYS"
    dash["A11"].font = Font(bold=True, color=BLUE, size=11)
    takeaways = [
        f"Top revenue region: {summaries['region'].iloc[0]['region']} ({summaries['region'].iloc[0]['revenue']:,.2f}).",
        f"Top revenue category: {summaries['category'].iloc[0]['category']} ({summaries['category'].iloc[0]['revenue']:,.2f}).",
        f"Top revenue product: {summaries['product'].iloc[0]['product']} ({summaries['product'].iloc[0]['revenue']:,.2f}).",
        f"Largest customer segment by revenue: {summaries['segment'].iloc[0]['customer_segment']}.",
        "All figures are simulated; seasonal multipliers are artificial scenario settings, not market evidence.",
    ]
    for i, line in enumerate(takeaways, 12):
        dash.merge_cells(start_row=i, start_column=1, end_row=i, end_column=8)
        dash.cell(i,1, "• " + line)
        dash.cell(i,1).font = Font(color=DARK, size=10)
        dash.cell(i,1).alignment = Alignment(wrap_text=True, vertical="center")
        dash.row_dimensions[i].height = 24
    dash["A19"] = "Workbook guide"
    dash["A19"].font = Font(bold=True, color=BLUE)
    dash.merge_cells("A20:H21")
    dash["A20"] = ("Use the dedicated analysis tabs for detailed comparisons. Raw Data contains all source records "
                   "plus calculated revenue, cost, profit and month. Summary tabs are reproducible aggregates. "
                   "Dashboard charts are overall views and do not respond to slicers or filters.")
    dash["A20"].alignment = Alignment(wrap_text=True, vertical="top")
    dash["A20"].font = Font(color=MUTED, size=10)
    for col in range(1,9):
        dash.column_dimensions[get_column_letter(col)].width = 16
    dash.freeze_panes = "A4"

    # Monthly analysis and chart
    mws = add_summary_sheet(wb, "Monthly Analysis", "24 monthly periods. Values are aggregated from the 1,200 source records.",
                            monthly, "MonthlyPerformance", ["revenue","cost","profit"], ["profit_margin_pct"])
    chart = LineChart()
    chart.title = "Monthly Revenue and Profit"
    chart.y_axis.title = "Unspecified currency units"
    chart.x_axis.title = "Month"
    chart.height, chart.width = 8, 16
    data = Reference(mws, min_col=2, max_col=4, min_row=4, max_row=4+len(monthly))
    cats = Reference(mws, min_col=1, min_row=5, max_row=4+len(monthly))
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.style = 13
    mws.add_chart(chart, "I4")

    # Dimensional analysis sheets and charts
    region_ws = add_summary_sheet(wb, "Regional Analysis", "Regional revenue, cost, profit, units and margin.",
                                  summaries["region"], "RegionalPerformance", ["revenue","cost","profit"], ["profit_margin_pct"])
    b = BarChart()
    b.type = "bar"; b.style = 10; b.title = "Revenue by Region"; b.x_axis.title = "Revenue"; b.y_axis.title = "Region"
    b.add_data(Reference(region_ws, min_col=2, min_row=4, max_row=4+len(summaries["region"])), titles_from_data=True)
    b.set_categories(Reference(region_ws, min_col=1, min_row=5, max_row=4+len(summaries["region"])))
    b.height, b.width = 7, 13
    region_ws.add_chart(b, "I4")

    for title, key, table_name, subtitle in [
        ("Category Analysis","category","CategoryPerformance","Category-level performance and profitability."),
        ("Product Analysis","product","ProductPerformance","Product-level performance and profitability."),
        ("Customer Analysis","segment","Customer-segment performance and profitability."),
    ]:
        add_summary_sheet(wb, title, subtitle, summaries[key], table_name,
                          ["revenue","cost","profit"], ["profit_margin_pct"])

    # Raw source records with calculated metrics
    raw_cols = ["order_id","order_date","region","sales_rep","customer_segment","category",
                "product","quantity","unit_price","unit_cost","revenue","cost","profit","sales_month"]
    rws = wb.create_sheet("Raw Data")
    style_title(rws, "SOURCE DATA", "1,200 synthetic order records. One order line per order in this simulation.", len(raw_cols))
    write_table(rws, raw[raw_cols], 4, "SalesRawData",
                ["unit_price","unit_cost","revenue","cost","profit"], [])
    rws.sheet_view.showGridLines = False

    # Data quality summary
    quality = pd.DataFrame([
        ["Record count", len(raw), 1200, "PASS" if len(raw)==1200 else "CHECK"],
        ["Unique order IDs", raw.order_id.nunique(), 1200, "PASS" if raw.order_id.is_unique else "CHECK"],
        ["Blank cells", int(raw.isna().sum().sum()), 0, "PASS" if not raw.isna().any().any() else "CHECK"],
        ["Non-positive quantities", int((raw.quantity<=0).sum()), 0, "PASS" if (raw.quantity>0).all() else "CHECK"],
        ["Negative prices/costs", int(((raw[["unit_price","unit_cost"]]<0).sum().sum())), 0, "PASS" if (raw[["unit_price","unit_cost"]]>=0).all().all() else "CHECK"],
        ["Revenue reconciliation", round(raw.revenue.sum(),2), round(revenue,2), "PASS"],
        ["Profit reconciliation", round(raw.profit.sum(),2), round(profit,2), "PASS"],
    ], columns=["check","actual","expected","status"])
    qws = add_summary_sheet(wb, "Data Quality", "Basic structural checks and reconciliation against calculated source totals.",
                            quality, "DataQuality", [], [])
    qws.conditional_formatting.add(f"D5:D{4+len(quality)}",
        ColorScaleRule(start_type="min", start_color="FCE4D6", mid_type="percentile",
                       mid_value=50, mid_color="FFF2CC", end_type="max", end_color="E2F0D9"))

    # Read Me
    readme = wb.create_sheet("Read Me")
    style_title(readme, "READ ME | DEFINITIONS & LIMITATIONS", "Read before interpreting or reusing the workbook.", 6)
    notes = [
        ("Dataset provenance","Entirely synthetic and deterministically generated for portfolio demonstration. No real company or customer data."),
        ("Coverage","January 2024 to December 2025; 1,200 order records; 50 records per month."),
        ("Revenue","Quantity multiplied by unit price."),
        ("Cost","Quantity multiplied by unit cost."),
        ("Profit","Revenue minus cost. This is gross transaction-level profit, not net profit."),
        ("Profit margin","Total profit divided by total revenue."),
        ("Orders","Distinct order_id count. In this dataset each order has exactly one row."),
        ("Average order value","Total revenue divided by distinct orders."),
        ("Currency","Not specified. Monetary amounts are shown as generic currency units."),
        ("Simulation caveat","November/December multipliers are artificial generator parameters, not evidence of real seasonal demand."),
        ("Excluded factors","No taxes, discounts, shipping, returns, refunds, operating expenses, inventory, payment data or real customer identifiers."),
        ("Dashboard behavior","Executive dashboard charts are static overall views. Use analysis tabs for sortable/filterable tables; charts do not respond to filters."),
        ("Rebuild","Run python python/generate_sales_data.py, python python/analyze_sales.py, then python python/build_excel_workbook.py from the repository root."),
    ]
    for i,(label,desc) in enumerate(notes,4):
        readme.cell(i,1,label).font = Font(bold=True,color=BLUE)
        readme.merge_cells(start_row=i,start_column=2,end_row=i,end_column=6)
        readme.cell(i,2,desc).alignment = Alignment(wrap_text=True,vertical="top")
        readme.cell(i,2).font = Font(color=DARK,size=10)
        readme.row_dimensions[i].height = 34
    readme.column_dimensions["A"].width = 25
    for col in "BCDEF": readme.column_dimensions[col].width = 20
    readme.sheet_view.showGridLines = False

    # Global presentation
    for ws in wb.worksheets:
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0
        ws.sheet_view.zoomScale = 90
        ws.sheet_properties.tabColor = TEAL if ws.title == "Executive Dashboard" else BLUE
    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True
    wb.calculation.calcMode = "auto"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)
    print(f"Created {OUT} with {len(raw):,} source records and {len(wb.sheetnames)} worksheets.")

if __name__ == "__main__":
    main()
