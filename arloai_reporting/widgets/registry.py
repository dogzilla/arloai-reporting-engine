"""
Widget registry for managing available widgets.
"""

from typing import Dict, Optional, List
import logging

from .base import BaseWidget

logger = logging.getLogger(__name__)


class WidgetRegistry:
    """
    Registry for managing and accessing available widgets.
    """
    
    def __init__(self):
        """Initialize the widget registry."""
        self._widgets: Dict[str, BaseWidget] = {}
        self._load_default_widgets()
    
    def register_widget(self, widget: BaseWidget) -> None:
        """
        Register a widget in the registry.
        
        Args:
            widget: Widget instance to register
        """
        self._widgets[widget.name] = widget
        logger.debug(f"Registered widget: {widget.name}")
    
    def get_widget(self, name: str) -> Optional[BaseWidget]:
        """
        Get a widget by name.
        
        Args:
            name: Name of the widget
            
        Returns:
            Widget instance or None if not found
        """
        return self._widgets.get(name)
    
    def list_widgets(self) -> List[str]:
        """
        Get list of all registered widget names.
        
        Returns:
            List of widget names
        """
        return list(self._widgets.keys())
    
    def get_widgets_for_data(self, data: Dict) -> List[str]:
        """
        Get list of widgets that can render with the provided data.
        
        Args:
            data: Data dictionary
            
        Returns:
            List of widget names that can render
        """
        compatible_widgets = []
        for name, widget in self._widgets.items():
            if widget.can_render(data):
                compatible_widgets.append(name)
        return compatible_widgets
    
    def _load_default_widgets(self) -> None:
        """Load default widgets into the registry."""
        # Import and register default widgets
        try:
            from .kpi_widgets import ToplineKPIGrid, BudgetPacingMeter
            from .chart_widgets import CTROverTime, ImpsClicksOverTime, DailySpendChart
            from .table_widgets import PlacementPerformanceTable
            from .comparison_widgets import CreativeComparison
            
            # Register all default widgets
            default_widgets = [
                ToplineKPIGrid(),
                BudgetPacingMeter(),
                CTROverTime(),
                ImpsClicksOverTime(),
                DailySpendChart(),
                PlacementPerformanceTable(),
                CreativeComparison()
            ]
            
            for widget in default_widgets:
                self.register_widget(widget)
                
            logger.info(f"Loaded {len(default_widgets)} default widgets")
            
        except ImportError as e:
            logger.warning(f"Could not load some default widgets: {e}")
            # Create placeholder widgets for now
            self._create_placeholder_widgets()
    
    def _create_placeholder_widgets(self) -> None:
        """Create placeholder widgets for development."""
        from .placeholders import PlaceholderWidget
        
        widget_names = [
            "topline_kpi_grid",
            "budget_pacing_meter", 
            "ctr_over_time",
            "imps_clicks_over_time",
            "daily_spend_chart",
            "placement_performance_table",
            "creative_comparison",
            "session_engagement_chart"
        ]
        
        for name in widget_names:
            widget = PlaceholderWidget(name)
            self.register_widget(widget)
        
        logger.info(f"Created {len(widget_names)} placeholder widgets")