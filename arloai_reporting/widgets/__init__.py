"""
Widget system for ArloAI Reporting Engine.

This module contains the widget architecture for creating modular,
reusable report components.
"""

from .base import BaseWidget
from .registry import WidgetRegistry

__all__ = ["BaseWidget", "WidgetRegistry"]