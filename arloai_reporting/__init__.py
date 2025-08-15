"""
ArloAI Reporting Engine

A modular reporting engine for generating HTML-based performance reports
from campaign data sources.
"""

__version__ = "0.1.0"
__author__ = "ArloAI"

from .engine import ReportEngine
from .widgets import *

__all__ = ["ReportEngine"]