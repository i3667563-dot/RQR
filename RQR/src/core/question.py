"""
Модель вопроса викторины.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Question:
    """
    Класс вопроса викторины.
    
    Attributes:
        id: Уникальный идентификатор вопроса
        question: Текст вопроса
        options: Список вариантов ответов
        correct: Индекс правильного ответа (0-based)
        intro_comment: Вступительный комментарий перед вопросом
        correct_comment: Комментарий при правильном ответе (загружается отдельно)
        wrong_comment: Комментарий при неправильном ответе (загружается отдельно)
        emoji: Эмодзи для отображения с вопросом
        tags: Теги вопроса для категоризации
    """
    
    id: int
    question: str
    options: List[str]
    correct: int
    intro_comment: str = ""
    correct_comment: str = ""
    wrong_comment: str = ""
    emoji: str = ""
    tags: List[str] = field(default_factory=list)
    
    def get_options_numbered(self) -> List[str]:
        """
        Получить нумерованный список вариантов ответов.
        
        Returns:
            Список строк вида "1. Вариант ответа"
        """
        return [f"{i + 1}. {option}" for i, option in enumerate(self.options)]
    
    def is_correct_answer(self, answer_index: int) -> bool:
        """
        Проверить, является ли ответ правильным.
        
        Args:
            answer_index: Индекс выбранного ответа (0-based)
            
        Returns:
            True если ответ правильный, False иначе
        """
        return answer_index == self.correct
    
    def get_correct_answer_text(self) -> str:
        """
        Получить текст правильного ответа.
        
        Returns:
            Текст правильного ответа
        """
        return self.options[self.correct]
    
    @classmethod
    def from_dict(cls, data: dict) -> "Question":
        """
        Создать вопрос из словаря (загрузка из JSON).
        
        Args:
            data: Словарь с данными вопроса
            
        Returns:
            Объект Question
        """
        return cls(
            id=data.get("id", 0),
            question=data.get("question", ""),
            options=data.get("options", []),
            correct=data.get("correct", 0),
        )
    
    def to_dict(self) -> dict:
        """
        Преобразовать вопрос в словарь (для сохранения в JSON).
        
        Returns:
            Словарь с данными вопроса
        """
        return {
            "id": self.id,
            "question": self.question,
            "options": self.options,
            "correct": self.correct,
        }
    
    def __str__(self) -> str:
        """Строковое представление вопроса."""
        return f"Question(id={self.id}, text='{self.question[:50]}...')"
    
    def __repr__(self) -> str:
        """Официальное строковое представление."""
        return self.__str__()
