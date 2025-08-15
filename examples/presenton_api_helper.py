#!/usr/bin/env python3
"""
Presenton API Helper - Direct integration with your Presenton installation.

This module provides direct API calls to Presenton for AI-powered presentation generation.
"""

import requests
import json
import time
from typing import Dict, Any, Optional, List
from pathlib import Path
import pandas as pd


class PresentonAPI:
    """Direct API integration with Presenton."""
    
    def __init__(self, base_url: str = "http://192.168.7.174:3050"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def health_check(self) -> bool:
        """Check if Presenton is healthy and accessible."""
        endpoints_to_try = [
            f"{self.base_url}/api/health",
            f"{self.base_url}/health",
            f"{self.base_url}/api/status",
            f"{self.base_url}/status",
            f"{self.base_url}/"
        ]
        
        for endpoint in endpoints_to_try:
            try:
                response = self.session.get(endpoint, timeout=10)
                if response.status_code in [200, 201]:
                    print(f"✅ Presenton accessible at: {endpoint}")
                    return True
            except Exception as e:
                continue
        
        print(f"❌ Presenton not accessible at {self.base_url}")
        return False
    
    def get_templates(self) -> List[Dict]:
        """Get available presentation templates."""
        try:
            response = self.session.get(f"{self.base_url}/api/templates", timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Templates endpoint returned: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error getting templates: {e}")
            return []
    
    def generate_presentation(self, 
                            prompt: str,
                            template: str = "business",
                            export_format: str = "pptx",
                            additional_data: Dict = None) -> Optional[bytes]:
        """Generate presentation using Presenton API."""
        
        payload = {
            "prompt": prompt,
            "template": template,
            "export_format": export_format
        }
        
        if additional_data:
            payload.update(additional_data)
        
        try:
            # Try different API endpoints that Presenton might use
            endpoints_to_try = [
                f"{self.base_url}/api/generate",
                f"{self.base_url}/api/presentations/generate",
                f"{self.base_url}/generate",
                f"{self.base_url}/api/v1/generate"
            ]
            
            for endpoint in endpoints_to_try:
                try:
                    print(f"🔄 Trying endpoint: {endpoint}")
                    response = self.session.post(endpoint, json=payload, timeout=120)
                    
                    if response.status_code in [200, 201]:
                        print(f"✅ Success with endpoint: {endpoint}")
                        
                        # Check if response is JSON (might contain download URL)
                        try:
                            json_response = response.json()
                            if 'download_url' in json_response:
                                # Download the file
                                download_response = self.session.get(
                                    f"{self.base_url}{json_response['download_url']}"
                                )
                                return download_response.content
                            elif 'file_data' in json_response:
                                # Base64 encoded file
                                import base64
                                return base64.b64decode(json_response['file_data'])
                        except:
                            # Response is likely the file itself
                            return response.content
                    
                    else:
                        print(f"❌ Endpoint {endpoint} returned: {response.status_code}")
                        if response.text:
                            print(f"   Response: {response.text[:200]}...")
                
                except Exception as e:
                    print(f"❌ Error with endpoint {endpoint}: {e}")
                    continue
            
            print("❌ All endpoints failed")
            return None
            
        except Exception as e:
            print(f"❌ Error generating presentation: {e}")
            return None
    
    def create_campaign_presentation(self, campaign_data: pd.DataFrame) -> Optional[bytes]:
        """Create a presentation specifically for campaign data."""
        
        # Prepare comprehensive campaign analysis
        total_impressions = campaign_data['Impressions'].sum()
        total_clicks = campaign_data['Clicks'].sum()
        avg_ctr = campaign_data['CTR'].mean()
        total_spend = campaign_data['Spend'].sum()
        avg_cpc = total_spend / total_clicks if total_clicks > 0 else 0
        
        date_range = f"{campaign_data['Date'].min().strftime('%B %d, %Y')} - {campaign_data['Date'].max().strftime('%B %d, %Y')}"
        
        # Daily performance analysis
        daily_performance = campaign_data.groupby('Date').agg({
            'Impressions': 'sum',
            'Clicks': 'sum',
            'CTR': 'mean',
            'Spend': 'sum'
        }).round(3)
        
        best_day = daily_performance['CTR'].idxmax()
        best_ctr = daily_performance['CTR'].max()
        
        # Creative performance
        creative_performance = campaign_data.groupby('Creative').agg({
            'Impressions': 'sum',
            'Clicks': 'sum',
            'CTR': 'mean',
            'Spend': 'sum'
        }).round(3)
        
        best_creative = creative_performance['CTR'].idxmax()
        
        # Create detailed prompt for Presenton
        prompt = f"""
        Create a professional campaign performance presentation for a university marketing campaign.
        
        CAMPAIGN OVERVIEW:
        - Campaign Period: {date_range}
        - Total Budget: ${total_spend:,.2f}
        - Total Impressions: {total_impressions:,}
        - Total Clicks: {total_clicks:,}
        - Average CTR: {avg_ctr:.3f}%
        - Average CPC: ${avg_cpc:.2f}
        
        KEY PERFORMANCE HIGHLIGHTS:
        - Best performing day: {best_day.strftime('%A, %B %d, %Y')} with {best_ctr:.3f}% CTR
        - Most effective creative: {best_creative.replace('Boston Area University Spring 2025  - ', '')}
        - Strong cost efficiency at ${avg_cpc:.2f} per click
        - Consistent daily performance with {len(daily_performance)} active days
        
        DAILY PERFORMANCE DATA:
        {daily_performance.to_string()}
        
        CREATIVE PERFORMANCE COMPARISON:
        {creative_performance.to_string()}
        
        PRESENTATION REQUIREMENTS:
        1. Executive Summary slide with key metrics and ROI
        2. Campaign Overview with timeline and objectives
        3. Performance Dashboard with KPI visualizations
        4. Daily Trends Analysis with charts
        5. Creative Performance Comparison
        6. Audience Insights and Engagement Metrics
        7. Cost Analysis and Budget Efficiency
        8. Key Insights and Learnings
        9. Strategic Recommendations for optimization
        10. Next Steps and Action Items
        
        DESIGN REQUIREMENTS:
        - Use a professional business theme
        - Include data visualizations and charts
        - Use university/education appropriate colors (blues, whites)
        - Make it suitable for executive presentation
        - Include clear call-to-action slides
        - Ensure all numbers are prominently displayed
        - Add visual elements like icons and graphics
        
        TARGET AUDIENCE: Marketing executives, university administrators, campaign stakeholders
        
        TONE: Professional, data-driven, actionable, optimistic about results
        """
        
        return self.generate_presentation(
            prompt=prompt,
            template="business",
            export_format="pptx",
            additional_data={
                "slides_count": 10,
                "include_charts": True,
                "theme": "professional",
                "color_scheme": "blue"
            }
        )


def test_presenton_integration():
    """Test Presenton integration with sample data."""
    print("🧪 Testing Presenton Integration")
    print("=" * 40)
    
    # Initialize API
    api = PresentonAPI()
    
    # Health check
    if not api.health_check():
        print("❌ Cannot connect to Presenton. Please ensure:")
        print("   1. Presenton is running on http://192.168.7.174:3050")
        print("   2. The service is accessible from this network")
        print("   3. No firewall is blocking the connection")
        return False
    
    # Get templates
    print("\n📋 Available Templates:")
    templates = api.get_templates()
    if templates:
        for template in templates:
            print(f"   • {template}")
    else:
        print("   No templates found or endpoint not available")
    
    # Test with sample data
    sample_dir = Path(__file__).parent / "sample_data"
    excel_files = [
        sample_dir / "sample-data-20250710.xlsx",
        sample_dir / "sample-data-20250814.xlsx"
    ]
    
    excel_files = [f for f in excel_files if f.exists()]
    
    if not excel_files:
        print("❌ No sample data found for testing")
        return False
    
    print(f"\n📊 Loading sample data from {len(excel_files)} files...")
    
    # Load data
    all_data = []
    for excel_file in excel_files:
        try:
            df = pd.read_excel(excel_file, sheet_name="Data")
            all_data.append(df)
        except Exception as e:
            print(f"Error reading {excel_file}: {e}")
    
    if not all_data:
        print("❌ Could not load sample data")
        return False
    
    combined_df = pd.concat(all_data, ignore_index=True)
    print(f"✅ Loaded {len(combined_df)} rows of campaign data")
    
    # Generate presentation
    print("\n🎨 Generating presentation with Presenton...")
    pptx_data = api.create_campaign_presentation(combined_df)
    
    if pptx_data:
        # Save the presentation
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / "presenton_campaign_report.pptx"
        with open(output_file, 'wb') as f:
            f.write(pptx_data)
        
        print(f"✅ Presenton presentation saved: {output_file}")
        print(f"📊 File size: {len(pptx_data):,} bytes")
        return True
    else:
        print("❌ Failed to generate presentation with Presenton")
        return False


if __name__ == "__main__":
    success = test_presenton_integration()
    
    if success:
        print("\n🎉 Presenton integration successful!")
        print("✅ Your ArloAI system can now generate AI-powered presentations")
    else:
        print("\n⚠️  Presenton integration not available")
        print("💡 The system will fall back to python-pptx generation")
        print("\nTo enable Presenton:")
        print("1. Start your Presenton service on http://192.168.7.174:3050")
        print("2. Ensure the API endpoints are accessible")
        print("3. Run this test again to verify connectivity")