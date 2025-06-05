"""
Configuration Management for Mollang IDE

Follows Frontend Design Guideline: Revealing Hidden Logic (Single Responsibility)
"""

import json
import os
from typing import Dict, Any, Optional, Tuple

from constants import CONFIG_FILENAME


class ConfigManager:
    """
    설정 파일 관리 클래스
    
    Follows Frontend Design Guideline: Single Responsibility - only handles config I/O
    """
    
    def __init__(self, config_filename: str = CONFIG_FILENAME):
        self.config_filename = config_filename
    
    def save_keywords(self, keywords: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        키워드 설정을 파일에 저장합니다.
        
        Returns:
            (success: bool, error_message: Optional[str])
        """
        try:
            with open(self.config_filename, 'w', encoding='utf-8') as f:
                json.dump(keywords, f, ensure_ascii=False, indent=2)
            return True, None
        except Exception as e:
            return False, str(e)
    
    def load_keywords(self) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        """
        키워드 설정을 파일에서 불러옵니다.
        
        Returns:
            (success: bool, keywords: Optional[Dict], error_message: Optional[str])
        """
        try:
            if not os.path.exists(self.config_filename):
                return False, None, "설정 파일이 존재하지 않습니다."
            
            with open(self.config_filename, 'r', encoding='utf-8') as f:
                keywords = json.load(f)
            return True, keywords, None
        except Exception as e:
            return False, None, str(e)
    
    def config_exists(self) -> bool:
        """설정 파일이 존재하는지 확인합니다."""
        return os.path.exists(self.config_filename)
    
    def backup_config(self, backup_suffix: str = ".backup") -> Tuple[bool, Optional[str]]:
        """
        현재 설정 파일을 백업합니다.
        
        Returns:
            (success: bool, error_message: Optional[str])
        """
        if not self.config_exists():
            return False, "백업할 설정 파일이 없습니다."
        
        backup_filename = self.config_filename + backup_suffix
        try:
            import shutil
            shutil.copy2(self.config_filename, backup_filename)
            return True, None
        except Exception as e:
            return False, str(e)


class ConfigValidator:
    """
    설정 데이터 검증 클래스
    
    Follows Frontend Design Guideline: Single Responsibility - only validates config
    """
    
    @staticmethod
    def is_valid_color(color: str) -> bool:
        """색상 값이 유효한지 확인합니다."""
        if not isinstance(color, str):
            return False
        
        # 간단한 hex 색상 검증
        if color.startswith('#') and len(color) == 7:
            try:
                int(color[1:], 16)
                return True
            except ValueError:
                return False
        
        return False
    
    @staticmethod
    def is_valid_keyword_category(category_data: Dict[str, Any]) -> bool:
        """키워드 카테고리 데이터가 유효한지 확인합니다."""
        if not isinstance(category_data, dict):
            return False
        
        required_keys = {'words', 'color'}
        if not required_keys.issubset(category_data.keys()):
            return False
        
        words = category_data.get('words')
        color = category_data.get('color')
        
        if not isinstance(words, list):
            return False
        
        if not all(isinstance(word, str) for word in words):
            return False
        
        if not ConfigValidator.is_valid_color(color):
            return False
        
        return True
    
    @staticmethod
    def validate_keywords_data(keywords: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        전체 키워드 데이터가 유효한지 확인합니다.
        
        Returns:
            (is_valid: bool, error_message: Optional[str])
        """
        if not isinstance(keywords, dict):
            return False, "키워드 데이터는 딕셔너리여야 합니다."
        
        for category_name, category_data in keywords.items():
            if not isinstance(category_name, str):
                return False, f"카테고리 이름은 문자열이어야 합니다: {category_name}"
            
            is_valid = ConfigValidator.is_valid_keyword_category(category_data)
            if not is_valid:
                return False, f"유효하지 않은 카테고리 데이터: {category_name}"
        
        return True, None


class ConfigService:
    """
    설정 관리 서비스 클래스
    
    Combines ConfigManager and ConfigValidator for higher-level operations
    """
    
    def __init__(self, config_filename: str = CONFIG_FILENAME):
        self.config_manager = ConfigManager(config_filename)
        self.validator = ConfigValidator()
    
    def save_keywords_with_validation(self, keywords: Dict[str, Any]) -> Tuple[bool, str]:
        """
        검증 후 키워드를 저장합니다.
        
        Returns:
            (success: bool, message: str)
        """
        # 검증
        is_valid, error_msg = self.validator.validate_keywords_data(keywords)
        if not is_valid:
            return False, f"검증 실패: {error_msg}"
        
        # 저장
        success, error_msg = self.config_manager.save_keywords(keywords)
        if success:
            return True, "설정 저장 완료!"
        else:
            return False, f"저장 실패: {error_msg}"
    
    def load_keywords_with_validation(self) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        """
        키워드를 불러오고 검증합니다.
        
        Returns:
            (success: bool, keywords: Optional[Dict], message: str)
        """
        # 로드
        success, keywords, error_msg = self.config_manager.load_keywords()
        if not success:
            return False, None, f"불러오기 실패: {error_msg}"
        
        # 검증
        is_valid, error_msg = self.validator.validate_keywords_data(keywords)
        if not is_valid:
            return False, None, f"유효하지 않은 설정 파일: {error_msg}"
        
        return True, keywords, "설정 불러오기 완료!"
