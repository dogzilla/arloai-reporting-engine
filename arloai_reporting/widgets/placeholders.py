"""
Placeholder widgets for development and testing.
"""

from typing import Dict, Any
from .base import BaseWidget


class PlaceholderWidget(BaseWidget):
    """
    Placeholder widget that renders a simple HTML block.
    Used during development before actual widgets are implemented.
    """
    
    def __init__(self, name: str):
        """
        Initialize placeholder widget.
        
        Args:
            name: Name of the widget
        """
        super().__init__(name, f"Placeholder for {name} widget")
    
    def render(self, data: Dict[str, Any]) -> str:
        """
        Render a placeholder HTML block.
        
        Args:
            data: Data dictionary (unused for placeholder)
            
        Returns:
            HTML string with placeholder content
        """
        return f"""
        <div class="widget-placeholder" id="{self.name}">
            <div class="placeholder-header">
                <h3>{self.name.replace('_', ' ').title()}</h3>
                <span class="placeholder-badge">Placeholder</span>
            </div>
            <div class="placeholder-content">
                <p>This is a placeholder for the <strong>{self.name}</strong> widget.</p>
                <p>Widget implementation coming soon...</p>
            </div>
        </div>
        
        <style>
        .widget-placeholder {{
            border: 2px dashed #ccc;
            border-radius: 8px;
            padding: 20px;
            margin: 10px 0;
            background-color: #f9f9f9;
            font-family: Arial, sans-serif;
        }}
        
        .placeholder-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .placeholder-header h3 {{
            margin: 0;
            color: #666;
        }}
        
        .placeholder-badge {{
            background-color: #ffc107;
            color: #000;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }}
        
        .placeholder-content {{
            color: #888;
        }}
        
        .placeholder-content p {{
            margin: 5px 0;
        }}
        </style>
        """
    
    def can_render(self, data: Dict[str, Any]) -> bool:
        """
        Placeholder widgets can always render.
        
        Args:
            data: Data dictionary
            
        Returns:
            Always True for placeholders
        """
        return True