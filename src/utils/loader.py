"""
Загрузчик данных.
Утилиты для работы с JSON файлами.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class DataLoader:
    """
    Класс для загрузки данных из JSON файлов.
    
    Предоставляет удобный интерфейс для чтения и записи JSON.
    
    Example:
        loader = DataLoader()
        data = loader.load_json("data/questions.json")
        comments = loader.load_comments("data/comments/intro_comments.json")
    """
    
    @staticmethod
    def load_json(file_path: Path | str, encoding: str = "utf-8") -> Optional[Dict[str, Any]]:
        """
        Загрузить JSON файл.
        
        Args:
            file_path: Путь к файлу
            encoding: Кодировка файла
            
        Returns:
            Словарь с данными или None если файл не найден
            
        Raises:
            json.JSONDecodeError: Если файл содержит некорректный JSON
        """
        path = Path(file_path)
        
        if not path.exists():
            print(f"[WARNING] Файл не найден: {path}")
            return None
        
        with open(path, 'r', encoding=encoding) as f:
            return json.load(f)
    
    @staticmethod
    def save_json(data: Dict[str, Any], file_path: Path | str, 
                  encoding: str = "utf-8", indent: int = 2) -> bool:
        """
        Сохранить данные в JSON файл.
        
        Args:
            data: Данные для сохранения
            file_path: Путь к файлу
            encoding: Кодировка файла
            indent: Отступ для форматирования
            
        Returns:
            True если сохранение успешно
        """
        path = Path(file_path)
        
        # Создаём директорию если не существует
        path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(path, 'w', encoding=encoding) as f:
                json.dump(data, f, ensure_ascii=False, indent=indent)
            return True
        except Exception as e:
            print(f"[ERROR] Ошибка сохранения: {e}")
            return False
    
    @staticmethod
    def load_questions(file_path: Path | str) -> List[Dict[str, Any]]:
        """
        Загрузить список вопросов из JSON.
        
        Args:
            file_path: Путь к файлу с вопросами
            
        Returns:
            Список словарей с вопросами
        """
        data = DataLoader.load_json(file_path)
        if data is None:
            return []
        return data.get("questions", [])
    
    @staticmethod
    def load_comments(file_path: Path | str) -> Dict[int, Dict[str, Any]]:
        """
        Загрузить комментарии из JSON.
        
        Args:
            file_path: Путь к файлу с комментариями
            
        Returns:
            Словарь {id_вопроса: комментарий}
        """
        data = DataLoader.load_json(file_path)
        if data is None:
            return {}
        
        comments_data = data.get("comments", {})
        
        # Конвертируем строковые ключи в int
        return {int(k): v for k, v in comments_data.items()}
    
    @staticmethod
    def validate_question(question: Dict[str, Any]) -> bool:
        """
        Проверить корректность структуры вопроса.
        
        Args:
            question: Словарь с данными вопроса
            
        Returns:
            True если структура корректна
        """
        required_fields = ["id", "question", "options", "correct"]
        
        for field in required_fields:
            if field not in question:
                print(f"[WARNING] Вопрос не имеет поля '{field}'")
                return False
        
        # Проверка типов
        if not isinstance(question["id"], int):
            print(f"[WARNING] 'id' должен быть int")
            return False
        
        if not isinstance(question["question"], str):
            print(f"[WARNING] 'question' должен быть str")
            return False
        
        if not isinstance(question["options"], list):
            print(f"[WARNING] 'options' должен быть list")
            return False
        
        if not isinstance(question["correct"], int):
            print(f"[WARNING] 'correct' должен быть int")
            return False
        
        # Проверка диапазона correct
        if not 0 <= question["correct"] < len(question["options"]):
            print(f"[WARNING] 'correct' вне диапазона options")
            return False
        
        return True
    
    @staticmethod
    def validate_questions_file(file_path: Path | str) -> bool:
        """
        Проверить файл с вопросами на корректность.
        
        Args:
            file_path: Путь к файлу
            
        Returns:
            True если все вопросы корректны
        """
        questions = DataLoader.load_questions(file_path)
        
        if not questions:
            print(f"[ERROR] Файл пуст или не найден: {file_path}")
            return False
        
        valid_count = 0
        for q in questions:
            if DataLoader.validate_question(q):
                valid_count += 1
        
        print(f"[INFO] Проверено вопросов: {len(questions)}, валидных: {valid_count}")
        return valid_count == len(questions)
