#!/usr/bin/env python3
"""
Example using real sample data files.

This example demonstrates how to generate reports using actual
campaign data files placed in the sample_data directory.
"""

import sys
from pathlib import Path
import glob

# Add the parent directory to the path so we can import arloai_reporting
sys.path.insert(0, str(Path(__file__).parent.parent))

from arloai_reporting import ReportEngine


def find_sample_files():
    """Find available sample data files."""
    sample_dir = Path(__file__).parent / "sample_data"
    
    files = {
        "excel": list(sample_dir.glob("excel/*.xlsx")) + list(sample_dir.glob("excel/*.xls")),
        "csv": list(sample_dir.glob("csv/*.csv")),
        "pdf": list(sample_dir.glob("pdfs/*.pdf")),
        "json": list(sample_dir.glob("json/*.json"))
    }
    
    return files


def main():
    """Main example function."""
    print("ArloAI Reporting Engine - Sample Data Example")
    print("=" * 50)
    
    # Find available sample files
    sample_files = find_sample_files()
    
    print("1. Scanning for sample data files...")
    total_files = sum(len(files) for files in sample_files.values())
    
    if total_files == 0:
        print("   No sample data files found!")
        print("   Please add sample files to examples/sample_data/")
        print("   Supported formats: .xlsx, .xls, .csv, .pdf, .json")
        print("\n   Directory structure:")
        print("   examples/sample_data/")
        print("   ├── excel/     # Excel files (.xlsx, .xls)")
        print("   ├── csv/       # CSV files")
        print("   ├── pdfs/      # PDF files")
        print("   └── json/      # JSON files")
        return 1
    
    print(f"   Found {total_files} sample files:")
    for file_type, files in sample_files.items():
        if files:
            print(f"   - {file_type.upper()}: {len(files)} files")
            for file_path in files:
                print(f"     • {file_path.name}")
    
    # Collect all available data sources
    data_sources = []
    for files in sample_files.values():
        data_sources.extend([str(f) for f in files])
    
    if not data_sources:
        print("   No valid data sources found.")
        return 1
    
    # Initialize the reporting engine
    print("\n2. Initializing reporting engine...")
    engine = ReportEngine()
    
    # Generate reports for different types
    report_types = ["initial", "mid_campaign", "final"]
    
    for report_type in report_types:
        print(f"\n3. Generating {report_type} report...")
        
        try:
            report = engine.generate_report(
                report_type=report_type,
                data_sources=data_sources,
                template="default"
            )
            
            print(f"   ✓ Report generated successfully!")
            print(f"     - Report type: {report.report_type}")
            print(f"     - Data sources: {len(report.data_sources)}")
            print(f"     - Widgets: {len(report.widgets)}")
            
            # Export to HTML
            output_dir = Path(__file__).parent / "output"
            output_dir.mkdir(exist_ok=True)
            
            html_path = output_dir / f"{report_type}_report_with_data.html"
            report.export_html(html_path)
            print(f"     - HTML saved: {html_path}")
            
            # Try PDF export
            try:
                pdf_path = output_dir / f"{report_type}_report_with_data.pdf"
                report.export_pdf(pdf_path)
                print(f"     - PDF saved: {pdf_path}")
            except Exception as e:
                print(f"     - PDF export failed: {e}")
        
        except Exception as e:
            print(f"   ✗ Error generating {report_type} report: {e}")
    
    print(f"\n4. Example completed!")
    print(f"   Check output directory: {Path(__file__).parent / 'output'}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())