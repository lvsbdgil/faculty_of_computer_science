
print("Пожалуйста введите поле в формате: \nX-X\n0-0\n---\nВаш ввод:") # Вывод инструкции ввода для пользователя

combination = [] # Массив в котором будет храниться поле

correct_values = ["X", "0", "-"] # Возможные символы, которые могут встречаться в вводе

# получаем от пользователя три строки ввода с помощью цикла
for i in range (0, 3):
    inp = list(input()) 
    if ((inp[0] not in correct_values) or (inp[1] not in correct_values) or (inp[2] not in correct_values)): # проверяем ввод на валидность
        print("Incorrect input \nTry again")
        exit(1)
    # Если ввод валидный, то добавляем елементы в массив
    combination.append(inp[0]) 
    combination.append(inp[1])
    combination.append(inp[2])
# далее создаем массив с индексами ячеек для победных комбинаций 
win_combinations = [
    # Победные ячейки по вертикали
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    # Победные ячейки по диагонали
    [0, 4, 8],
    [2, 4, 6],
    # Победные ячейки по горизонтали
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
]

# Создадим функцию, которая будет проверять текущее поле на наличие победной комбинации крестиков или ноликов
def win():
    for line in win_combinations: 
        if (combination[line [0]] == combination[line [1]] == combination[line [2]]): # Проверяем все возможные победные комбинации
            if (combination[line [0]] == "X"):
                return 1
            if (combination[line [0]] == "0"):
                return -1
    if ("-" not in combination): # Если поле полностью заполнено и нету победной комбинации то вывозвращаем флаг о ничьей
        return 0
    
    return False


# Далее создадим функцию minimax которая будет принимать на вход два аргумента, depth - глубина (колено) древа возможных вариантов и solution - какой ход нам нужен на выходе: наилучший или наихудший
# Это потреуется для оценки последующих возможных ходов противника (то есть человека)
def minimax(depth, solution):
    res = win() # Вызываем функцию win для оценки текущего поля на победу
    if res == 1:
        return 1
    elif res == -1:
        return -1 
    elif res == 0:
        return 0
    
    if (solution == "best"): # Если нам требуется наилучший случай 
        max_p = float("-inf")
        for i in range (9):
            if (combination[i] == "-"):
                combination[i] = "X" # Делаем ход за "X"
                p = minimax(depth + 1, "worst") # Оцениваем ход с точки зрения противника 
                combination[i] = "-" # Отменяем ход
                max_p = max(p, max_p) # Обновлем максимальную оценку
        return max_p # Возвращаем лучшую оценку для X



    else: # Если нам тербуется наихудший случай (ход противника)
        min_p = float("inf")
        for i in range (9):
            if (combination[i] == "-"):
                combination[i] = "0" # Делаем ход за 0
                p = minimax(depth + 1, "best") # Оцениваем ход с точки зрения X
                combination[i] = "-" # Отменям ход
                max_p = min(p, min_p) # Обноаляем минималную оценку
        return min_p # Возвращаем наихудшую оценку для X 


max_p = float("-inf") # Создаем переменную для подсчета максимального количества очков
best_m = -1 # Создаем переменную для сохранения индекса лучшего хода
for i in range(9):
    if combination[i] == "-": # Проходимся по всем незанятым ячейкам поля 
        combination[i] = "X" # Делаем предпологаемый ход
        p = minimax(0, "best") # Оцениваем ход с помощью minimax
        combination[i] = "-" # Отменяем ход
        if p > max_p: # Если оценка лучше текущей то запоминаем 
            max_p = p # Обновляем максимальную оценку
            best_m = i # Запоминаем индекс

if best_m != -1:
    combination[best_m] = "X" # Делаем оптимальный ход

# Выводим получившееся поле
print("Наилучший ход:")
print(f"{combination[0]} {combination[1]} {combination[2]}")
print(f"{combination[3]} {combination[4]} {combination[5]}")
print(f"{combination[6]} {combination[7]} {combination[8]}")