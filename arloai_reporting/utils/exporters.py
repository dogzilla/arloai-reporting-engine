"""
Export utilities for converting reports to various formats.
"""

from typing import Union
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class HTMLExporter:
    """Exports reports as HTML files."""
    
    def export(self, content: str, output_path: Union[str, Path]) -> None:
        """
        Export HTML content to file.
        
        Args:
            content: HTML content string
            output_path: Path to save the HTML file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"HTML exported successfully to {output_path}")
        except Exception as e:
            logger.error(f"Error exporting HTML to {output_path}: {e}")
            raise


class PDFExporter:
    """Exports reports as PDF files."""
    
    def __init__(self, engine: str = "weasyprint"):
        """
        Initialize PDF exporter.
        
        Args:
            engine: PDF generation engine ('weasyprint' or 'reportlab')
        """
        self.engine = engine
    
    def export(self, content: str, output_path: Union[str, Path]) -> None:
        """
        Export HTML content to PDF file.
        
        Args:
            content: HTML content string
            output_path: Path to save the PDF file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if self.engine == "weasyprint":
                self._export_with_weasyprint(content, output_path)
            elif self.engine == "reportlab":
                self._export_with_reportlab(content, output_path)
            else:
                raise ValueError(f"Unsupported PDF engine: {self.engine}")
            
            logger.info(f"PDF exported successfully to {output_path}")
        except Exception as e:
            logger.error(f"Error exporting PDF to {output_path}: {e}")
            raise
    
    def _export_with_weasyprint(self, content: str, output_path: Path) -> None:
        """Export using WeasyPrint."""
        try:
            from weasyprint import HTML, CSS
            from weasyprint.text.fonts import FontConfiguration
            
            # Create font configuration
            font_config = FontConfiguration()
            
            # Add CSS for better PDF rendering
            pdf_css = CSS(string="""
                @page {
                    size: A4;
                    margin: 1in;
                }
                body {
                    font-family: Arial, sans-serif;
                    font-size: 12pt;
                    line-height: 1.4;
                }
                .page-break {
                    page-break-before: always;
                }
            """, font_config=font_config)
            
            # Generate PDF
            html_doc = HTML(string=content)
            html_doc.write_pdf(
                output_path,
                stylesheets=[pdf_css],
                font_config=font_config
            )
            
        except ImportError:
            logger.error("WeasyPrint not installed. Install with: pip install weasyprint")
            raise
    
    def _export_with_reportlab(self, content: str, output_path: Path) -> None:
        """Export using ReportLab (placeholder implementation)."""
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            
            # This is a very basic implementation
            # In practice, you'd need to parse HTML and convert to ReportLab elements
            c = canvas.Canvas(str(output_path), pagesize=letter)
            c.drawString(100, 750, "ArloAI Report")
            c.drawString(100, 730, "Generated from HTML content")
            c.drawString(100, 710, f"Content length: {len(content)} characters")
            c.save()
            
            logger.warning("ReportLab export is a placeholder implementation")
            
        except ImportError:
            logger.error("ReportLab not installed. Install with: pip install reportlab")
            raise