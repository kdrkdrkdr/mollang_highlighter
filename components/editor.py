"""
Code Editor Component

Follows Frontend Design Guideline: Abstracting Implementation Details
"""

from PySide6.QtWidgets import QWidget, QPlainTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QPainter, QTextEdit, QTextCharFormat, QTextCursor

from constants import (
    DEFAULT_FONT_SIZE, TAB_SPACES, EditorColors,
    DEFAULT_SAMPLE_CODE
)
from core.highlighter import HighlighterFactory


class LineNumberArea(QWidget):
    """
    줄 번호 표시 영역
    
    Follows Frontend Design Guideline: Single Responsibility
    """
    
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return self.code_editor.lineNumberAreaWidth()

    def paintEvent(self, event):
        self.code_editor.lineNumberAreaPaintEvent(event)


class CodeEditor(QPlainTextEdit):
    """
    몰랭 언어용 코드 에디터
    
    Follows Frontend Design Guideline: Abstracting Implementation Details
    """
    
    def __init__(self, initial_text=None):
        super().__init__()
        
        self._setup_editor()
        self._setup_line_numbers()
        self._setup_highlighter()
        
        # 초기 텍스트 설정
        sample_text = initial_text if initial_text is not None else DEFAULT_SAMPLE_CODE
        self.setPlainText(sample_text)
    
    def _setup_editor(self):
        """에디터 기본 설정을 초기화합니다."""
        # 폰트 설정
        font = self._get_monospace_font()
        self.setFont(font)
        
        # 에디터 스타일
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {EditorColors.BACKGROUND};
                color: {EditorColors.TEXT};
                selection-background-color: {EditorColors.SELECTION_BACKGROUND};
                selection-color: {EditorColors.SELECTION_TEXT};
                border: 1px solid {EditorColors.BORDER};
                font-family: 'Consolas', 'Monaco', monospace;
            }}
        """)
        
        # 탭 크기 설정
        self._setup_tab_size()
    
    def _get_monospace_font(self):
        """모노스페이스 폰트를 가져옵니다."""
        # 우선순위에 따라 폰트 시도
        font_candidates = ["Consolas", "Monaco", "monospace"]
        
        for font_name in font_candidates:
            font = QFont(font_name, DEFAULT_FONT_SIZE)
            if font.exactMatch():
                return font
        
        # 기본 폰트 반환
        return QFont("monospace", DEFAULT_FONT_SIZE)
    
    def _setup_tab_size(self):
        """탭 크기를 설정합니다."""
        metrics = self.fontMetrics()
        self.setTabStopDistance(TAB_SPACES * metrics.horizontalAdvance(' '))
    
    def _setup_line_numbers(self):
        """줄 번호 영역을 설정합니다."""
        self.line_number_area = LineNumberArea(self)
        
        # 시그널 연결
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        
        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()
    
    def _setup_highlighter(self):
        """구문 하이라이터를 설정합니다."""
        self.highlighter = HighlighterFactory.create_mollang_highlighter(self.document())
    
    def update_keywords(self, keywords):
        """키워드를 업데이트합니다."""
        if hasattr(self, 'highlighter'):
            self.highlighter.update_keywords(keywords)
    
    def get_keywords(self):
        """현재 키워드를 가져옵니다."""
        if hasattr(self, 'highlighter'):
            return self.highlighter.get_keywords()
        return {}
    
    def set_sample_code(self, code):
        """샘플 코드를 설정합니다."""
        self.setPlainText(code)
        if hasattr(self, 'highlighter'):
            self.highlighter.rehighlight()
    
    # Line number area methods
    def lineNumberAreaWidth(self):
        """줄 번호 영역 너비를 계산합니다."""
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num //= 10
            digits += 1
        
        from constants import LINE_NUMBER_PADDING
        space = LINE_NUMBER_PADDING + self.fontMetrics().horizontalAdvance('9') * digits
        return space
    
    def updateLineNumberAreaWidth(self, newBlockCount):
        """줄 번호 영역 너비를 업데이트합니다."""
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)
    
    def updateLineNumberArea(self, rect, dy):
        """줄 번호 영역을 업데이트합니다."""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), 
                                       self.line_number_area.width(), 
                                       rect.height())
        
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)
    
    def resizeEvent(self, event):
        """리사이즈 이벤트를 처리합니다."""
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(cr.left(), cr.top(), 
                                        self.lineNumberAreaWidth(), 
                                        cr.height())
    
    def lineNumberAreaPaintEvent(self, event):
        """줄 번호 영역을 그립니다."""
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(EditorColors.LINE_NUMBER_BACKGROUND))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor(EditorColors.LINE_NUMBER_TEXT))
                painter.drawText(0, int(top), self.line_number_area.width(), 
                               self.fontMetrics().height(), 
                               Qt.AlignmentFlag.AlignRight, number)
            
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1
    
    def highlightCurrentLine(self):
        """현재 줄을 하이라이트합니다."""
        extra_selections = []
        
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(EditorColors.CURRENT_LINE)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextCharFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        
        self.setExtraSelections(extra_selections)


class EditorManager:
    """
    에디터 상태 관리 클래스
    
    Follows Frontend Design Guideline: Scoping State Management
    """
    
    def __init__(self, editor: CodeEditor):
        self.editor = editor
        self._change_callbacks = []
    
    def set_text(self, text: str):
        """텍스트를 설정합니다."""
        self.editor.setPlainText(text)
        self._notify_change()
    
    def get_text(self) -> str:
        """현재 텍스트를 가져옵니다."""
        return self.editor.toPlainText()
    
    def insert_text(self, text: str):
        """현재 커서 위치에 텍스트를 삽입합니다."""
        cursor = self.editor.textCursor()
        cursor.insertText(text)
        self._notify_change()
    
    def clear(self):
        """에디터를 비웁니다."""
        self.editor.clear()
        self._notify_change()
    
    def on_change(self, callback):
        """텍스트 변경 시 호출될 콜백을 등록합니다."""
        self._change_callbacks.append(callback)
    
    def _notify_change(self):
        """텍스트 변경을 모든 콜백에 알립니다."""
        for callback in self._change_callbacks:
            try:
                callback(self.get_text())
            except Exception as e:
                print(f"에디터 변경 콜백 오류: {e}")
