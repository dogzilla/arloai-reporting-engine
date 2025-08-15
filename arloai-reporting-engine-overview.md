# ArloAI Reporting Engine – Project Overview

## 1. Project Goal

Build a modular reporting engine that programmatically generates HTML-based performance reports from campaign data sources. These reports should mimic the design aesthetic of the provided `sample_insight_report.pdf` and support automation, templating, and widget-based extensibility.

---

## 2. Report Types

- **Initial Report**: Campaign launch summary with static setup and early performance metrics.
- **Mid-Campaign Report**: Delivered on a variable cadence (e.g. daily, weekly) with updated metrics.
- **Final Report**: Wrap-up deep-dive with detailed breakdowns and insights.

---

## 3. Input Sources

- `Summary-Superflash-20250711.pdf`
- `Muzit Superflash Campaign CTR Report` spreadsheets (e.g., `20250710.xlsx`, `20250814.xlsx`)
- (Future) API feeds from ad platforms and analytics providers

---

## 4. Output Format & Design

- Reports are rendered as HTML (with optional PDF export).
- Layout and visual hierarchy modeled after `sample_insight_report.pdf`.
- Sectioned, widget-driven layout with clean typography and modular design blocks.

---

## 5. Widget Architecture

Widgets are modular HTML components. Each:
- Accepts normalized data input
- Returns a styled HTML block
- Is injected via the rendering engine into predefined template slots

All reports support pluggable widget injection and future dynamic expansion.

---

## 6. Currently Supported Widgets

- `ctr_over_time`: CTR by day (line chart)
- `imps_clicks_over_time`: Dual-axis bar chart
- `creative_comparison`: Side-by-side KPI cards
- `daily_spend_chart`: Bar chart
- `session_engagement_chart`: Line chart of engagement %
- `budget_pacing_meter`: KPI with budget progress bar
- `topline_kpi_grid`: CTR, CPC, CPM, Spend, Sessions, etc.
- `placement_performance_table`: CTR by placement/device

---

## 7. Core System Features

- Uses **Jinja2** for HTML templating
- Generates HTML for:
  - PDF conversion (WeasyPrint or headless Chrome)
  - Dashboard use (live or static)
- Ingestion abstraction:
  - Currently manual (via `.pdf`, `.xlsx`)
  - API-adaptable for automation
- Compatible with:
  - Open Interpreter (report generation + LLM analysis)
  - n8n / Activepieces (workflow orchestration)
  - Presenton (HTML presentation engine)
  - Open Notebook (report archiving)

---

## 8. Future Features & Widgets (from Glossary)

Planned widgets include:

- Day of Week
- Time of Day
- City / Region / DMA
- Age, Gender, Income
- Device Make / Type
- Weather, Temperature
- Connection Type, Carrier
- Mindset Index
- Retargeting vs Real-Time performance

Widgets will be added as data segments become available.

---

## 9. Summary

This reporting engine creates structured, visually rich HTML campaign reports that can evolve from manually fed insights to fully automated, API-powered dashboards.

It is designed with:
- Reusability
- Extensibility
- Cross-environment integration

…as core architectural principles.

It will produce high-fidelity outputs that resemble agency-quality insight reports while offering flexible ingestion, model-based analysis, and widget-level modularity.

