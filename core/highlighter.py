"""
Mollang Syntax Highlighter

Follows Frontend Design Guideline: Abstracting Implementation Details
"""

import re
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtCore import QRegularExpression

from constants import SyntaxColors
from core.keywords import MollangKeywords


class HighlightingRule:
    """
    단일 하이라이팅 규칙
    
    Follows Frontend Design Guideline: Single Responsibility
    """
    
    def __init__(self, pattern: str, color: str, bold: bool = True):
        self.pattern = QRegularExpression(pattern)
        self.format = QTextCharFormat()
        self.format.setForeground(QColor(color))
        if bold:
            self.format.setFontWeight(QFont.Weight.Bold)


class MollangHighlightingRules:
    """
    몰랭 언어 하이라이팅 규칙 생성기
    
    Follows Frontend Design Guideline: Organizing Code by Feature/Domain
    """
    
    @staticmethod
    def create_variable_rules():
        """변수 패턴 규칙들을 생성합니다."""
        rules = []
        
        # 기본 변수 패턴들
        variable_patterns = [
            r'\b몰\b',                    # 몰 단독
            r'\b모오+올\b',               # 모올, 모오올, 모오오올...
            r'\b모오+울\b',               # 모울, 모오울, 모오오울...
        ]
        
        for pattern in variable_patterns:
            rules.append(HighlightingRule(pattern, SyntaxColors.VARIABLE))
        
        return rules
    
    @staticmethod
    def create_string_io_rules():
        """문자열 입출력 규칙들을 생성합니다."""
        rules = []
        patterns = MollangKeywords.get_complex_patterns()["string_io"]
        
        for pattern in patterns:
            rules.append(HighlightingRule(pattern, SyntaxColors.STRING_IO))
        
        return rules
    
    @staticmethod
    def create_heap_memory_rules():
        """힙 메모리 규칙들을 생성합니다."""
        rules = []
        patterns = MollangKeywords.get_complex_patterns()["heap_memory"]
        
        for pattern in patterns:
            rules.append(HighlightingRule(pattern, SyntaxColors.HEAP_MEMORY))
        
        return rules
    
    @staticmethod
    def create_float_format_rules():
        """실수 포맷팅 규칙들을 생성합니다."""
        rules = []
        patterns = MollangKeywords.get_complex_patterns()["float_format"]
        
        for pattern in patterns:
            rules.append(HighlightingRule(pattern, SyntaxColors.EXIT_FORMAT))
        
        return rules
    
    @staticmethod
    def create_complex_keyword_rules():
        """복합 키워드 규칙들을 생성합니다."""
        rules = []
        patterns = MollangKeywords.get_complex_patterns()["complex_keywords"]
        
        for pattern in patterns:
            rules.append(HighlightingRule(pattern, SyntaxColors.KEYWORD_COMPLEX))
        
        return rules
    
    @staticmethod
    def create_operator_rules():
        """연산자 규칙들을 생성합니다."""
        rules = []
        
        # 연속 연산자 (먼저 처리)
        multi_patterns = MollangKeywords.get_complex_patterns()["multi_operators"]
        for pattern in multi_patterns:
            rules.append(HighlightingRule(pattern, SyntaxColors.OPERATOR_MULTI))
        
        # 단일 연산자
        single_patterns = MollangKeywords.get_complex_patterns()["single_operators"]
        for pattern in single_patterns:
            rules.append(HighlightingRule(pattern, SyntaxColors.OPERATOR_SINGLE))
        
        return rules
    
    @staticmethod
    def create_function_rules():
        """함수 관련 규칙들을 생성합니다."""
        rules = []
        
        # 함수명
        function_names = MollangKeywords.get_default_keywords()["함수명"]["words"]
        for func_name in function_names:
            pattern = f'\\b{re.escape(func_name)}\\b'
            rules.append(HighlightingRule(pattern, SyntaxColors.FUNCTION_NAME))
        
        return rules
    
    @staticmethod
    def create_simple_keyword_rules():
        """간단한 키워드 규칙들을 생성합니다."""
        rules = []
        
        # 간단한 입출력 키워드
        simple_keywords = ['루', '아']
        for keyword in simple_keywords:
            pattern = f'\\b{re.escape(keyword)}\\b'
            rules.append(HighlightingRule(pattern, SyntaxColors.KEYWORD_SIMPLE))
        
        # 종료 키워드
        rules.append(HighlightingRule(r'0ㅅ0', SyntaxColors.EXIT_FORMAT))
        
        return rules
    
    @staticmethod
    def create_punctuation_rules():
        """구두점 규칙들을 생성합니다."""
        rules = []
        pattern = r'[(),]'
        rules.append(HighlightingRule(pattern, SyntaxColors.PUNCTUATION, bold=False))
        return rules


class MollangSyntaxHighlighter(QSyntaxHighlighter):
    """
    몰랭 언어 구문 하이라이터
    
    Follows Frontend Design Guideline: Separating Code Paths for Conditional Rendering
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._keywords = MollangKeywords.get_default_keywords()
        self._setup_highlighting_rules()
    
    def update_keywords(self, new_keywords):
        """키워드를 업데이트하고 재하이라이팅합니다."""
        if MollangKeywords.validate_keyword_data(new_keywords):
            self._keywords = new_keywords
            self._setup_highlighting_rules()
            self.rehighlight()
    
    def get_keywords(self):
        """현재 키워드를 반환합니다."""
        return self._keywords.copy()
    
    def _setup_highlighting_rules(self):
        """
        하이라이팅 규칙을 설정합니다.
        
        중요: 우선순위에 따라 규칙을 적용합니다.
        더 구체적인 패턴이 더 일반적인 패턴보다 먼저 와야 합니다.
        """
        self.highlighting_rules = []
        
        # 1순위: 문자열 입출력 (가장 구체적)
        self.highlighting_rules.extend(MollangHighlightingRules.create_string_io_rules())
        
        # 2순위: 힙 메모리 패턴
        self.highlighting_rules.extend(MollangHighlightingRules.create_heap_memory_rules())
        
        # 3순위: 실수 포맷팅
        self.highlighting_rules.extend(MollangHighlightingRules.create_float_format_rules())
        
        # 4순위: 복합 키워드
        self.highlighting_rules.extend(MollangHighlightingRules.create_complex_keyword_rules())
        
        # 5순위: 연산자 (연속 -> 단일 순서)
        self.highlighting_rules.extend(MollangHighlightingRules.create_operator_rules())
        
        # 6순위: 함수 관련
        self.highlighting_rules.extend(MollangHighlightingRules.create_function_rules())
        
        # 7순위: 변수 (더 일반적인 패턴)
        self.highlighting_rules.extend(MollangHighlightingRules.create_variable_rules())
        
        # 8순위: 간단한 키워드
        self.highlighting_rules.extend(MollangHighlightingRules.create_simple_keyword_rules())
        
        # 9순위: 구두점 (가장 일반적)
        self.highlighting_rules.extend(MollangHighlightingRules.create_punctuation_rules())
        
        # 사용자 정의 키워드 추가
        self._add_custom_keyword_rules()
    
    def _add_custom_keyword_rules(self):
        """사용자 정의 키워드 규칙을 추가합니다."""
        for category, data in self._keywords.items():
            words = data.get('words', [])
            color = data.get('color', SyntaxColors.KEYWORD_SIMPLE)
            
            for word in words:
                # 기본 키워드와 중복되지 않는 경우만 추가
                if not self._is_default_keyword(word):
                    pattern = f'\\b{re.escape(word)}\\b'
                    rule = HighlightingRule(pattern, color)
                    self.highlighting_rules.append(rule)
    
    def _is_default_keyword(self, word):
        """기본 키워드인지 확인합니다."""
        default_keywords = MollangKeywords.get_default_keywords()
        for category_data in default_keywords.values():
            if word in category_data.get('words', []):
                return True
        return False
    
    def highlightBlock(self, text):
        """
        텍스트 블록에 하이라이팅을 적용합니다.
        
        Follows Frontend Design Guideline: Reducing Eye Movement
        """
        # 모든 규칙을 텍스트에 적용
        for rule in self.highlighting_rules:
            match_iterator = rule.pattern.globalMatch(text)
            
            while match_iterator.hasNext():
                match = match_iterator.next()
                start_index = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start_index, length, rule.format)


class HighlighterFactory:
    """
    하이라이터 생성 팩토리
    
    Follows Frontend Design Guideline: Avoiding Premature Abstraction
    """
    
    @staticmethod
    def create_mollang_highlighter(parent=None, initial_keywords=None):
        """몰랭 하이라이터를 생성합니다."""
        highlighter = MollangSyntaxHighlighter(parent)
        
        if initial_keywords and MollangKeywords.validate_keyword_data(initial_keywords):
            highlighter.update_keywords(initial_keywords)
        
        return highlighter
