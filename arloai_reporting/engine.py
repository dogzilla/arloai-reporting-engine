"""
Core reporting engine for ArloAI Reporting Engine.

This module contains the main ReportEngine class that orchestrates
report generation from data sources to final HTML/PDF output.
"""

from typing import Dict, List, Optional, Union, Any
from pathlib import Path
import logging
from jinja2 import Environment, FileSystemLoader

from .data.processors import DataProcessor
from .widgets.registry import WidgetRegistry
from .utils.exporters import HTMLExporter, PDFExporter

logger = logging.getLogger(__name__)


class ReportEngine:
    """
    Main reporting engine that coordinates data processing, widget rendering,
    and report generation.
    """
    
    def __init__(self, template_dir: Optional[str] = None):
        """
        Initialize the reporting engine.
        
        Args:
            template_dir: Directory containing Jinja2 templates
        """
        self.template_dir = template_dir or str(Path(__file__).parent / "templates")
        self.jinja_env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=True
        )
        
        self.data_processor = DataProcessor()
        self.widget_registry = WidgetRegistry()
        self.html_exporter = HTMLExporter()
        self.pdf_exporter = PDFExporter()
        
        logger.info("ReportEngine initialized")
    
    def generate_report(
        self,
        report_type: str,
        data_sources: List[Union[str, Path]],
        template: str = "default",
        widgets: Optional[List[str]] = None,
        output_format: str = "html"
    ) -> "Report":
        """
        Generate a report from data sources.
        
        Args:
            report_type: Type of report ('initial', 'mid_campaign', 'final')
            data_sources: List of data source file paths
            template: Template name to use
            widgets: List of widget names to include (None for auto-selection)
            output_format: Output format ('html', 'pdf', 'both')
            
        Returns:
            Report object with generated content
        """
        logger.info(f"Generating {report_type} report with {len(data_sources)} data sources")
        
        # Process data sources
        processed_data = self.data_processor.process_sources(data_sources)
        
        # Select widgets based on report type and available data
        if widgets is None:
            widgets = self._select_widgets_for_report_type(report_type, processed_data)
        
        # Render widgets
        rendered_widgets = {}
        for widget_name in widgets:
            widget = self.widget_registry.get_widget(widget_name)
            if widget and widget.can_render(processed_data):
                rendered_widgets[widget_name] = widget.render(processed_data)
                logger.debug(f"Rendered widget: {widget_name}")
            else:
                logger.warning(f"Skipping widget {widget_name} - cannot render with available data")
        
        # Load and render template
        template_obj = self.jinja_env.get_template(f"{template}.html")
        html_content = template_obj.render(
            report_type=report_type,
            widgets=rendered_widgets,
            data=processed_data,
            metadata=self._generate_metadata(report_type, data_sources)
        )
        
        # Create report object
        report = Report(
            content=html_content,
            report_type=report_type,
            data_sources=data_sources,
            widgets=list(rendered_widgets.keys())
        )
        
        logger.info(f"Report generated successfully with {len(rendered_widgets)} widgets")
        return report
    
    def _select_widgets_for_report_type(
        self, 
        report_type: str, 
        data: Dict[str, Any]
    ) -> List[str]:
        """
        Auto-select appropriate widgets based on report type and available data.
        
        Args:
            report_type: Type of report
            data: Processed data dictionary
            
        Returns:
            List of widget names to include
        """
        # This is a placeholder implementation
        # In practice, this would analyze the data and select appropriate widgets
        base_widgets = ["topline_kpi_grid"]
        
        if report_type == "initial":
            return base_widgets + ["budget_pacing_meter"]
        elif report_type == "mid_campaign":
            return base_widgets + [
                "ctr_over_time",
                "imps_clicks_over_time", 
                "daily_spend_chart"
            ]
        elif report_type == "final":
            return base_widgets + [
                "ctr_over_time",
                "imps_clicks_over_time",
                "creative_comparison",
                "placement_performance_table",
                "session_engagement_chart"
            ]
        else:
            return base_widgets
    
    def _generate_metadata(
        self, 
        report_type: str, 
        data_sources: List[Union[str, Path]]
    ) -> Dict[str, Any]:
        """Generate metadata for the report."""
        from datetime import datetime
        
        return {
            "generated_at": datetime.now().isoformat(),
            "report_type": report_type,
            "data_sources": [str(source) for source in data_sources],
            "engine_version": "0.1.0"
        }


class Report:
    """
    Represents a generated report with content and metadata.
    """
    
    def __init__(
        self,
        content: str,
        report_type: str,
        data_sources: List[Union[str, Path]],
        widgets: List[str]
    ):
        self.content = content
        self.report_type = report_type
        self.data_sources = data_sources
        self.widgets = widgets
        self.html_exporter = HTMLExporter()
        self.pdf_exporter = PDFExporter()
    
    def export_html(self, output_path: Union[str, Path]) -> None:
        """Export report as HTML file."""
        self.html_exporter.export(self.content, output_path)
        logger.info(f"Report exported to HTML: {output_path}")
    
    def export_pdf(self, output_path: Union[str, Path]) -> None:
        """Export report as PDF file."""
        self.pdf_exporter.export(self.content, output_path)
        logger.info(f"Report exported to PDF: {output_path}")
    
    def get_html(self) -> str:
        """Get the HTML content of the report."""
        return self.content