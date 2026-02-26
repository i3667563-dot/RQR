"""
Модель игрока.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Player:
    """
    Класс игрока.
    
    Attributes:
        name: Имя игрока
        score: Текущий счёт
        correct_answers: Количество правильных ответов
        wrong_answers: Количество неправильных ответов
        current_streak: Текущая серия правильных ответов
        best_streak: Лучшая серия правильных ответов
        total_questions: Всего вопросов пройдено
    """
    
    name: str
    score: int = 0
    correct_answers: int = 0
    wrong_answers: int = 0
    current_streak: int = 0
    best_streak: int = 0
    total_questions: int = 0
    
    def add_correct_answer(self, points: int = 10, bonus: int = 0) -> None:
        """
        Добавить правильный ответ.
        
        Args:
            points: Базовое количество очков за ответ
            bonus: Бонусные очки (например, за серию)
        """
        self.score += points + bonus
        self.correct_answers += 1
        self.total_questions += 1
        self.current_streak += 1
        
        if self.current_streak > self.best_streak:
            self.best_streak = self.current_streak
    
    def add_wrong_answer(self) -> None:
        """
        Добавить неправильный ответ.
        """
        self.wrong_answers += 1
        self.total_questions += 1
        self.current_streak = 0
    
    def get_accuracy(self) -> float:
        """
        Получить процент правильных ответов.
        
        Returns:
            Процент от 0 до 100
        """
        if self.total_questions == 0:
            return 0.0
        return (self.correct_answers / self.total_questions) * 100
    
    def get_stats(self) -> dict:
        """
        Получить статистику игрока.
        
        Returns:
            Словарь со всей статистикой
        """
        return {
            "name": self.name,
            "score": self.score,
            "correct_answers": self.correct_answers,
            "wrong_answers": self.wrong_answers,
            "total_questions": self.total_questions,
            "accuracy": self.get_accuracy(),
            "current_streak": self.current_streak,
            "best_streak": self.best_streak,
        }
    
    def reset(self) -> None:
        """
        Сбросить всю статистику (кроме имени).
        """
        self.score = 0
        self.correct_answers = 0
        self.wrong_answers = 0
        self.current_streak = 0
        self.best_streak = 0
        self.total_questions = 0
    
    def __str__(self) -> str:
        """Строковое представление игрока."""
        return f"Player(name='{self.name}', score={self.score})"
    
    def __repr__(self) -> str:
        """Официальное строковое представление."""
        return self.__str__()
