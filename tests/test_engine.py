"""
Tests for the ReportEngine class.
"""

import pytest
import tempfile
from pathlib import Path
import sys

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from arloai_reporting import ReportEngine
from arloai_reporting.engine import Report


class TestReportEngine:
    """Test cases for ReportEngine."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = ReportEngine()
    
    def test_engine_initialization(self):
        """Test that the engine initializes correctly."""
        assert self.engine is not None
        assert self.engine.data_processor is not None
        assert self.engine.widget_registry is not None
        assert self.engine.html_exporter is not None
        assert self.engine.pdf_exporter is not None
    
    def test_generate_report_with_empty_sources(self):
        """Test generating a report with no data sources."""
        report = self.engine.generate_report(
            report_type="mid_campaign",
            data_sources=[],
            template="default"
        )
        
        assert isinstance(report, Report)
        assert report.report_type == "mid_campaign"
        assert isinstance(report.content, str)
        assert len(report.content) > 0
    
    def test_generate_report_different_types(self):
        """Test generating different report types."""
        report_types = ["initial", "mid_campaign", "final"]
        
        for report_type in report_types:
            report = self.engine.generate_report(
                report_type=report_type,
                data_sources=[],
                template="default"
            )
            
            assert report.report_type == report_type
            assert isinstance(report.content, str)
    
    def test_report_html_export(self):
        """Test exporting report to HTML."""
        report = self.engine.generate_report(
            report_type="mid_campaign",
            data_sources=[],
            template="default"
        )
        
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        
        try:
            report.export_html(tmp_path)
            assert tmp_path.exists()
            
            # Check that the file contains HTML content
            content = tmp_path.read_text()
            assert "<!DOCTYPE html>" in content
            assert "<html" in content
            assert "</html>" in content
            
        finally:
            if tmp_path.exists():
                tmp_path.unlink()
    
    def test_widget_registry_has_widgets(self):
        """Test that the widget registry has some widgets."""
        widgets = self.engine.widget_registry.list_widgets()
        assert len(widgets) > 0
        
        # Check for some expected widgets
        expected_widgets = [
            "topline_kpi_grid",
            "ctr_over_time", 
            "budget_pacing_meter"
        ]
        
        for widget_name in expected_widgets:
            assert widget_name in widgets


class TestReport:
    """Test cases for Report class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.report = Report(
            content="<html><body>Test Report</body></html>",
            report_type="test",
            data_sources=[],
            widgets=["test_widget"]
        )
    
    def test_report_initialization(self):
        """Test that Report initializes correctly."""
        assert self.report.content == "<html><body>Test Report</body></html>"
        assert self.report.report_type == "test"
        assert self.report.data_sources == []
        assert self.report.widgets == ["test_widget"]
    
    def test_get_html(self):
        """Test getting HTML content."""
        html = self.report.get_html()
        assert html == "<html><body>Test Report</body></html>"


if __name__ == "__main__":
    pytest.main([__file__])