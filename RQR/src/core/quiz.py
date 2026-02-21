"""
Викторина: загрузка вопросов и управление ими.
"""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any

from .question import Question
from .config import Config


class Quiz:
    """
    Класс викторины.
    
    Управляет загрузкой, хранением и предоставлением вопросов.
    
    Attributes:
        questions: Список всех вопросов
        current_index: Индекс текущего вопроса
        total_questions: Общее количество вопросов
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Инициализировать викторину.
        
        Args:
            config: Конфигурация игры (по умолчанию используется Config())
        """
        self.config = config or Config()
        self.questions: List[Question] = []
        self.current_index: int = 0
        
        # Комментарии (загружаются отдельно)
        self.intro_comments: Dict[int, Dict[str, Any]] = {}
        self.correct_comments: Dict[int, str] = {}
        self.wrong_comments: Dict[int, str] = {}
        
        # Загрузка данных
        self._load_questions()
        self._load_intro_comments()
        self._load_correct_comments()
        self._load_wrong_comments()
        self._apply_comments()
    
    def _load_questions(self) -> None:
        """
        Загрузить вопросы из JSON файла.
        
        Raises:
            FileNotFoundError: Если файл с вопросами не найден
            json.JSONDecodeError: Если файл содержит некорректный JSON
        """
        with open(self.config.QUESTIONS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.questions = [
            Question.from_dict(q_data) 
            for q_data in data.get("questions", [])
        ]
    
    def _load_intro_comments(self) -> None:
        """
        Загрузить вступительные комментарии из JSON файла.
        
        Комментарии хранятся в словаре с ключами-номерами вопросов.
        """
        if not self.config.INTRO_COMMENTS_FILE.exists():
            return
        
        with open(self.config.INTRO_COMMENTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        comments_data = data.get("comments", {})
        
        for key, comment_data in comments_data.items():
            question_id = int(key)
            self.intro_comments[question_id] = comment_data
    
    def _load_correct_comments(self) -> None:
        """
        Загрузить комментарии для правильных ответов из JSON файла.
        """
        if not self.config.CORRECT_COMMENTS_FILE.exists():
            return
        
        with open(self.config.CORRECT_COMMENTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        comments_data = data.get("comments", {})
        
        for key, comment_data in comments_data.items():
            question_id = int(key)
            self.correct_comments[question_id] = comment_data.get("text", "")
    
    def _load_wrong_comments(self) -> None:
        """
        Загрузить комментарии для неправильных ответов из JSON файла.
        """
        if not self.config.WRONG_COMMENTS_FILE.exists():
            return
        
        with open(self.config.WRONG_COMMENTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        comments_data = data.get("comments", {})
        
        for key, comment_data in comments_data.items():
            question_id = int(key)
            self.wrong_comments[question_id] = comment_data.get("text", "")
    
    def _apply_comments(self) -> None:
        """
        Применить все комментарии к вопросам.
        
        Добавляет emoji, intro_comment, correct_comment, wrong_comment к каждому вопросу.
        """
        for question in self.questions:
            # Вступительный комментарий
            intro_data = self.intro_comments.get(question.id, {})
            if intro_data:
                question.emoji = intro_data.get("emoji", "")
                question.intro_comment = intro_data.get("text", "")
                question.tags = intro_data.get("tags", [])
            
            # Комментарии к ответам
            question.correct_comment = self.correct_comments.get(question.id, "")
            question.wrong_comment = self.wrong_comments.get(question.id, "")
    
    def get_question(self, index: Optional[int] = None) -> Optional[Question]:
        """
        Получить вопрос по индексу.
        
        Args:
            index: Индекс вопроса (0-based). Если None, используется current_index.
            
        Returns:
            Объект Question или None, если индекс вне диапазона
        """
        if index is None:
            index = self.current_index
        
        if 0 <= index < len(self.questions):
            return self.questions[index]
        return None
    
    def get_next_question(self) -> Optional[Question]:
        """
        Перейти к следующему вопросу и вернуть его.
        
        Returns:
            Следующий вопрос или None, если вопросы закончились
        """
        if self.current_index < len(self.questions) - 1:
            self.current_index += 1
            return self.questions[self.current_index]
        return None
    
    def has_next(self) -> bool:
        """
        Проверить, есть ли следующий вопрос.
        
        Returns:
            True если есть следующий вопрос
        """
        return self.current_index < len(self.questions) - 1
    
    def has_previous(self) -> bool:
        """
        Проверить, есть ли предыдущий вопрос.
        
        Returns:
            True если есть предыдущий вопрос
        """
        return self.current_index > 0
    
    def go_to_question(self, index: int) -> bool:
        """
        Перейти к конкретному вопросу.
        
        Args:
            index: Индекс вопроса (0-based)
            
        Returns:
            True если переход успешен, False если индекс вне диапазона
        """
        if 0 <= index < len(self.questions):
            self.current_index = index
            return True
        return False
    
    def go_to_first(self) -> None:
        """Перейти к первому вопросу."""
        self.current_index = 0
    
    def go_to_last(self) -> None:
        """Перейти к последнему вопросу."""
        self.current_index = len(self.questions) - 1
    
    def shuffle(self) -> None:
        """Перемешать вопросы (для модов и кастомных режимов)."""
        import random
        random.shuffle(self.questions)
        self.current_index = 0
    
    def get_progress(self) -> tuple:
        """
        Получить текущий прогресс.
        
        Returns:
            Кортеж (текущий_номер, всего_вопросов)
        """
        return (self.current_index + 1, len(self.questions))
    
    def get_progress_percent(self) -> float:
        """
        Получить процент прогресса.
        
        Returns:
            Процент от 0 до 100
        """
        if not self.questions:
            return 0.0
        return ((self.current_index + 1) / len(self.questions)) * 100
    
    def __len__(self) -> int:
        """Количество вопросов."""
        return len(self.questions)
    
    def __iter__(self):
        """Итератор по вопросам."""
        return iter(self.questions)
    
    def __str__(self) -> str:
        """Строковое представление."""
        return f"Quiz(questions={len(self.questions)}, current={self.current_index + 1})"
