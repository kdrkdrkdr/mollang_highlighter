"""
Dialog Components for Mollang IDE

Follows Frontend Design Guideline: Separating Code Paths for Conditional Rendering
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QFormLayout, 
    QLineEdit, QDialogButtonBox, QColorDialog, QLabel, QListWidget, 
    QListWidgetItem, QGroupBox, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from core.keywords import KeywordManager


class KeywordEditDialog(QDialog):
    """
    키워드 편집 다이얼로그
    
    Follows Frontend Design Guideline: Single Responsibility
    """
    
    def __init__(self, category="", word="", color="#FF0000", existing_categories=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("키워드 편집")
        self.setModal(True)
        
        self.color = color
        self.existing_categories = existing_categories or []
        
        self._setup_ui()
        self._populate_data(category, word)
    
    def _setup_ui(self):
        """UI를 설정합니다."""
        layout = QFormLayout()
        self.setLayout(layout)
        
        # 카테고리 입력
        self.category_edit = QLineEdit()
        layout.addRow("카테고리:", self.category_edit)
        
        # 키워드 입력
        self.word_edit = QLineEdit()
        layout.addRow("키워드:", self.word_edit)
        
        # 색상 선택
        self._setup_color_selection(layout)
        
        # 버튼
        self._setup_buttons(layout)
    
    def _setup_color_selection(self, layout):
        """색상 선택 UI를 설정합니다."""
        color_layout = QHBoxLayout()
        
        self.color_label = QLabel("색상 미리보기")
        self._update_color_preview()
        
        self.color_btn = QPushButton("색상 선택")
        self.color_btn.clicked.connect(self._choose_color)
        
        color_layout.addWidget(self.color_label)
        color_layout.addWidget(self.color_btn)
        layout.addRow("색상:", color_layout)
    
    def _setup_buttons(self, layout):
        """버튼을 설정합니다."""
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._validate_and_accept)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)
    
    def _populate_data(self, category, word):
        """기존 데이터를 폼에 채웁니다."""
        self.category_edit.setText(category)
        self.word_edit.setText(word)
    
    def _update_color_preview(self):
        """색상 미리보기를 업데이트합니다."""
        self.color_label.setStyleSheet(
            f"background-color: {self.color}; "
            f"border: 1px solid black; "
            f"padding: 5px;"
        )
    
    def _choose_color(self):
        """색상 선택 다이얼로그를 엽니다."""
        color = QColorDialog.getColor(QColor(self.color), self)
        if color.isValid():
            self.color = color.name()
            self._update_color_preview()
    
    def _validate_and_accept(self):
        """입력을 검증하고 다이얼로그를 닫습니다."""
        category = self.category_edit.text().strip()
        word = self.word_edit.text().strip()
        
        if not category:
            self._show_error("카테고리를 입력해주세요.")
            return
        
        if not word:
            self._show_error("키워드를 입력해주세요.")
            return
        
        self.accept()
    
    def _show_error(self, message):
        """에러 메시지를 표시합니다."""
        QMessageBox.warning(self, "입력 오류", message)
    
    def get_values(self):
        """입력된 값들을 반환합니다."""
        return (
            self.category_edit.text().strip(),
            self.word_edit.text().strip(),
            self.color
        )


class KeywordListWidget(QListWidget):
    """
    키워드 목록 위젯
    
    Follows Frontend Design Guideline: Abstracting Implementation Details
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keywords_data = {}
    
    def update_keywords(self, keywords):
        """키워드 목록을 업데이트합니다."""
        self.keywords_data = keywords
        self._refresh_list()
    
    def _refresh_list(self):
        """리스트를 새로고침합니다."""
        self.clear()
        
        for category, data in self.keywords_data.items():
            words = data.get('words', [])
            color = data.get('color', '#000000')
            
            for word in words:
                self._add_keyword_item(category, word, color)
    
    def _add_keyword_item(self, category, word, color):
        """키워드 아이템을 추가합니다."""
        item = QListWidgetItem(f"[{category}] {word}")
        item.setForeground(QColor(color))
        item.setData(Qt.ItemDataRole.UserRole, (category, word))
        self.addItem(item)
    
    def get_selected_keyword(self):
        """선택된 키워드를 반환합니다."""
        current_item = self.currentItem()
        if current_item:
            return current_item.data(Qt.ItemDataRole.UserRole)
        return None


class KeywordControlPanel(QGroupBox):
    """
    키워드 조작 패널
    
    Follows Frontend Design Guideline: Eliminating Props Drilling with Composition
    """
    
    def __init__(self, keyword_list: KeywordListWidget, keyword_manager: KeywordManager, parent=None):
        super().__init__("키워드 목록", parent)
        self.keyword_list = keyword_list
        self.keyword_manager = keyword_manager
        
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """UI를 설정합니다."""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 키워드 리스트 추가
        layout.addWidget(self.keyword_list)
        
        # 버튼 패널
        self._setup_button_panel(layout)
    
    def _setup_button_panel(self, layout):
        """버튼 패널을 설정합니다."""
        button_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("추가")
        self.edit_btn = QPushButton("편집")
        self.delete_btn = QPushButton("삭제")
        
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        
        layout.addLayout(button_layout)
    
    def _connect_signals(self):
        """시그널을 연결합니다."""
        self.add_btn.clicked.connect(self._add_keyword)
        self.edit_btn.clicked.connect(self._edit_keyword)
        self.delete_btn.clicked.connect(self._delete_keyword)
    
    def _add_keyword(self):
        """키워드를 추가합니다."""
        existing_categories = list(self.keyword_manager.get_keywords().keys())
        dialog = KeywordEditDialog(
            existing_categories=existing_categories, 
            parent=self
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            category, word, color = dialog.get_values()
            success = self.keyword_manager.add_keyword(category, word, color)
            
            if success:
                self.keyword_list.update_keywords(self.keyword_manager.get_keywords())
            else:
                QMessageBox.warning(self, "추가 실패", "키워드 추가에 실패했습니다.")
    
    def _edit_keyword(self):
        """키워드를 편집합니다."""
        selected = self.keyword_list.get_selected_keyword()
        if not selected:
            QMessageBox.information(self, "선택 필요", "편집할 키워드를 선택해주세요.")
            return
        
        category, word = selected
        keywords = self.keyword_manager.get_keywords()
        color = keywords[category]['color']
        
        existing_categories = list(keywords.keys())
        dialog = KeywordEditDialog(
            category, word, color, 
            existing_categories=existing_categories,
            parent=self
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_category, new_word, new_color = dialog.get_values()
            success = self.keyword_manager.update_keyword(
                category, word, new_category, new_word, new_color
            )
            
            if success:
                self.keyword_list.update_keywords(self.keyword_manager.get_keywords())
            else:
                QMessageBox.warning(self, "편집 실패", "키워드 편집에 실패했습니다.")
    
    def _delete_keyword(self):
        """키워드를 삭제합니다."""
        selected = self.keyword_list.get_selected_keyword()
        if not selected:
            QMessageBox.information(self, "선택 필요", "삭제할 키워드를 선택해주세요.")
            return
        
        category, word = selected
        
        reply = QMessageBox.question(
            self, "삭제 확인", 
            f"키워드 '{word}'를 삭제하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success = self.keyword_manager.remove_keyword(category, word)
            
            if success:
                self.keyword_list.update_keywords(self.keyword_manager.get_keywords())
            else:
                QMessageBox.warning(self, "삭제 실패", "키워드 삭제에 실패했습니다.")


class KeywordConfigDialog(QDialog):
    """
    키워드 설정 메인 다이얼로그
    
    Follows Frontend Design Guideline: Eliminating Props Drilling with Composition
    """
    
    def __init__(self, current_keywords, parent=None):
        super().__init__(parent)
        self.setWindowTitle("키워드 설정")
        self.setModal(True)
        self.resize(500, 400)
        
        # 키워드 매니저 초기화
        self.keyword_manager = KeywordManager()
        self.keyword_manager.set_keywords(current_keywords)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """UI를 설정합니다."""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 키워드 리스트와 컨트롤 패널
        keyword_list = KeywordListWidget()
        self.control_panel = KeywordControlPanel(keyword_list, self.keyword_manager)
        layout.addWidget(self.control_panel)
        
        # 초기 키워드 로드
        keyword_list.update_keywords(self.keyword_manager.get_keywords())
        
        # 확인/취소 버튼
        self._setup_buttons(layout)
    
    def _setup_buttons(self, layout):
        """버튼을 설정합니다."""
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def get_keywords(self):
        """편집된 키워드를 반환합니다."""
        return self.keyword_manager.get_keywords()


class MessageHelper:
    """
    메시지 표시 헬퍼 클래스
    
    Follows Frontend Design Guideline: Standardizing Return Types
    """
    
    @staticmethod
    def show_success(parent, title, message):
        """성공 메시지를 표시합니다."""
        QMessageBox.information(parent, title, message)
    
    @staticmethod
    def show_error(parent, title, message):
        """에러 메시지를 표시합니다."""
        QMessageBox.critical(parent, title, message)
    
    @staticmethod
    def show_warning(parent, title, message):
        """경고 메시지를 표시합니다."""
        QMessageBox.warning(parent, title, message)
    
    @staticmethod
    def ask_confirmation(parent, title, message):
        """확인 다이얼로그를 표시합니다."""
        reply = QMessageBox.question(
            parent, title, message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes
