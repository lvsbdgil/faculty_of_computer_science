# Подключаем библиотеку для цветного вывода в терминал
import colorama

# Подключаем библиотеку для генерации случайных значений
import random

# Инициализируем colorama, чтобы цвета работали даже в Windows
colorama.init(autoreset=True)

# Словарь: для каждой фигуры перечислены фигуры, которые она побеждает
winning_combinations = {}

# Правила игры: каждая фигура побеждает семь других
winning_combinations["sponge"] = ["paper", "air", "water", "dragon", "devil", "lightning", "gun"]
winning_combinations["paper"] = ["air", "water", "dragon", "devil", "lightning", "gun", "rock"]
winning_combinations["air"] = ["water", "dragon", "devil", "lightning", "gun", "rock", "fire"]
winning_combinations["water"] = ["dragon", "devil", "lightning", "gun", "rock", "fire", "scissors"]
winning_combinations["dragon"] = ["devil", "lightning", "gun", "rock", "fire", "scissors", "snake"]
winning_combinations["devil"] = ["lightning", "gun", "rock", "fire", "scissors", "snake", "human"]
winning_combinations["lightning"] = ["gun", "rock", "fire", "scissors", "snake", "human", "tree"]
winning_combinations["gun"] = ["rock", "fire", "scissors", "snake", "human", "tree", "wolf"]
winning_combinations["rock"] = ["fire", "scissors", "snake", "human", "tree", "wolf", "sponge"]
winning_combinations["fire"] = ["scissors", "snake", "human", "tree", "wolf", "sponge", "paper"]
winning_combinations["scissors"] = ["snake", "human", "tree", "wolf", "sponge", "paper", "air"]
winning_combinations["snake"] = ["human", "tree", "wolf", "sponge", "paper", "air", "water"]
winning_combinations["human"] = ["tree", "wolf", "sponge", "paper", "air", "water", "dragon"]
winning_combinations["tree"] = ["wolf", "sponge", "paper", "air", "water", "dragon", "devil"]
winning_combinations["wolf"] = ["sponge", "paper", "air", "water", "dragon", "devil", "lightning"]

# Полный перечень всех допустимых фигур в игре
figures = [
    "sponge", "paper", "air", "water", "dragon", "devil",
    "lightning", "gun", "rock", "fire", "scissors", "snake",
    "human", "tree", "wolf"
]

# Список команд, которые может ввести пользователь
possible_commands = ["/start", "/finish", "/score"]

# Уровни сложности (типы поведения компьютера)
complexity = ["1", "2", "3", "4"]

# Сохраняем последовательность ходов игрока (для умного режима)
figure_history = []

# Словарь для подсчёта, сколько раз каждая фигура была выбрана игроком
figure_frequency = {}

# Счёт: очки игрока и компьютера
person_p = 0      # очки игрока
computer_p = 0    # очки компьютера

# Функция определяет результат одного раунда
def is_winning(person, computer, winning_combinations):
    # Если фигура компьютера в списке побед игрока — игрок выиграл
    if computer in winning_combinations[person]:
        return 1
    # Если фигура игрока в списке побед компьютера — игрок проиграл
    elif person in winning_combinations[computer]:
        return -1
    # В остальных случаях — ничья
    else:
        return 0

# Приветственное сообщение
print(f"{colorama.Fore.CYAN}Игра Камень-ножницы-бумага и не только!{colorama.Style.RESET_ALL}")
print(f"{colorama.Fore.CYAN}Доступные команды: {', '.join(possible_commands)}{colorama.Style.RESET_ALL}")

# Ожидаем первую команду от пользователя
command = input().strip()

# Если команда неизвестна — просим ввести снова
if command not in possible_commands:
    while command not in possible_commands:
        print(f"{colorama.Fore.RED}Неверная команда. Попробуйте снова:{colorama.Style.RESET_ALL}")
        command = input().strip()

# Обработка команды завершения до начала игры
if command == "/finish":
    print(f"{colorama.Fore.YELLOW}Жаль, что не получилось поиграть!{colorama.Style.RESET_ALL}")
    exit(0)

# Обработка запроса счёта до игры
elif command == "/score":
    print(f"{colorama.Fore.LIGHTBLACK_EX}Счёт появится после начала игры.{colorama.Style.RESET_ALL}")

# Запрос типа игры
print(f"{colorama.Fore.CYAN}Выберите тип игры:{colorama.Style.RESET_ALL}")
print(f"{colorama.Fore.LIGHTGREEN_EX}1{colorama.Fore.CYAN} — компьютер выбирает случайно")
print(f"{colorama.Fore.LIGHTGREEN_EX}2{colorama.Fore.CYAN} — компьютер всегда выбирает одну и ту же фигуру")
print(f"{colorama.Fore.LIGHTGREEN_EX}3{colorama.Fore.CYAN} — компьютер всегда побеждает")
print(f"{colorama.Fore.LIGHTGREEN_EX}4{colorama.Fore.CYAN} — умный режим (анализ предыдущих ходов){colorama.Style.RESET_ALL}")

# Получаем выбор сложности
game_type = input().strip()

# Проверка корректности выбора
while game_type not in complexity:
    print(f"{colorama.Fore.RED}Неверный тип игры. Введите 1, 2, 3 или 4:{colorama.Style.RESET_ALL}")
    game_type = input().strip()

# Информация перед началом игры
print(f"{colorama.Fore.CYAN}Начинаем игру! Введите одну из фигур или команду (/finish, /score).{colorama.Style.RESET_ALL}")
print(f"{colorama.Fore.LIGHTBLACK_EX}Доступные фигуры: {', '.join(figures)}{colorama.Style.RESET_ALL}")

# Первый ход игрока
user_input = input().strip()

# Для режима 2: запоминаем одну случайную фигуру, которую компьютер будет использовать всегда
random_figure = random.choice(figures)

# Основной игровой цикл — работает, пока игрок не введёт /finish
while user_input != "/finish":

    # Если игрок запросил счёт — показываем его и продолжаем игру
    if user_input == "/score":
        print(f"{colorama.Fore.LIGHTBLACK_EX}Текущий счёт: Ты — {person_p}, Компьютер — {computer_p}{colorama.Style.RESET_ALL}")
        print(f"{colorama.Fore.CYAN}Сделайте ход или введите команду:{colorama.Style.RESET_ALL}")
        user_input = input().strip()
        continue

    # Если введена несуществующая фигура — напоминаем допустимые варианты
    if user_input not in figures:
        print(f"{colorama.Fore.RED}Неизвестная фигура. Доступные: {', '.join(figures)}{colorama.Style.RESET_ALL}")
        user_input = input().strip()
        continue

    # Определяем, что выберет компьютер, в зависимости от выбранного режима

    if game_type == "1":
        # Режим 1: полностью случайный выбор
        computer_choice = random.choice(figures)

    elif game_type == "2":
        # Режим 2: компьютер всегда выбирает одну и ту же фигуру
        computer_choice = random_figure

    elif game_type == "3":
        # Режим 3: компьютер выбирает фигуру, которая гарантированно побеждает текущий ход игрока
        computer_choice = None
        for figure in figures:
            if user_input in winning_combinations[figure]:
                computer_choice = figure
                break
        # На случай, если правила изменились или возникла ошибка — резервный случайный выбор
        if computer_choice is None:
            computer_choice = random.choice(figures)

    elif game_type == "4":
        # Режим 4: умный выбор на основе статистики ходов игрока
        if len(figure_history) < 2:
            # Если слишком мало данных — играем случайно
            computer_choice = random.choice(figures)
        else:
            # Находим фигуру, которую игрок использует чаще всего
            most_common = max(figure_frequency, key=figure_frequency.get)
            computer_choice = None
            # Подбираем фигуру, которая побеждает эту самую частую
            for figure in figures:
                if most_common in winning_combinations[figure]:
                    computer_choice = figure
                    break
            # Если по какой-то причине не нашли — выбираем случайно
            if computer_choice is None:
                computer_choice = random.choice(figures)

    # Добавляем текущий ход игрока в историю
    figure_history.append(user_input)

    # Увеличиваем счётчик использования этой фигуры
    # Метод .get() возвращает 0, если фигуры ещё не было в словаре
    figure_frequency[user_input] = figure_frequency.get(user_input, 0) + 1

    # Определяем исход раунда
    result = is_winning(user_input, computer_choice, winning_combinations)

    # Выводим результат 
    if result == 1:
        person_p += 1
        print(f"{colorama.Fore.GREEN}Ты победил!{colorama.Style.RESET_ALL} Компьютер выбрал {computer_choice}.")
    elif result == -1:
        computer_p += 1
        print(f"{colorama.Fore.RED}Ты проиграл.{colorama.Style.RESET_ALL} Компьютер выбрал {computer_choice}.")
    else:
        print(f"{colorama.Fore.YELLOW}Ничья.{colorama.Style.RESET_ALL} Оба выбрали {computer_choice}.")

    # Показываем текущий счёт
    print(f"{colorama.Fore.LIGHTBLACK_EX}Счёт: Ты — {person_p}, Компьютер — {computer_p}{colorama.Style.RESET_ALL}")
    print(f"{colorama.Fore.CYAN}Сделайте новый ход или введите команду (/finish, /score):{colorama.Style.RESET_ALL}")

    # Ожидаем следующий ввод
    user_input = input().strip()

# Игра завершена, выводим финальный счёт
print(f"{colorama.Fore.YELLOW}Спасибо за игру! Финальный счёт: Ты — {person_p}, Компьютер — {computer_p}{colorama.Style.RESET_ALL}")
