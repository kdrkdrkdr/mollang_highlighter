"""
Components module for Mollang IDE

Provides UI components for the IDE interface.
"""

from .editor import CodeEditor, EditorManager, LineNumberArea
from .dialogs import (
    KeywordEditDialog, KeywordListWidget, KeywordControlPanel,
    KeywordConfigDialog, MessageHelper
)
from .main_window import (
    MainWindow, MainWindowController, ToolbarManager, 
    GuidePanel, WindowFactory
)

__all__ = [
    # Editor components
    'CodeEditor',
    'EditorManager', 
    'LineNumberArea',
    
    # Dialog components
    'KeywordEditDialog',
    'KeywordListWidget',
    'KeywordControlPanel', 
    'KeywordConfigDialog',
    'MessageHelper',
    
    # Main window components
    'MainWindow',
    'MainWindowController',
    'ToolbarManager',
    'GuidePanel',
    'WindowFactory'
]
