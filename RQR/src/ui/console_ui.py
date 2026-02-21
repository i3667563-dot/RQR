"""
Консольный интерфейс для Russian Quiz Remake с полноценным сюжетом.
"""

from typing import Optional

from ..core.game import Game
from ..core.question import Question
from ..core.story import StoryBeat


class ConsoleUI:
    """
    Консольный интерфейс игры с сюжетом.
    
    Отвечает за отображение информации, диалогов и получение ввода от игрока.
    """
    
    # ASCII логотип игры
    LOGO = """
╔════════════════════════════════════╗
║         RQR                        ║
║    Russian Quiz Remake             ║
║         ~~~                        ║
║    ШОУ ПАМЯТИ                      ║
╚════════════════════════════════════╝
"""
    
    # Цвета для настроения (ANSI коды)
    MOOD_COLORS = {
        "normal": "",
        "dramatic": "\033[91m",      # Красный
        "calm": "\033[94m",          # Синий
        "mysterious": "\033[95m",    # Фиолетовый
        "emotional": "\033[93m",     # Жёлтый
    }
    RESET = "\033[0m"
    
    def __init__(self, game: Game):
        """
        Инициализировать консольный интерфейс.
        
        Args:
            game: Объект игры
        """
        self.game = game
        self.show_emoji = True
        self.show_comments = True
        self.show_story = True
    
    def clear_screen(self) -> None:
        """Очистить экран консоли."""
        print("\n" * 2)
    
    def print_logo(self) -> None:
        """Вывести логотип игры."""
        print(self.LOGO)
    
    def print_separator(self, char: str = "─", length: int = 50) -> None:
        """Вывести разделительную линию."""
        print(char * length)
    
    def print_act_header(self, act_number: int) -> None:
        """
        Вывести заголовок акта.
        
        Args:
            act_number: Номер акта (1-4)
        """
        # Названия актов без спойлеров
        act_names = {
            1: "ЧАСТЬ I",
            2: "ЧАСТЬ II",
            3: "ЧАСТЬ III",
            4: "ЧАСТЬ IV",
        }
        
        self.clear_screen()
        self.print_separator("═")
        print(f"  {act_names.get(act_number, '')}")
        self.print_separator("═")
        print()
    
    def print_story_beat(self, beat: StoryBeat) -> None:
        """
        Вывести сюжетный момент.
        
        Args:
            beat: Объект сюжетного момента
        """
        if not self.show_story:
            return
        
        # Проверка на новый акт
        current_question, _ = self.game.quiz.get_progress()
        
        # Вывод заголовка акта если это первый момент акта
        if beat.trigger_question == 1:
            self.print_act_header(1)
        elif beat.trigger_question == 40:
            self.print_act_header(2)
        elif beat.trigger_question == 77:
            self.print_act_header(3)
        elif beat.trigger_question == 115:
            self.print_act_header(4)
        
        self.print_separator("═")
        
        # Заголовок момента
        mood_color = self.MOOD_COLORS.get(beat.mood, "")
        print(f"  {mood_color}📖 {beat.title}{self.RESET}")
        self.print_separator("═")
        
        # Кто говорит
        character = self.game.story.get_character_by_name(beat.speaker)
        emoji = character.emoji if character and self.show_emoji else ""
        
        print(f"\n  {emoji} {beat.speaker}:")
        print()
        
        # Текст диалога (с отступами)
        for line in beat.text.split('\n'):
            print(f"    {line}")
        
        print()
        self.print_separator("═")
    
    def print_question(self, question: Question, question_number: int, total: int) -> None:
        """Вывести вопрос на экран."""
        # Прогресс бар
        progress = f"Вопрос {question_number}/{total}"
        print(f"\n📍 {progress}")
        
        # Вступительный комментарий ведущего
        if self.show_comments and question.intro_comment:
            emoji = question.emoji + " " if self.show_emoji and question.emoji else ""
            print(f"\n🎤 Иван: {emoji}{question.intro_comment}")
        
        # Текст вопроса
        print(f"\n❓ {question.question}")
        
        # Варианты ответов
        print("\nВарианты ответов:")
        for i, option in enumerate(question.options, 1):
            print(f"  {i}. {option}")
    
    def print_result(self, is_correct: bool, question: Question) -> None:
        """Вывести результат ответа."""
        if is_correct:
            print(f"\n✅ Правильно!")
            if self.show_comments and question.correct_comment:
                print(f"💬 Иван: {question.correct_comment}")
        else:
            print(f"\n❌ Неправильно!")
            print(f"Правильный ответ: {question.get_correct_answer_text()}")
            if self.show_comments and question.wrong_comment:
                print(f"💬 Иван: {question.wrong_comment}")
    
    def print_stats(self) -> None:
        """Вывести статистику игрока."""
        stats = self.game.player.get_stats()
        
        print("\n📊 Статистика:")
        print(f"  Имя: {stats['name']}")
        print(f"  Счёт: {stats['score']}")
        print(f"  Правильно: {stats['correct_answers']}")
        print(f"  Неправильно: {stats['wrong_answers']}")
        print(f"  Точность: {stats['accuracy']:.1f}%")
        print(f"  Серия: {stats['current_streak']} (лучшая: {stats['best_streak']})")
    
    def print_results(self) -> None:
        """Вывести итоги игры с учётом сюжета."""
        results = self.game.get_results()
        
        self.print_header("🏆 ИТОГИ ИГРЫ 🏆")
        
        print(f"\n👤 Игрок: {results['name']}")
        print(f"📈 Счёт: {results['score']}")
        print(f"✅ Правильных ответов: {results['correct_answers']} из {results['total_questions']}")
        print(f"🎯 Точность: {results['accuracy']:.1f}%")
        print(f"🔥 Лучшая серия: {results['best_streak']}")
        print(f"📖 Сюжетных моментов: {len(self.game.story.shown_beats)} из {len(self.game.story)}")
        
        # Прогресс по актам
        act_progress = self.game.story.get_progress_by_act()
        print("\n📚 Прогресс по актам:")
        act_names = {1: "Пробуждение", 2: "Раскрытие", 3: "Истина", 4: "Решение"}
        for act, name in act_names.items():
            shown = act_progress.get(act, 0)
            total = len(self.game.story.get_beats_by_act(act))
            print(f"  Акт {act} ({name}): {shown}/{total}")
        
        # Оценка результата
        accuracy = results['accuracy']
        if accuracy >= 90:
            print("\n🏅 Легендарный результат!")
            print("   Иван был бы горд тобой...")
        elif accuracy >= 75:
            print("\n🥇 Отличный результат!")
            print("   Ты почти всё вспомнил!")
        elif accuracy >= 50:
            print("\n🥈 Хороший результат!")
            print("   Но есть куда расти...")
        else:
            print("\n🥉 Есть куда расти!")
            print("   Память ещё проснётся...")
    
    def print_header(self, text: str) -> None:
        """Вывести заголовок раздела."""
        self.print_separator()
        print(f"  {text}")
        self.print_separator()
    
    def get_input(self, prompt: str = "> ") -> str:
        """Получить ввод от пользователя."""
        try:
            return input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            return ""
    
    def get_answer(self, question: Question) -> Optional[int]:
        """Получить ответ от игрока."""
        while True:
            user_input = self.get_input(f"\nВаш ответ (1-{len(question.options)}) > ")
            
            if user_input.lower() in ("quit", "exit", "q"):
                return None
            
            try:
                answer = int(user_input)
                if 1 <= answer <= len(question.options):
                    return answer - 1
                else:
                    print(f"⚠️ Введите число от 1 до {len(question.options)}")
            except ValueError:
                print("⚠️ Введите корректное число")
    
    def ask_continue(self) -> bool:
        """Спросить, хочет ли игрок продолжить."""
        response = self.get_input("\nПродолжить? (Enter - да, n - нет) > ")
        return response.lower() not in ("n", "no", "н", "нет")
    
    def welcome(self) -> None:
        """Приветствовать игрока и начать историю."""
        self.clear_screen()
        self.print_logo()
        
        # Вступительный диалог
        self.print_separator("═")
        print("  📖 ПРОЛОГ: ПРИГЛАШЕНИЕ")
        self.print_separator("═")
        print()
        print("  🎤 Иван:")
        print()
        print("    А-а-а... очнулся.")
        print("    Добро пожаловать, Алексей.")
        print()
        print("    Я знаю, у тебя миллион вопросов.")
        print("    Где ты? Что это за место? Почему я знаю твоё имя?")
        print()
        print("    Сядь. Расслабься. Всё узнаешь в своё время.")
        print()
        print("    Меня зовут Иван. Я ведущий этого... шоу.")
        print("    А ты — следующий участник.")
        print()
        print("    152 вопроса. 152 шага к истине.")
        print("    Готов?")
        print()
        self.print_separator("═")
        
        input("\nНажмите Enter чтобы начать...")
    
    def game_loop(self) -> None:
        """Основной игровой цикл с сюжетом."""
        self.game.start()
        
        while self.game.is_running:
            question = self.game.get_current_question()
            
            if question is None:
                break
            
            current, total = self.game.quiz.get_progress()
            
            # Проверка сюжетного момента
            story_beat = self.game.check_story_beat()
            if story_beat:
                self.print_story_beat(story_beat)
                input("\nНажмите Enter чтобы продолжить...")
            
            # Отображение вопроса
            self.clear_screen()
            self.print_question(question, current, total)
            
            # Получение ответа
            answer = self.get_answer(question)
            
            if answer is None:
                break
            
            # Обработка ответа
            is_correct = self.game.answer(answer)
            self.print_result(is_correct, question)
            self.print_stats()
            
            # Проверка окончания игры
            if self.game.is_finished():
                self.print_results()
                
                # Финальный сюжетный момент
                final_beat = self.game.check_story_beat()
                if final_beat:
                    input("\nНажмите Enter для финала...")
                    self.print_story_beat(final_beat)
                
                break
            
            # Продолжение?
            if not self.ask_continue():
                self.print_results()
                break
            
            # Следующий вопрос
            self.game.next_question()
        
        self.game.stop()
