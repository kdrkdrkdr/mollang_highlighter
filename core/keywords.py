"""
Mollang Language Keywords Management

Follows Frontend Design Guideline: Organizing Code by Feature/Domain
"""

from constants import SyntaxColors


class MollangKeywords:
    """
    Mollang 언어의 키워드 정의와 관리
    
    Follows Frontend Design Guideline: Cohesion - keeps related keywords together
    """
    
    @staticmethod
    def get_default_keywords():
        """기본 키워드 설정을 반환합니다."""
        return {
            "제어_키워드": {
                "words": ["은?행", "털!자", "돌!자", "짓!자"],
                "color": SyntaxColors.KEYWORD_COMPLEX
            },
            "점프_키워드": {
                "words": ["가!자", "가자!"],
                "color": SyntaxColors.KEYWORD_COMPLEX
            },
            "입출력_키워드": {
                "words": ["루", "루?", "루!", "아"],
                "color": SyntaxColors.KEYWORD_SIMPLE
            },
            "종료_키워드": {
                "words": ["0ㅅ0"],
                "color": SyntaxColors.EXIT_FORMAT
            },
            "함수명": {
                "words": ["뭵뤩", "뭵뤡", "말랑", "머리", "무릎", "망령", "매립", "무리", "밀랍"],
                "color": SyntaxColors.FUNCTION_NAME
            }
        }
    
    @staticmethod
    def get_variable_patterns():
        """변수 패턴들을 반환합니다."""
        return [
            r'\b몰\b',                    # 몰 단독
            r'\b모오+올\b',               # 모올, 모오올, 모오오올...
            r'\b모오+울\b',               # 모울, 모오울, 모오오울...
        ]
    
    @staticmethod
    def get_complex_patterns():
        """복합 패턴들을 반환합니다."""
        return {
            "complex_keywords": [
                r'은\?행',    # 은?행
                r'털!자',     # 털!자  
                r'돌!자',     # 돌!자
                r'짓!자',     # 짓!자
                r'가!자',     # 가!자
                r'가자!',     # 가자!
                r'루\?',      # 루?
                r'루!',       # 루!
            ],
            "multi_operators": [
                r'\.{4,}',      # .... (나머지)
                r'\.{3}',       # ... (정수 나눗셈)  
                r'\.{2}',       # .. (나눗셈)
                r'\?{2,}',      # ?? (증가)
                r'!{2,}',       # !! (감소)
            ],
            "single_operators": [
                r'\?', r'!', r'\.', r'\*', r'~', r'=', r'&'
            ],
            "string_io": [
                # 문자열 입력 전체: 변수~변수루?
                r'(?:몰|모오+올|모오+울)~(?:몰|모오+올|모오+울)루\?',
                # 문자열 출력 전체: 변수~변수루  
                r'(?:몰|모오+올|모오+울)~(?:몰|모오+올|모오+울)루(?!\?)'
            ],
            "heap_memory": [
                # 힙 길이 계산: &변수~변수
                r'&(?:몰|모오+올|모오+울)~(?:몰|모오+올|모오+울)',
                # 힙 메모리 접근: 변수[*~=]변수
                r'(?:몰|모오+올|모오+울)[\*~=](?:몰|모오+올|모오+울)'
            ],
            "float_format": [
                # 실수 포맷: 연산자들루!
                r'[\?\!\.\,]+루!'
            ]
        }
    
    @staticmethod
    def validate_keyword_data(keywords):
        """키워드 데이터가 유효한지 확인합니다."""
        if not isinstance(keywords, dict):
            return False
        
        for category, data in keywords.items():
            if not isinstance(data, dict):
                return False
            if 'words' not in data or 'color' not in data:
                return False
            if not isinstance(data['words'], list):
                return False
            if not isinstance(data['color'], str):
                return False
        
        return True


class KeywordManager:
    """
    키워드 상태 관리 클래스
    
    Follows Frontend Design Guideline: Scoping State Management
    """
    
    def __init__(self):
        self._keywords = MollangKeywords.get_default_keywords()
        self._change_callbacks = []
    
    def get_keywords(self):
        """현재 키워드를 반환합니다."""
        return self._keywords.copy()
    
    def set_keywords(self, new_keywords):
        """키워드를 설정하고 변경 콜백을 호출합니다."""
        if MollangKeywords.validate_keyword_data(new_keywords):
            self._keywords = new_keywords.copy()
            self._notify_change()
            return True
        return False
    
    def add_keyword(self, category, word, color):
        """새 키워드를 추가합니다."""
        if category not in self._keywords:
            self._keywords[category] = {'words': [], 'color': color}
        
        if word not in self._keywords[category]['words']:
            self._keywords[category]['words'].append(word)
            self._keywords[category]['color'] = color
            self._notify_change()
            return True
        return False
    
    def remove_keyword(self, category, word):
        """키워드를 제거합니다."""
        if category in self._keywords and word in self._keywords[category]['words']:
            self._keywords[category]['words'].remove(word)
            if not self._keywords[category]['words']:
                del self._keywords[category]
            self._notify_change()
            return True
        return False
    
    def update_keyword(self, old_category, old_word, new_category, new_word, new_color):
        """기존 키워드를 수정합니다."""
        # 기존 키워드 제거
        self.remove_keyword(old_category, old_word)
        # 새 키워드 추가
        return self.add_keyword(new_category, new_word, new_color)
    
    def on_change(self, callback):
        """키워드 변경 시 호출될 콜백을 등록합니다."""
        self._change_callbacks.append(callback)
    
    def _notify_change(self):
        """키워드 변경을 모든 콜백에 알립니다."""
        for callback in self._change_callbacks:
            try:
                callback(self._keywords)
            except Exception as e:
                print(f"키워드 변경 콜백 오류: {e}")
