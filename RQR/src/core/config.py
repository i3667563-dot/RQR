"""
Конфигурация игры.
Пути к файлам, настройки, константы.
"""

import os
from pathlib import Path


class Config:
    """
    Класс конфигурации игры.
    
    Хранит все пути и настройки в одном месте для удобного доступа.
    Модифицируйте этот класс для изменения базовых настроек игры.
    
    Attributes:
        PROJECT_ROOT: Корневая директория проекта
        DATA_DIR: Директория с данными
        QUESTIONS_FILE: Путь к файлу с вопросами
        COMMENTS_DIR: Директория с комментариями
        INTRO_COMMENTS_FILE: Путь к вступительным комментариям
        CORRECT_COMMENTS_FILE: Путь к комментариям при правильном ответе
        WRONG_COMMENTS_FILE: Путь к комментариям при неправильном ответе
    """
    
    # Корневая директория проекта (автоматически определяется)
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    
    # Директория с данными
    DATA_DIR = PROJECT_ROOT / "data"
    
    # Файлы данных
    QUESTIONS_FILE = DATA_DIR / "questions.json"
    
    # Директория с комментариями
    COMMENTS_DIR = DATA_DIR / "comments"
    
    # Файлы комментариев
    INTRO_COMMENTS_FILE = COMMENTS_DIR / "intro_comments.json"
    CORRECT_COMMENTS_FILE = COMMENTS_DIR / "correct_comments.json"
    WRONG_COMMENTS_FILE = COMMENTS_DIR / "wrong_comments.json"
    
    # Настройки игры
    GAME_TITLE = "Russian Quiz Remake"
    GAME_VERSION = "1.0.0"
    
    # Настройки отображения
    MAX_OPTIONS_DISPLAY = 4  # Максимальное количество вариантов для отображения
    
    # Настройки scoring
    POINTS_PER_CORRECT = 10  # Очков за правильный ответ
    BONUS_POINTS_STREAK = 5  # Бонусных очков за серию правильных ответов
    
    @classmethod
    def get_data_path(cls, filename: str) -> Path:
        """
        Получить полный путь к файлу в директории data.
        
        Args:
            filename: Имя файла в директории data
            
        Returns:
            Полный путь к файлу
        """
        return cls.DATA_DIR / filename
    
    @classmethod
    def get_comments_path(cls, filename: str) -> Path:
        """
        Получить полный путь к файлу комментариев.
        
        Args:
            filename: Имя файла в директории comments
            
        Returns:
            Полный путь к файлу комментариев
        """
        return cls.COMMENTS_DIR / filename
    
    @classmethod
    def validate_paths(cls) -> bool:
        """
        Проверить существование всех необходимых файлов.
        
        Returns:
            True если все файлы существуют, False иначе
        """
        required_files = [
            cls.QUESTIONS_FILE,
            cls.INTRO_COMMENTS_FILE,
            cls.CORRECT_COMMENTS_FILE,
            cls.WRONG_COMMENTS_FILE,
        ]
        
        for file_path in required_files:
            if not file_path.exists():
                print(f"[WARNING] Файл не найден: {file_path}")
                return False
        
        return True
