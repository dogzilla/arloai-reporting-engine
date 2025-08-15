"""
Base widget class for ArloAI Reporting Engine.

All widgets inherit from BaseWidget and implement the render method.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class BaseWidget(ABC):
    """
    Abstract base class for all report widgets.
    
    Widgets are modular HTML components that:
    - Accept normalized data input
    - Return styled HTML blocks
    - Can be injected into template slots
    """
    
    def __init__(self, name: str, description: str = ""):
        """
        Initialize the widget.
        
        Args:
            name: Unique name for the widget
            description: Human-readable description
        """
        self.name = name
        self.description = description
    
    @abstractmethod
    def render(self, data: Dict[str, Any]) -> str:
        """
        Render the widget as HTML.
        
        Args:
            data: Normalized data dictionary
            
        Returns:
            HTML string for the widget
        """
        pass
    
    @abstractmethod
    def can_render(self, data: Dict[str, Any]) -> bool:
        """
        Check if the widget can render with the provided data.
        
        Args:
            data: Normalized data dictionary
            
        Returns:
            True if widget can render, False otherwise
        """
        pass
    
    def get_required_fields(self) -> List[str]:
        """
        Get list of required data fields for this widget.
        
        Returns:
            List of required field names
        """
        return []
    
    def get_optional_fields(self) -> List[str]:
        """
        Get list of optional data fields for this widget.
        
        Returns:
            List of optional field names
        """
        return []
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """
        Validate that the data contains required fields.
        
        Args:
            data: Data dictionary to validate
            
        Returns:
            True if data is valid, False otherwise
        """
        required_fields = self.get_required_fields()
        return all(field in data for field in required_fields)
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
    
    def __repr__(self) -> str:
        return self.__str__()