# ============================================================
# DAY 36 — Missing Data Handling with pandas
# File: day36_missing_data.py
# Dataset: Portfolio stocks + Monthly revenue (with deliberate NaNs)
# ============================================================

import pandas as pd
import numpy as np

# ── Load both sheets from Excel ──────────────────────────────
portfolio = pd.read_excel("day36_input.xlsx", sheet_name="Portfolio_Data")
revenue   = pd.read_excel("day36_input.xlsx", sheet_name="Monthly_Revenue")

print("=" * 60)
print("DAY 36 — MISSING DATA HANDLING")
print("=" * 60)

# ============================================================
# SECTION 1 — DETECTING MISSING VALUES
# ============================================================
print("\n── SECTION 1: DETECTING MISSING VALUES ──\n")

# 1A. isnull() → returns True where value is NaN/None
null_mask = portfolio.isnull()
print("isnull() output (first 5 rows):")
print(null_mask.head())

# 1B. isnull().sum() → count of nulls per column  ← most useful line in practice
print("\nNull count per column (portfolio):")
print(portfolio.isnull().sum())

# 1C. Percentage of nulls per column
print("\nNull % per column (portfolio):")
null_pct = (portfolio.isnull().sum() / len(portfolio) * 100).round(2)
print(null_pct)

# 1D. notnull() → opposite of isnull(); True where data EXISTS
print("\nRows where Current_Price is NOT null:")
print(portfolio[portfolio["Current_Price"].notnull()]["Stock"].tolist())

# 1E. info() → quick overview including non-null counts per column
print("\nportfolio.info():")
portfolio.info()

# 1F. Total null cells in entire DataFrame
total_nulls = portfolio.isnull().sum().sum()
print(f"\nTotal null cells in portfolio sheet: {total_nulls}")

# ============================================================
# SECTION 2 — DROPPING NULLS
# ============================================================
print("\n── SECTION 2: DROPPING NULLS ──\n")

# 2A. dropna() — drops ALL rows that have ANY null
df_dropped_any = portfolio.dropna()
print(f"Rows after dropna() (any null removed): {len(df_dropped_any)}")

# 2B. dropna(how='all') — drops only rows where EVERY cell is null
df_dropped_all = portfolio.dropna(how='all')
print(f"Rows after dropna(how='all'):           {len(df_dropped_all)}")

# 2C. dropna(subset=[...]) — drop rows where specific columns are null
#     Use case: we NEED Current_Price to calculate PnL, so drop only if that's missing
df_need_price = portfolio.dropna(subset=["Current_Price"])
print(f"Rows with Current_Price available:      {len(df_need_price)}")

# 2D. dropna(thresh=N) — keep rows that have at least N non-null values
df_thresh = portfolio.dropna(thresh=5)   # row must have at least 5 valid values
print(f"Rows with at least 5 valid fields:      {len(df_thresh)}")

# ============================================================
# SECTION 3 — FILLING NULLS WITH fillna()
# ============================================================
print("\n── SECTION 3: FILLING NULLS ──\n")

# Make a working copy — never modify the original directly
df = portfolio.copy()

# 3A. Fill with a fixed constant
#     Use case: missing sector → label as "Unknown"
df["Sector"] = df["Sector"].fillna("Unknown")
print("Sector after fillna('Unknown'):")
print(df["Sector"].tolist())

# 3B. Fill with column mean
#     Use case: missing Quantity → assume average portfolio position size
mean_qty = df["Quantity"].mean()
df["Quantity"] = df["Quantity"].fillna(mean_qty).round(0)
print(f"\nQuantity mean used for fill: {mean_qty:.0f}")
print(f"Quantity after fillna(mean): {df['Quantity'].tolist()}")

# 3C. Fill with column median
#     Use case: Buy_Price — median is better than mean when outliers exist (DRREDDY at 5800!)
median_buy = df["Buy_Price"].median()
df["Buy_Price"] = df["Buy_Price"].fillna(median_buy)
print(f"\nBuy_Price median used for fill: {median_buy}")

# 3D. Fill with column mode (most frequent value)
#     Use case: Dividend_Yield — fill with the most common yield in the dataset
mode_div = df["Dividend_Yield"].mode()[0]   # mode() returns a Series, take index 0
df["Dividend_Yield"] = df["Dividend_Yield"].fillna(mode_div)
print(f"\nDividend_Yield mode used for fill: {mode_div}")

# 3E. Fill Current_Price with Buy_Price as a logical fallback
#     Use case: if we have no current price, use buy price (assumes flat return)
df["Current_Price"] = df["Current_Price"].fillna(df["Buy_Price"])
print("\nCurrent_Price after fillna(Buy_Price fallback):")
print(df[["Stock", "Buy_Price", "Current_Price"]])

# ============================================================
# SECTION 4 — FORWARD FILL & BACKWARD FILL
# ============================================================
print("\n── SECTION 4: FORWARD FILL & BACKWARD FILL ──\n")

# Time-series data: forward fill propagates last known value forward
# This makes sense for financial data (price unchanged until new data arrives)
rev = revenue.copy()

print("Revenue before fill (Revenue_Lakhs):")
print(rev[["Month", "Revenue_Lakhs"]])

# 4A. Forward Fill (ffill) — copy from row ABOVE
rev_ffill = rev.copy()
rev_ffill["Revenue_Lakhs"] = rev_ffill["Revenue_Lakhs"].ffill()
print("\nRevenue_Lakhs after ffill():")
print(rev_ffill[["Month", "Revenue_Lakhs"]])

# 4B. Backward Fill (bfill) — copy from row BELOW
rev_bfill = rev.copy()
rev_bfill["Revenue_Lakhs"] = rev_bfill["Revenue_Lakhs"].bfill()
print("\nRevenue_Lakhs after bfill():")
print(rev_bfill[["Month", "Revenue_Lakhs"]])

# ============================================================
# SECTION 5 — INTERPOLATION
# ============================================================
print("\n── SECTION 5: INTERPOLATION ──\n")

# interpolate() estimates missing values by fitting a line between known points
# Best for smooth time-series (revenue, prices) — does NOT make sense for categories

rev_interp = rev.copy()
rev_interp["Revenue_Lakhs"]   = rev_interp["Revenue_Lakhs"].interpolate(method="linear")
rev_interp["Expenses_Lakhs"]  = rev_interp["Expenses_Lakhs"].interpolate(method="linear")
rev_interp["Profit_Lakhs"]    = rev_interp["Profit_Lakhs"].interpolate(method="linear")
rev_interp["Growth_Pct"]      = rev_interp["Growth_Pct"].interpolate(method="linear")

print("Revenue sheet after linear interpolation:")
print(rev_interp.to_string(index=False))

# ============================================================
# SECTION 6 — REAL-WORLD PIPELINE: CLEAN → CALCULATE → EXPORT
# ============================================================
print("\n── SECTION 6: CLEAN PIPELINE → EXPORT ──\n")

# Step 1: Load fresh copy
df_clean = portfolio.copy()

# Step 2: Fill each column using the most appropriate strategy
df_clean["Sector"]         = df_clean["Sector"].fillna("Unknown")
df_clean["Quantity"]       = df_clean["Quantity"].fillna(df_clean["Quantity"].median())
df_clean["Buy_Price"]      = df_clean["Buy_Price"].fillna(df_clean["Buy_Price"].median())
df_clean["Current_Price"]  = df_clean["Current_Price"].fillna(df_clean["Buy_Price"])
df_clean["Dividend_Yield"] = df_clean["Dividend_Yield"].fillna(df_clean["Dividend_Yield"].mean())

# Step 3: Derive new columns
df_clean["Investment_Value"]  = (df_clean["Quantity"] * df_clean["Buy_Price"]).round(2)
df_clean["Current_Value"]     = (df_clean["Quantity"] * df_clean["Current_Price"]).round(2)
df_clean["PnL"]               = (df_clean["Current_Value"] - df_clean["Investment_Value"]).round(2)
df_clean["Return_Pct"]        = ((df_clean["PnL"] / df_clean["Investment_Value"]) * 100).round(2)

print("Cleaned portfolio with PnL:")
print(df_clean[["Stock", "Sector", "Investment_Value", "Current_Value", "PnL", "Return_Pct"]].to_string(index=False))

# Step 4: Export to Excel — two sheets
with pd.ExcelWriter("day36_output.xlsx", engine="openpyxl") as writer:
    df_clean.to_excel(writer, sheet_name="Cleaned_Portfolio", index=False)
    rev_interp.to_excel(writer, sheet_name="Interpolated_Revenue", index=False)

print("\n✅ Output exported: day36_output.xlsx")
print("   → Sheet 1: Cleaned_Portfolio")
print("   → Sheet 2: Interpolated_Revenue")

# ============================================================
# SECTION 7 — SUMMARY AUDIT: BEFORE vs AFTER
# ============================================================
print("\n── SECTION 7: AUDIT — NULL COUNT BEFORE vs AFTER ──\n")

before = portfolio.isnull().sum().sum()
after  = df_clean.isnull().sum().sum()
print(f"Total nulls BEFORE cleaning : {before}")
print(f"Total nulls AFTER  cleaning : {after}")
print(f"Nulls resolved              : {before - after}")
