# Day 36 — Missing Data Handling with pandas

**Phase 3 | 84-Day Python + Excel Roadmap**
**Date:** May 10, 2026
**Author:** Bhanu Pratap Singh

---

## Overview

Practiced all core missing-data techniques in pandas using a realistic Indian stock portfolio dataset and monthly revenue time-series, both containing deliberate NaN values.

---

## Files

| File | Description |
|---|---|
| `day36_input.xlsx` | Raw input — Portfolio_Data + Monthly_Revenue sheets with NaNs |
| `day36_missing_data.py` | Main practice script — 7 sections covering all techniques |
| `day36_output.xlsx` | Cleaned output — Cleaned_Portfolio + Interpolated_Revenue sheets |

---

## Techniques Covered

| Technique | Method | Use Case |
|---|---|---|
| Null detection | `isnull()`, `notnull()`, `info()` | Audit data quality |
| Count nulls | `isnull().sum()` | Find problematic columns |
| Drop rows | `dropna()`, `dropna(subset=[])` | Remove unrecoverable records |
| Fill constant | `fillna("Unknown")` | Categorical columns |
| Fill mean/median | `fillna(df[col].mean())` | Numeric columns |
| Fill mode | `fillna(df[col].mode()[0])` | Most frequent value |
| Logical fallback | `fillna(df["other_col"])` | Use related column |
| Forward fill | `ffill()` | Time-series: carry last value |
| Backward fill | `bfill()` | Time-series: pull next value |
| Interpolation | `interpolate(method="linear")` | Smooth numeric series |

---

## Key Result

- **Dataset:** 15 stocks, 7 columns, 18 missing values
- **After cleaning:** 0 null cells
- **Derived columns:** Investment Value, Current Value, PnL, Return %
- **Export:** 2-sheet Excel workbook

---

## Portfolio Connection

Missing data handling is a mandatory first step in any real financial data pipeline. Every project from Day 50 onward will include a cleaning stage using these exact techniques before any analysis or visualization.
