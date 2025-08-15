# ArloAI Reporting Engine

A comprehensive reporting engine that generates professional campaign performance reports in multiple formats: **HTML**, **PDF**, and **PowerPoint**.

## Overview

This reporting engine creates structured, visually rich campaign reports that can evolve from manually fed insights to fully automated, API-powered dashboards. Reports mimic the design aesthetic of professional agency insight reports while offering flexible ingestion, model-based analysis, and widget-level modularity.

## 🚀 Latest Updates (v2.0)

### **Multi-Format Output Pipeline**
- ✅ **Interactive HTML Reports** with Plotly charts and responsive design
- ✅ **Professional PDF Reports** with print-optimized styling
- ✅ **PowerPoint Presentations** with AI-powered generation via Presenton
- ✅ **Real Campaign Data Processing** from Excel files
- ✅ **Server Integration** for remote web access (192.168.7.174:53138)

### **Enhanced Data Visualization**
- 📊 **Interactive Plotly Charts**: Hover, zoom, pan functionality
- 📈 **Performance Dashboards**: KPI cards, daily trends, creative comparison
- 🎯 **Executive Summaries**: Automated insights and recommendations
- 📋 **Professional Styling**: Gradients, animations, responsive layouts

### **PowerPoint Integration**
- 🎨 **Presenton AI Integration**: AI-powered presentation generation
- 📊 **Python-pptx Fallback**: Reliable PowerPoint creation when Presenton unavailable
- 🔄 **Automatic Detection**: Smart fallback system for maximum reliability
- 💼 **Professional Templates**: Business-ready slide layouts with data visualization

## Features

- **Multi-Format Output**: HTML, PDF, and PowerPoint generation
- **Interactive Visualizations**: Plotly charts with hover interactions and zoom
- **AI-Powered Presentations**: Integration with Presenton for intelligent slide generation
- **Modular Widget Architecture**: Pluggable HTML components for different data visualizations
- **Real Data Processing**: Excel file ingestion with comprehensive campaign analytics
- **Professional Styling**: Agency-quality reports with modern design
- **Server Integration**: Remote web access with proper IP addressing
- **Flexible Data Sources**: Support for PDF, Excel, and future API integrations
- **Template-Based**: Uses Jinja2 for flexible HTML templating

## Report Types

- **Initial Report**: Campaign launch summary with static setup and early performance metrics
- **Mid-Campaign Report**: Regular updates (daily/weekly) with current performance metrics
- **Final Report**: Comprehensive wrap-up with detailed analysis and insights

## Current Widgets

### **Interactive HTML Widgets**
- `ctr_over_time`: Interactive CTR trends with Plotly
- `imps_clicks_over_time`: Dual-axis performance charts
- `creative_comparison`: Side-by-side KPI comparison cards
- `daily_spend_chart`: Animated spending visualization
- `session_engagement_chart`: Engagement metrics with hover details
- `budget_pacing_meter`: Progress indicators with visual feedback
- `topline_kpi_grid`: Comprehensive KPI dashboard
- `placement_performance_table`: Device/placement performance breakdown

### **PowerPoint Slide Templates**
- **Executive Summary**: Key metrics and campaign overview
- **KPI Dashboard**: Visual performance indicators with colored metrics
- **Daily Performance**: Detailed daily breakdown tables
- **Creative Analysis**: Performance comparison by creative version
- **Strategic Recommendations**: AI-generated insights and next steps
- **Professional Layouts**: University/business-appropriate styling

## Installation

```bash
pip install -r requirements.txt

# Additional dependencies for enhanced features
pip install plotly kaleido weasyprint reportlab python-pptx
```

## Quick Start

### **Generate All Report Formats**
```python
from examples.data_to_widgets import WidgetGenerator
from examples.powerpoint_integration import PowerPointGenerator

# HTML + PDF Generation
generator = WidgetGenerator()
html_report = generator.generate_complete_report(
    excel_files=["sample-data-20250710.xlsx"],
    output_file="campaign_report.html"
)

# PowerPoint Generation (with Presenton AI support)
ppt_generator = PowerPointGenerator()
presentations = ppt_generator.generate_presentation(
    excel_files=["sample-data-20250710.xlsx"],
    output_format="both"  # Tries Presenton AI, falls back to python-pptx
)
```

### **Interactive HTML Reports**
```python
# Generate enhanced reports with Plotly charts
from examples.enhanced_widgets_with_plotly import generate_enhanced_report

generate_enhanced_report(
    excel_files=["sample-data-20250710.xlsx"],
    output_file="enhanced_report.html",
    server_ip="192.168.7.174:53138"
)
```

### **Presenton AI Integration**
```python
from examples.presenton_api_helper import PresentonAPI

# AI-powered presentation generation
api = PresentonAPI("http://192.168.7.174:3050")
if api.health_check():
    pptx_data = api.create_campaign_presentation(campaign_data)
```

## Project Structure

```
arloai-reporting-engine/
├── arloai_reporting/                    # Main package
│   ├── __init__.py
│   ├── engine.py                       # Core reporting engine
│   ├── widgets/                        # Widget implementations
│   ├── templates/                      # Jinja2 templates
│   ├── data/                          # Data processing modules
│   └── utils/                         # Utility functions
├── examples/                          # Working implementations
│   ├── data_to_widgets.py            # HTML/PDF report generation
│   ├── enhanced_widgets_with_plotly.py # Interactive Plotly charts
│   ├── powerpoint_integration.py      # PowerPoint generation
│   ├── presenton_api_helper.py        # Presenton AI integration
│   ├── sample_data/                   # Real campaign data files
│   └── output/                        # Generated reports
├── tests/                             # Test suite
├── docs/                              # Documentation
└── requirements.txt                   # Dependencies
```

## 🎯 **Current Capabilities**

### **✅ Working Features**
- **Excel Data Processing**: Real campaign data (436K+ impressions, 15K+ clicks)
- **Interactive HTML Reports**: Plotly charts with hover/zoom functionality
- **PDF Export**: Professional print-ready reports with WeasyPrint
- **PowerPoint Generation**: Both AI-powered (Presenton) and reliable (python-pptx)
- **Server Integration**: Remote web access via 192.168.7.174:53138
- **Professional Styling**: Agency-quality layouts with responsive design
- **Executive Summaries**: Automated insights and recommendations

### **🔄 Ready for Testing**
- **Presenton AI Integration**: Service detected at http://192.168.7.174:3050
- **Multi-format Pipeline**: HTML → PDF → PowerPoint workflow
- **Design PDF Processing**: Extract layout specifications from reference PDFs
- **Custom Styling**: Apply brand guidelines and visual requirements

## Integration & Compatibility

### **✅ Currently Integrated**
- **Presenton AI** (http://192.168.7.174:3050) - AI-powered presentation generation
- **Plotly** - Interactive data visualizations with hover/zoom
- **WeasyPrint** - Professional PDF generation with print optimization
- **Python-pptx** - Reliable PowerPoint creation with custom layouts
- **Server Integration** - Remote web access via 192.168.7.174:53138

### **🔄 Compatible Systems**
- **Open Interpreter** - Report generation + LLM analysis
- **n8n / Activepieces** - Workflow orchestration and automation
- **Open Notebook** - Report archiving and documentation
- **Excel/CSV Data Sources** - Campaign data ingestion
- **PDF Reference Processing** - Design specification extraction

## 🧪 **Testing & Next Steps**

### **Ready to Test**
```bash
# Test HTML/PDF generation
python examples/data_to_widgets.py

# Test enhanced Plotly reports  
python examples/enhanced_widgets_with_plotly.py

# Test PowerPoint generation
python examples/powerpoint_integration.py

# Test Presenton AI integration (when service is running)
python examples/presenton_api_helper.py
```

### **View Generated Reports**
- **Interactive HTML**: http://192.168.7.174:53138/enhanced_plotly_report.html
- **PDF Reports**: Available in `/examples/output/` directory
- **PowerPoint Files**: Generated as `.pptx` files for download

### **Next Development Phase**
1. **Test Presenton AI integration** with running service
2. **Design PDF processing** for layout extraction and replication
3. **Custom styling implementation** based on brand guidelines
4. **Automated workflow integration** with n8n/Activepieces
5. **API endpoint development** for programmatic report generation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details.