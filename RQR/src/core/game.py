"""
Основной класс игры.
Управляет игровым процессом и сюжетом.
"""

from typing import Optional

from .config import Config
from .quiz import Quiz
from .player import Player
from .question import Question
from .story import Story, StoryBeat


class Game:
    """
    Класс игры.
    
    Управляет основным игровым циклом, взаимодействием с игроком,
    подсчётом результатов и повествованием истории.
    
    Attributes:
        config: Конфигурация игры
        quiz: Объект викторины
        player: Объект игрока
        story: Объект истории
        is_running: Флаг активного игрового процесса
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Инициализировать игру.
        
        Args:
            config: Конфигурация игры (по умолчанию Config())
        """
        self.config = config or Config()
        self.quiz = Quiz(self.config)
        self.player = Player(name="Алексей")  # Имя игрока по умолчанию
        self.story = Story()
        self.is_running = False
    
    def set_player_name(self, name: str) -> None:
        """
        Установить имя игрока.
        
        Args:
            name: Имя игрока
        """
        self.player.name = name
        # Обновляем имя в истории (если нужно)
        self.story.player.name = name
    
    def start(self) -> None:
        """Начать игру."""
        self.is_running = True
        self.quiz.go_to_first()
        self.story.reset()
    
    def stop(self) -> None:
        """Закончить игру."""
        self.is_running = False
    
    def get_current_question(self) -> Optional[Question]:
        """
        Получить текущий вопрос.
        
        Returns:
            Текущий вопрос или None
        """
        return self.quiz.get_question()
    
    def answer(self, answer_index: int) -> bool:
        """
        Дать ответ на текущий вопрос.
        
        Args:
            answer_index: Индекс ответа (0-based)
            
        Returns:
            True если ответ правильный, False иначе
        """
        question = self.get_current_question()
        
        if question is None:
            return False
        
        is_correct = question.is_correct_answer(answer_index)
        
        if is_correct:
            # Подсчёт очков
            points = self.config.POINTS_PER_CORRECT
            
            # Бонус за серию
            bonus = 0
            if self.player.current_streak >= 3:
                bonus = self.config.BONUS_POINTS_STREAK
            
            self.player.add_correct_answer(points, bonus)
        else:
            self.player.add_wrong_answer()
        
        return is_correct
    
    def next_question(self) -> bool:
        """
        Перейти к следующему вопросу.
        
        Returns:
            True если переход успешен, False если это последний вопрос
        """
        next_q = self.quiz.get_next_question()
        if next_q is not None:
            self.story.current_question += 1
        return next_q is not None
    
    def check_story_beat(self) -> Optional[StoryBeat]:
        """
        Проверить, есть ли сюжетный момент для текущего вопроса.
        
        Returns:
            StoryBeat или None
        """
        current, _ = self.quiz.get_progress()
        return self.story.get_story_beat(current)
    
    def is_finished(self) -> bool:
        """
        Проверить, закончена ли игра.
        
        Returns:
            True если все вопросы пройдены
        """
        return not self.quiz.has_next()
    
    def get_results(self) -> dict:
        """
        Получить результаты игры.
        
        Returns:
            Словарь с результатами
        """
        stats = self.player.get_stats()
        stats["total_questions"] = len(self.quiz)
        stats["is_finished"] = self.is_finished()
        stats["story_completed"] = len(self.story.shown_beats) == len(self.story)
        return stats
    
    def reset(self) -> None:
        """
        Сбросить игру к начальному состоянию.
        """
        self.quiz.go_to_first()
        self.player.reset()
        self.story.reset()
        self.is_running = False
    
    def __str__(self) -> str:
        """Строковое представление игры."""
        return f"Game(player={self.player.name}, progress={self.quiz.get_progress()})"
