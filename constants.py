"""
Constants for Mollang IDE

Follows Frontend Design Guideline: Naming Magic Numbers
"""

# UI Constants
MAIN_WINDOW_WIDTH = 1400
MAIN_WINDOW_HEIGHT = 900
MAIN_WINDOW_X = 100
MAIN_WINDOW_Y = 100

GUIDE_PANEL_MAX_WIDTH = 350
SPLITTER_EDITOR_WIDTH = 1000

# Editor Constants
DEFAULT_FONT_SIZE = 12
TAB_SPACES = 4
LINE_NUMBER_PADDING = 3

# Colors
class EditorColors:
    BACKGROUND = "#1e1e1e"
    TEXT = "#ffffff"
    SELECTION_BACKGROUND = "#0078d4"
    SELECTION_TEXT = "#ffffff"
    BORDER = "#404040"
    LINE_NUMBER_BACKGROUND = "#2d2d30"
    LINE_NUMBER_TEXT = "#858585"
    CURRENT_LINE = "#2a2d2e"

class GuideColors:
    BACKGROUND = "#252526"
    TEXT = "#cccccc"
    BORDER = "#404040"

# Syntax Highlighting Colors
class SyntaxColors:
    VARIABLE = "#00FFFF"          # 청록색 - 변수
    KEYWORD_SIMPLE = "#2196F3"    # 파란색 - 간단 키워드
    KEYWORD_COMPLEX = "#FF6B35"   # 주황색 - 복합 키워드  
    OPERATOR_SINGLE = "#FFC107"   # 황색 - 단일 연산자
    OPERATOR_MULTI = "#FF9800"    # 진한 주황색 - 연속 연산자
    HEAP_MEMORY = "#E91E63"       # 분홍색 - 힙 메모리
    STRING_IO = "#00E676"         # 밝은 녹색 - 문자열 입출력
    FUNCTION_NAME = "#4CAF50"     # 녹색 - 함수명
    FUNCTION_CALL = "#FF5722"     # 깊은 주황색 - 함수 호출
    EXIT_FORMAT = "#9C27B0"       # 보라색 - 종료/포맷
    PUNCTUATION = "#9E9E9E"       # 회색 - 괄호와 쉼표

# File Constants
CONFIG_FILENAME = "mollang_keywords.json"

# Sample Code Templates
SIMPLE_TEST_CODE = '''몰?
몰루'''

FULL_TEST_CODE = '''몰? 모올?? 모오올???
몰루 모올루 모오올루

은?행 털!자 돌!자 짓!자 가!자 가자!
루? 루! 아 0ㅅ0

??.????루!

몰~몰루? 몰~몰루

몰*모올? 몰=모올몰*모올 &몰~모올루

머리 은?행 몰,모올,모오올
    몰모올모오올루
    몰.모올..모오올...모오오올....모오오오올루
짓!자

머리 은?행 ???가!자

뭵뤩 말랑 무릎 망령 매립 무리 밀랍'''

DEFAULT_SAMPLE_CODE = '''몰?
몰루

몰????.??????????? 모올????.????.?? 모오올몰모올
아모오올!!!!루 모오올모올 아모오올!!!!!!!루 아모오올루 아모오올루
아모오올???루 아몰루 아모올루 몰모올 아몰???????????루 아모오올???루
아몰모올??????루 아모오올루 아모오올!!!!!!!!루 아모올?루

??.????루!

몰~몰루?
몰~몰루

머리 은?행 몰,모올,모오올
몰*모올?
몰=모올몰*모올
모오올~~루
짓!자

머리 은?행 몰가!자

몰?....?? 은?행
가???자!
털!자

&몰~몰루

0ㅅ0?'''
