"""
Main Window Component for Mollang IDE

Follows Frontend Design Guideline: Eliminating Props Drilling with Composition
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QSplitter, QTextBrowser
)
from PySide6.QtCore import Qt

from constants import (
    MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT, MAIN_WINDOW_X, MAIN_WINDOW_Y,
    GUIDE_PANEL_MAX_WIDTH, SPLITTER_EDITOR_WIDTH, GuideColors,
    SIMPLE_TEST_CODE, FULL_TEST_CODE
)
from components.editor import CodeEditor, EditorManager
from components.dialogs import KeywordConfigDialog, MessageHelper
from core import ConfigService, KeywordManager


class ToolbarManager:
    """
    툴바 관리 클래스
    
    Follows Frontend Design Guideline: Scoping State Management
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.buttons = {}
        self._create_buttons()
    
    def _create_buttons(self):
        """버튼들을 생성합니다."""
        button_configs = [
            ("config", "키워드 설정"),
            ("save", "설정 저장"),
            ("load", "설정 불러오기"),
            ("simple_test", "간단 테스트"),
            ("full_test", "전체 테스트")
        ]
        
        for key, text in button_configs:
            self.buttons[key] = QPushButton(text)
    
    def get_layout(self):
        """툴바 레이아웃을 반환합니다."""
        layout = QHBoxLayout()
        
        for button in self.buttons.values():
            layout.addWidget(button)
        
        layout.addStretch()
        return layout
    
    def connect_signals(self, callback_map):
        """시그널을 연결합니다."""
        for key, callback in callback_map.items():
            if key in self.buttons:
                self.buttons[key].clicked.connect(callback)


class GuidePanel(QTextBrowser):
    """
    가이드 패널 컴포넌트
    
    Follows Frontend Design Guideline: Single Responsibility
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_appearance()
        self._setup_content()
    
    def _setup_appearance(self):
        """패널 외관을 설정합니다."""
        self.setMaximumWidth(GUIDE_PANEL_MAX_WIDTH)
        self.setStyleSheet(f"""
            QTextBrowser {{
                background-color: {GuideColors.BACKGROUND};
                color: {GuideColors.TEXT};
                border: 1px solid {GuideColors.BORDER};
            }}
        """)
    
    def _setup_content(self):
        """가이드 내용을 설정합니다."""
        guide_content = self._get_guide_html()
        self.setHtml(guide_content)
    
    def _get_guide_html(self):
        """가이드 HTML 콘텐츠를 반환합니다."""
        return '''
<h3 style="color: #FF6B35;">완전한 몰랭 구문 하이라이터</h3>

<h4 style="color: #2196F3;">📋 지원하는 모든 문법</h4>

<p><span style="color: #00FFFF; font-weight: bold;">청록색</span> - 변수<br>
<span style="font-family: monospace;">몰, 모올, 모오올, 모오오올...</span></p>

<p><span style="color: #2196F3; font-weight: bold;">파란색</span> - 입출력<br>
<span style="font-family: monospace;">루, 아</span></p>

<p><span style="color: #FF6B35; font-weight: bold;">주황색</span> - 제어문<br>
<span style="font-family: monospace;">은?행, 털!자, 돌!자, 짓!자, 가!자, 가자!, 루?, 루!</span></p>

<p><span style="color: #FFC107; font-weight: bold;">황색</span> - 기본 연산자<br>
<span style="font-family: monospace;">?, !, ., *, ~, =, &</span></p>

<p><span style="color: #FF9800; font-weight: bold;">진한주황</span> - 연속 연산자<br>
<span style="font-family: monospace;">??, !!!, .., ..., ....</span></p>

<p><span style="color: #E91E63; font-weight: bold;">분홍색</span> - 힙 메모리<br>
<span style="font-family: monospace;">몰*모올, 몰~모올, 몰=모올, &몰~모올</span></p>

<p><span style="color: #00E676; font-weight: bold;">밝은녹색</span> - 문자열 입출력<br>
<span style="font-family: monospace;">몰~몰루?, 몰~몰루</span></p>

<p><span style="color: #4CAF50; font-weight: bold;">녹색</span> - 함수명<br>
<span style="font-family: monospace;">뭵뤩, 말랑, 머리, 무릎...</span></p>

<p><span style="color: #FF5722; font-weight: bold;">깊은주황</span> - 함수 호출<br>
<span style="font-family: monospace;">머리은?행...가!자</span></p>

<p><span style="color: #9C27B0; font-weight: bold;">보라색</span> - 종료/포맷<br>
<span style="font-family: monospace;">0ㅅ0, 루!</span></p>

<h4 style="color: #4CAF50;">🎯 테스트 버튼</h4>
<ul>
<li><b>간단 테스트</b>: 기본 변수와 출력</li>
<li><b>전체 테스트</b>: 모든 문법 요소 포함</li>
</ul>

<h4 style="color: #E91E63;">🚀 새로 추가된 기능</h4>
<ul>
<li>실수 포맷팅: <code style="color: #9C27B0;">??.????루!</code></li>
<li>문자열 입출력: <code style="color: #00E676;">몰~몰루?</code></li>
<li>힙 메모리 길이: <code style="color: #E91E63;">&몰~모올</code></li>
<li>함수 호출 패턴: <code style="color: #FF5722;">머리은?행...가!자</code></li>
<li>변수 조합: <code style="color: #00FFFF;">몰모올모오올</code></li>
</ul>

<hr>
<p><small>이제 몰랭의 모든 문법이 정확히 하이라이팅됩니다!</small></p>
        '''


class MainWindowController:
    """
    메인 윈도우 컨트롤러
    
    Follows Frontend Design Guideline: Scoping State Management
    """
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.config_service = ConfigService()
        self.keyword_manager = KeywordManager()
        
        # 키워드 변경 시 에디터 업데이트
        self.keyword_manager.on_change(self._on_keywords_changed)
    
    def open_keyword_config(self):
        """키워드 설정 다이얼로그를 엽니다."""
        current_keywords = self.keyword_manager.get_keywords()
        dialog = KeywordConfigDialog(current_keywords, self.main_window)
        
        if dialog.exec() == dialog.DialogCode.Accepted:
            new_keywords = dialog.get_keywords()
            self.keyword_manager.set_keywords(new_keywords)
    
    def save_config(self):
        """설정을 저장합니다."""
        keywords = self.keyword_manager.get_keywords()
        success, message = self.config_service.save_keywords_with_validation(keywords)
        
        if success:
            MessageHelper.show_success(self.main_window, "저장 완료", message)
        else:
            MessageHelper.show_error(self.main_window, "저장 실패", message)
    
    def load_config(self):
        """설정을 불러옵니다."""
        success, keywords, message = self.config_service.load_keywords_with_validation()
        
        if success:
            self.keyword_manager.set_keywords(keywords)
            MessageHelper.show_success(self.main_window, "불러오기 완료", message)
        else:
            MessageHelper.show_error(self.main_window, "불러오기 실패", message)
    
    def simple_test(self):
        """간단한 테스트 코드를 설정합니다."""
        self.main_window.editor_manager.set_text(SIMPLE_TEST_CODE)
    
    def full_test(self):
        """전체 테스트 코드를 설정합니다."""
        self.main_window.editor_manager.set_text(FULL_TEST_CODE)
    
    def _on_keywords_changed(self, keywords):
        """키워드 변경 시 에디터를 업데이트합니다."""
        self.main_window.code_editor.update_keywords(keywords)


class MainWindow(QMainWindow):
    """
    메인 윈도우 클래스
    
    Follows Frontend Design Guideline: Eliminating Props Drilling with Composition
    """
    
    def __init__(self):
        super().__init__()
        self._setup_window()
        self._create_components()
        self._setup_layout()
        self._connect_controller()
    
    def _setup_window(self):
        """윈도우 기본 설정을 초기화합니다."""
        self.setWindowTitle("완전한 몰랭 IDE - 모든 문법 지원")
        self.setGeometry(MAIN_WINDOW_X, MAIN_WINDOW_Y, 
                        MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
    
    def _create_components(self):
        """컴포넌트들을 생성합니다."""
        # 코드 에디터
        self.code_editor = CodeEditor()
        self.editor_manager = EditorManager(self.code_editor)
        
        # 툴바
        self.toolbar_manager = ToolbarManager(self)
        
        # 가이드 패널
        self.guide_panel = GuidePanel()
    
    def _setup_layout(self):
        """레이아웃을 설정합니다."""
        # 메인 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 툴바 추가
        toolbar_layout = self.toolbar_manager.get_layout()
        main_layout.addLayout(toolbar_layout)
        
        # 에디터와 가이드 패널
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.code_editor)
        splitter.addWidget(self.guide_panel)
        splitter.setSizes([SPLITTER_EDITOR_WIDTH, GUIDE_PANEL_MAX_WIDTH])
        
        main_layout.addWidget(splitter)
    
    def _connect_controller(self):
        """컨트롤러를 연결합니다."""
        self.controller = MainWindowController(self)
        
        # 툴바 시그널 연결
        callback_map = {
            "config": self.controller.open_keyword_config,
            "save": self.controller.save_config,
            "load": self.controller.load_config,
            "simple_test": self.controller.simple_test,
            "full_test": self.controller.full_test
        }
        
        self.toolbar_manager.connect_signals(callback_map)


class WindowFactory:
    """
    윈도우 생성 팩토리
    
    Follows Frontend Design Guideline: Avoiding Premature Abstraction
    """
    
    @staticmethod
    def create_main_window():
        """메인 윈도우를 생성합니다."""
        return MainWindow()
    
    @staticmethod
    def create_keyword_config_dialog(current_keywords, parent=None):
        """키워드 설정 다이얼로그를 생성합니다."""
        return KeywordConfigDialog(current_keywords, parent)
