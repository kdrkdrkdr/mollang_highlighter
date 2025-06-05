"""
Mollang IDE - A Complete IDE for the Mollang Programming Language

A syntax highlighting IDE for the Mollang esoteric programming language with 
support for all language constructs including variables, operators, functions,
heap memory management, and string I/O.

Features:
- Complete syntax highlighting for all Mollang constructs
- Customizable keyword management
- Configuration save/load
- Line numbers and current line highlighting
- Dark theme optimized for coding

Architecture:
- core/: Core logic (highlighter, keywords, config)
- components/: UI components (editor, dialogs, main window)
- constants.py: Application constants and configuration
- main.py: Application entry point

Follows Frontend Design Guidelines for clean, maintainable code structure.
"""

from .main import MollangIDEApplication, main
from .core import *
from .components import *

__version__ = "1.0.0"
__author__ = "Mollang IDE Team"

__all__ = [
    'MollangIDEApplication',
    'main'
]
