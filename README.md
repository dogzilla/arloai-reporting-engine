# ArloAI Reporting Engine

A modular reporting engine that programmatically generates HTML-based performance reports from campaign data sources.

## Overview

This reporting engine creates structured, visually rich HTML campaign reports that can evolve from manually fed insights to fully automated, API-powered dashboards. Reports mimic the design aesthetic of professional agency insight reports while offering flexible ingestion, model-based analysis, and widget-level modularity.

## Features

- **Modular Widget Architecture**: Pluggable HTML components for different data visualizations
- **Multiple Report Types**: Initial, mid-campaign, and final reports
- **Flexible Data Sources**: Support for PDF, Excel, and future API integrations
- **HTML/PDF Output**: Generate reports for web viewing or PDF export
- **Template-Based**: Uses Jinja2 for flexible HTML templating

## Report Types

- **Initial Report**: Campaign launch summary with static setup and early performance metrics
- **Mid-Campaign Report**: Regular updates (daily/weekly) with current performance metrics
- **Final Report**: Comprehensive wrap-up with detailed analysis and insights

## Current Widgets

- `ctr_over_time`: CTR by day (line chart)
- `imps_clicks_over_time`: Dual-axis bar chart
- `creative_comparison`: Side-by-side KPI cards
- `daily_spend_chart`: Bar chart
- `session_engagement_chart`: Line chart of engagement %
- `budget_pacing_meter`: KPI with budget progress bar
- `topline_kpi_grid`: CTR, CPC, CPM, Spend, Sessions, etc.
- `placement_performance_table`: CTR by placement/device

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from arloai_reporting import ReportEngine

# Initialize the engine
engine = ReportEngine()

# Generate a report
report = engine.generate_report(
    report_type="mid_campaign",
    data_sources=["campaign_data.xlsx"],
    template="default"
)

# Export to HTML
report.export_html("campaign_report.html")

# Export to PDF
report.export_pdf("campaign_report.pdf")
```

## Project Structure

```
arloai-reporting-engine/
├── arloai_reporting/           # Main package
│   ├── __init__.py
│   ├── engine.py              # Core reporting engine
│   ├── widgets/               # Widget implementations
│   ├── templates/             # Jinja2 templates
│   ├── data/                  # Data processing modules
│   └── utils/                 # Utility functions
├── tests/                     # Test suite
├── examples/                  # Example usage and sample data
├── docs/                      # Documentation
└── requirements.txt           # Dependencies
```

## Integration

Compatible with:
- Open Interpreter (report generation + LLM analysis)
- n8n / Activepieces (workflow orchestration)
- Presenton (HTML presentation engine)
- Open Notebook (report archiving)
- WeasyPrint or headless Chrome (PDF conversion)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details.