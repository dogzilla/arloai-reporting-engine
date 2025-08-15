#!/usr/bin/env python3
"""
Enhanced widget generator with Plotly charts and PDF output support.
"""

import sys
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
from datetime import datetime
import weasyprint
import json

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from arloai_reporting.data.processors import DataProcessor


class EnhancedWidgetGenerator:
    """Enhanced widget generator with Plotly charts and PDF support."""
    
    def __init__(self, server_ip="192.168.7.174", server_port=53138):
        self.processor = DataProcessor()
        self.server_ip = server_ip
        self.server_port = server_port
        
        # Set Plotly theme
        pio.templates.default = "plotly_white"
    
    def generate_plotly_daily_chart(self, df: pd.DataFrame) -> str:
        """Generate interactive daily performance chart using Plotly."""
        daily_data = df.groupby('Date').agg({
            'Impressions': 'sum',
            'Clicks': 'sum',
            'CTR': 'mean',
            'Spend': 'sum'
        }).reset_index()
        
        # Create subplot with secondary y-axis
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Daily Impressions', 'Daily Clicks', 'CTR Trend', 'Daily Spend'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Impressions bar chart
        fig.add_trace(
            go.Bar(x=daily_data['Date'], y=daily_data['Impressions'], 
                   name='Impressions', marker_color='#3498db'),
            row=1, col=1
        )
        
        # Clicks bar chart
        fig.add_trace(
            go.Bar(x=daily_data['Date'], y=daily_data['Clicks'], 
                   name='Clicks', marker_color='#e74c3c'),
            row=1, col=2
        )
        
        # CTR line chart
        fig.add_trace(
            go.Scatter(x=daily_data['Date'], y=daily_data['CTR'], 
                      mode='lines+markers', name='CTR', line_color='#2ecc71'),
            row=2, col=1
        )
        
        # Spend area chart
        fig.add_trace(
            go.Scatter(x=daily_data['Date'], y=daily_data['Spend'], 
                      fill='tonexty', name='Spend', line_color='#f39c12'),
            row=2, col=2
        )
        
        fig.update_layout(
            height=600,
            showlegend=False,
            title_text="📈 Daily Performance Analytics",
            title_x=0.5,
            font=dict(family="Arial, sans-serif", size=12)
        )
        
        # Convert to HTML
        chart_html = fig.to_html(include_plotlyjs='cdn', div_id="daily-chart")
        
        return f"""
        <div class="plotly-chart-section">
            <h2>📈 Interactive Daily Performance</h2>
            {chart_html}
        </div>
        """
    
    def generate_plotly_performance_funnel(self, df: pd.DataFrame) -> str:
        """Generate performance funnel chart."""
        total_impressions = df['Impressions'].sum()
        total_clicks = df['Clicks'].sum()
        
        # Simulate conversion funnel (you'd have real data)
        conversions = int(total_clicks * 0.15)  # 15% conversion rate
        purchases = int(conversions * 0.25)     # 25% purchase rate
        
        fig = go.Figure(go.Funnel(
            y = ["Impressions", "Clicks", "Conversions", "Purchases"],
            x = [total_impressions, total_clicks, conversions, purchases],
            textinfo = "value+percent initial",
            marker = {"color": ["#3498db", "#e74c3c", "#2ecc71", "#f39c12"]},
            connector = {"line": {"color": "royalblue", "dash": "dot", "width": 3}}
        ))
        
        fig.update_layout(
            title="🎯 Campaign Performance Funnel",
            font=dict(family="Arial, sans-serif", size=14),
            height=400
        )
        
        chart_html = fig.to_html(include_plotlyjs='cdn', div_id="funnel-chart")
        
        return f"""
        <div class="plotly-chart-section">
            <h2>🎯 Performance Funnel</h2>
            {chart_html}
        </div>
        """
    
    def generate_plotly_creative_comparison(self, df: pd.DataFrame) -> str:
        """Generate creative comparison radar chart."""
        creative_data = df.groupby('Creative').agg({
            'Impressions': 'sum',
            'Clicks': 'sum',
            'CTR': 'mean',
            'Spend': 'sum'
        }).reset_index()
        
        # Normalize metrics for radar chart (0-100 scale)
        creative_data['Impressions_norm'] = (creative_data['Impressions'] / creative_data['Impressions'].max()) * 100
        creative_data['Clicks_norm'] = (creative_data['Clicks'] / creative_data['Clicks'].max()) * 100
        creative_data['CTR_norm'] = (creative_data['CTR'] / creative_data['CTR'].max()) * 100
        creative_data['Spend_norm'] = (creative_data['Spend'] / creative_data['Spend'].max()) * 100
        
        fig = go.Figure()
        
        categories = ['Impressions', 'Clicks', 'CTR', 'Spend']
        
        for _, row in creative_data.iterrows():
            creative_name = row['Creative'].replace('Boston Area University Spring 2025  - ', '')
            values = [row['Impressions_norm'], row['Clicks_norm'], row['CTR_norm'], row['Spend_norm']]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=creative_name
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="🎨 Creative Performance Comparison",
            height=500
        )
        
        chart_html = fig.to_html(include_plotlyjs='cdn', div_id="radar-chart")
        
        return f"""
        <div class="plotly-chart-section">
            <h2>🎨 Creative Performance Radar</h2>
            {chart_html}
        </div>
        """
    
    def generate_enhanced_report(self, excel_files: list, output_format="html") -> str:
        """Generate enhanced report with Plotly charts."""
        
        # Read and combine Excel data
        all_data = []
        for excel_file in excel_files:
            try:
                df = pd.read_excel(excel_file, sheet_name="Data")
                all_data.append(df)
            except Exception as e:
                print(f"Error reading {excel_file}: {e}")
        
        if not all_data:
            return "<p>No data could be loaded from Excel files.</p>"
        
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Generate enhanced widgets
        daily_chart = self.generate_plotly_daily_chart(combined_df)
        funnel_chart = self.generate_plotly_performance_funnel(combined_df)
        radar_chart = self.generate_plotly_creative_comparison(combined_df)
        
        # Basic KPIs
        total_impressions = combined_df['Impressions'].sum()
        total_clicks = combined_df['Clicks'].sum()
        avg_ctr = combined_df['CTR'].mean()
        total_spend = combined_df['Spend'].sum()
        
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>ArloAI Enhanced Campaign Report</title>
            <style>
                {self.get_enhanced_styles()}
            </style>
        </head>
        <body>
            <div class="report-container">
                <header class="report-header">
                    <h1>🚀 ArloAI Enhanced Campaign Report</h1>
                    <p class="report-subtitle">Interactive Analytics • Generated {datetime.now().strftime('%B %d, %Y')}</p>
                    <p class="server-info">🌐 Accessible at: http://{self.server_ip}:{self.server_port}/</p>
                </header>
                
                <div class="kpi-summary">
                    <div class="kpi-card">
                        <div class="kpi-icon">👁️</div>
                        <div class="kpi-content">
                            <div class="kpi-value">{total_impressions:,}</div>
                            <div class="kpi-label">Total Impressions</div>
                        </div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-icon">👆</div>
                        <div class="kpi-content">
                            <div class="kpi-value">{total_clicks:,}</div>
                            <div class="kpi-label">Total Clicks</div>
                        </div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-icon">🎯</div>
                        <div class="kpi-content">
                            <div class="kpi-value">{avg_ctr:.3f}%</div>
                            <div class="kpi-label">Average CTR</div>
                        </div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-icon">💰</div>
                        <div class="kpi-content">
                            <div class="kpi-value">${total_spend:,.2f}</div>
                            <div class="kpi-label">Total Spend</div>
                        </div>
                    </div>
                </div>
                
                {daily_chart}
                {funnel_chart}
                {radar_chart}
                
                <footer class="report-footer">
                    <p>Generated by ArloAI Reporting Engine with Plotly • Interactive Charts • Real-time Data</p>
                </footer>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def generate_pdf_report(self, html_content: str, output_path: str) -> bool:
        """Convert HTML report to PDF."""
        try:
            # Create PDF-optimized CSS
            pdf_css = """
            @page {
                size: A4;
                margin: 1cm;
            }
            .plotly-chart-section {
                page-break-inside: avoid;
                margin-bottom: 2cm;
            }
            .kpi-summary {
                page-break-inside: avoid;
            }
            """
            
            # Add PDF-specific styles
            html_with_pdf_css = html_content.replace(
                '</style>',
                pdf_css + '</style>'
            )
            
            # Generate PDF
            weasyprint.HTML(string=html_with_pdf_css).write_pdf(output_path)
            return True
            
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return False
    
    def get_enhanced_styles(self) -> str:
        """Enhanced CSS styles for modern dashboard."""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        
        .report-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .report-header {
            text-align: center;
            margin-bottom: 40px;
            padding: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .report-header h1 {
            font-size: 3em;
            margin-bottom: 15px;
            font-weight: 700;
        }
        
        .report-subtitle {
            font-size: 1.2em;
            opacity: 0.9;
            margin-bottom: 10px;
        }
        
        .server-info {
            font-size: 1em;
            opacity: 0.8;
            background: rgba(255,255,255,0.1);
            padding: 10px 20px;
            border-radius: 25px;
            display: inline-block;
            margin-top: 10px;
        }
        
        .kpi-summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-bottom: 50px;
        }
        
        .kpi-card {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            transition: all 0.3s ease;
            border-left: 5px solid #3498db;
        }
        
        .kpi-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        }
        
        .kpi-icon {
            font-size: 3em;
            margin-right: 25px;
            opacity: 0.8;
        }
        
        .kpi-value {
            font-size: 2.2em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }
        
        .kpi-label {
            font-size: 1em;
            color: #7f8c8d;
            font-weight: 500;
        }
        
        .plotly-chart-section {
            background: white;
            margin-bottom: 40px;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .plotly-chart-section h2 {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 25px 30px;
            margin: 0;
            font-size: 1.5em;
            font-weight: 600;
        }
        
        .plotly-chart-section .plotly-graph-div {
            padding: 20px;
        }
        
        .report-footer {
            text-align: center;
            padding: 30px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            color: #7f8c8d;
            font-size: 0.95em;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .report-container {
                padding: 10px;
            }
            
            .report-header h1 {
                font-size: 2em;
            }
            
            .kpi-summary {
                grid-template-columns: 1fr;
            }
            
            .kpi-card {
                padding: 20px;
            }
            
            .kpi-icon {
                font-size: 2.5em;
                margin-right: 15px;
            }
        }
        
        /* Print Styles */
        @media print {
            body {
                background: white;
            }
            
            .report-container {
                max-width: none;
                padding: 0;
            }
            
            .plotly-chart-section {
                page-break-inside: avoid;
                margin-bottom: 30px;
            }
        }
        """


def main():
    """Generate enhanced report with Plotly charts."""
    print("🚀 Generating Enhanced Report with Plotly Charts")
    print("=" * 60)
    
    # Find sample files
    sample_dir = Path(__file__).parent / "sample_data"
    excel_files = [
        str(sample_dir / "sample-data-20250710.xlsx"),
        str(sample_dir / "sample-data-20250814.xlsx")
    ]
    
    excel_files = [f for f in excel_files if Path(f).exists()]
    
    if not excel_files:
        print("❌ No Excel files found!")
        return 1
    
    print(f"📊 Processing {len(excel_files)} Excel files...")
    
    # Generate enhanced report
    generator = EnhancedWidgetGenerator()
    
    # HTML Report
    html_report = generator.generate_enhanced_report(excel_files, "html")
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Save HTML
    html_file = output_dir / "enhanced_plotly_report.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    print(f"✅ Enhanced HTML report: {html_file}")
    print(f"🌐 View at: http://192.168.7.174:53138/enhanced_plotly_report.html")
    
    # Generate PDF
    pdf_file = output_dir / "enhanced_plotly_report.pdf"
    if generator.generate_pdf_report(html_report, str(pdf_file)):
        print(f"📄 PDF report generated: {pdf_file}")
    else:
        print("⚠️  PDF generation failed (charts may not render in PDF)")
    
    print("\n🎉 Enhanced report generation complete!")
    print("\nFeatures added:")
    print("✅ Interactive Plotly charts")
    print("✅ Responsive design")
    print("✅ PDF export capability")
    print("✅ Server IP integration")
    print("✅ Modern dashboard styling")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())