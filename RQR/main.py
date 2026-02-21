"""
Russian Quiz Remake (RQR)
Викторина с вопросами о России и сюжетной историей.

Запуск игры:
    python main.py
"""

import sys
from pathlib import Path

# Добавляем корень проекта в PATH для импортов
sys.path.insert(0, str(Path(__file__).parent))

from src.core import Game, Config
from src.ui import ConsoleUI


def main():
    """Точка входа в игру."""
    
    # Проверка конфигурации
    config = Config()
    if not config.validate_paths():
        print("[ERROR] Не все необходимые файлы найдены!")
        print("Проверьте наличие файлов в папке data/")
        return
    
    # Создание и настройка игры
    game = Game(config)
    
    # Ввод имени (опционально, по умолчанию "Алексей")
    print("╔════════════════════════════════════╗")
    print("║         RQR                        ║")
    print("║    Russian Quiz Remake             ║")
    print("║    ШОУ ПАМЯТИ                      ║")
    print("╚════════════════════════════════════╝")
    print()
    print("Введите своё имя (Enter - Алексей):")
    name = input("> ").strip()
    
    if name:
        game.set_player_name(name)
    
    # Запуск консольного интерфейса
    ui = ConsoleUI(game)
    ui.welcome()
    ui.game_loop()
    
    print("\nСпасибо за игру!")


if __name__ == "__main__":
    main()
