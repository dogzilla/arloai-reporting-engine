#!/usr/bin/env python3
"""
Basic usage example for ArloAI Reporting Engine.

This example demonstrates how to generate a simple report
using the reporting engine.
"""

import sys
from pathlib import Path

# Add the parent directory to the path so we can import arloai_reporting
sys.path.insert(0, str(Path(__file__).parent.parent))

from arloai_reporting import ReportEngine


def main():
    """Main example function."""
    print("ArloAI Reporting Engine - Basic Usage Example")
    print("=" * 50)
    
    # Initialize the reporting engine
    print("1. Initializing reporting engine...")
    engine = ReportEngine()
    
    # For this example, we'll create a report without real data sources
    # In practice, you would provide actual file paths
    print("2. Generating sample report...")
    
    try:
        # Generate a mid-campaign report
        report = engine.generate_report(
            report_type="mid_campaign",
            data_sources=[],  # Empty for this example
            template="default"
        )
        
        print("3. Report generated successfully!")
        print(f"   - Report type: {report.report_type}")
        print(f"   - Widgets included: {len(report.widgets)}")
        print(f"   - Widget names: {', '.join(report.widgets)}")
        
        # Export to HTML
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        html_path = output_dir / "sample_report.html"
        report.export_html(html_path)
        print(f"4. HTML report saved to: {html_path}")
        
        # Try to export to PDF (will work if weasyprint is installed)
        try:
            pdf_path = output_dir / "sample_report.pdf"
            report.export_pdf(pdf_path)
            print(f"5. PDF report saved to: {pdf_path}")
        except Exception as e:
            print(f"5. PDF export failed (install weasyprint for PDF support): {e}")
        
        print("\nExample completed successfully!")
        print(f"Check the output directory: {output_dir}")
        
    except Exception as e:
        print(f"Error generating report: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())