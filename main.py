"""
Mollang IDE Main Application

Entry point for the Mollang language IDE with syntax highlighting.
Follows Frontend Design Guideline: Single Responsibility for main entry point.
"""

import sys
from PySide6.QtWidgets import QApplication

from components import WindowFactory


class MollangIDEApplication:
    """
    몰랭 IDE 애플리케이션 클래스
    
    Follows Frontend Design Guideline: Single Responsibility
    """
    
    def __init__(self):
        self.app = None
        self.main_window = None
    
    def initialize(self):
        """애플리케이션을 초기화합니다."""
        self.app = QApplication(sys.argv)
        self.app.setStyle('Fusion')
        
        # 메인 윈도우 생성
        self.main_window = WindowFactory.create_main_window()
    
    def run(self):
        """애플리케이션을 실행합니다."""
        if not self.app or not self.main_window:
            raise RuntimeError("애플리케이션이 초기화되지 않았습니다. initialize()를 먼저 호출하세요.")
        
        self.main_window.show()
        return self.app.exec()


def main():
    """
    메인 함수
    
    Follows Frontend Design Guideline: Revealing Hidden Logic
    """
    try:
        # 애플리케이션 생성 및 초기화
        app = MollangIDEApplication()
        app.initialize()
        
        # 애플리케이션 실행
        exit_code = app.run()
        
        # 정상 종료
        sys.exit(exit_code)
        
    except Exception as e:
        print(f"애플리케이션 실행 중 오류 발생: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
