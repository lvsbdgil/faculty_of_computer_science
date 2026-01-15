# Импортируем необходимые модули:

import tkinter as tk
import random


class GameOfLife:
    """
    Класс, описывающий логику и интерфейс игры Жизнь.
    """

    def __init__(self, root):
        """
        Конструктор класса: вызывается один раз при создании объекта.
        Размеры, элементы управления, начальное поле.
        """
        self.root = root  # Сохраняем ссылку на главное окно Tkinter
        self.root.title("Игра Жизнь")  # Заголовок окна

        # === ПАРАМЕТРЫ ПОЛЯ ===
        # Сколько строк и столбцов будет на нашем игровом поле.
        # Можно изменить эти числа, чтобы сделать поле больше или меньше !.
        self.rows = 30   # количество строк (по вертикали)
        self.cols = 50   # количество столбцов (по горизонтали)
        self.cell_size = 15  # Размер одной клетки в пикселях (ширина и высота)

        # === СОСТОЯНИЕ ИГРОВОГО ПОЛЯ ===
        # Создаём двумерный список (матрицу), где каждая ячейка — это True (живая) или False (мёртвая).
        # Изначально всё поле мёртвое.
        self.grid = [[False for _ in range(self.cols)] for _ in range(self.rows)]

        # Флаг, показывающий, запущена ли симуляция.
        self.running = False

        # Скорость обновления (в миллисекундах между поколениями).
        # Чем меньше число — тем быстрее идёт игра.
        self.speed = 200  # по умолчанию — 200 мс

        # === ОСНОВНОЕ ИГРОВОЕ ПОЛЕ ===
        # Вычисляем общую ширину и высоту холста, чтобы он вмещал все клетки.
        self.canvas_width = self.cols * self.cell_size
        self.canvas_height = self.rows * self.cell_size

        # Создаём холст — область, на которой будем рисовать клетки.
        self.canvas = tk.Canvas(
            root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg='white'  # фон белый, чтобы мёртвые клетки были незаметны
        )
        self.canvas.pack()  # Размещаем холст в окне

        # === ОБРАБОТКА КЛИКОВ МЫШЬЮ ===
        # Когда пользователь кликает левой кнопкой мыши по холсту,
        # вызывается метод on_click.
        self.canvas.bind("<Button-1>", self.on_click)

        # === ПАНЕЛЬ УПРАВЛЕНИЯ ===
        # Создаём отдельный фрейм (контейнер) под кнопки, чтобы они не мешали полю.
        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)  # Отступ сверху/снизу — 10 пикселей

        # --- Кнопка "Запустить" ---
        self.start_button = tk.Button(
            control_frame,
            text="▶ Запустить",
            command=self.start  # При нажатии вызовется метод start()
        )
        self.start_button.pack(side=tk.LEFT, padx=5)  # Располагаем слева, с отступом

        # --- Кнопка "Остановить" ---
        self.stop_button = tk.Button(
            control_frame,
            text="⏹ Остановить",
            command=self.stop
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # --- Кнопка "Очистить" (обнулить всё поле) ---
        self.clear_button = tk.Button(
            control_frame,
            text="Очистить",
            command=self.clear
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # --- Поле для ввода количества случайных клеток ---
        tk.Label(control_frame, text="Случайные клетки:").pack(side=tk.LEFT, padx=(20, 5))
        # Переменная для хранения значения из спинбокса (числового поля)
        self.random_count = tk.IntVar(value=100)  # по умолчанию — 100 клеток
        self.random_spinbox = tk.Spinbox(
            control_frame,
            from_=1,  # минимум 1 клетка
            to=self.rows * self.cols,  # максимум — всё поле
            width=5,
            textvariable=self.random_count
        )
        self.random_spinbox.pack(side=tk.LEFT, padx=5)

        # --- Кнопка Случайно — заполняет поле случайными живыми клетками ---
        self.random_button = tk.Button(
            control_frame,
            text="Случайно",
            command=self.randomize
        )
        self.random_button.pack(side=tk.LEFT, padx=5)

        # --- Ползунок скорости ---
        tk.Label(control_frame, text="Скорость (мс):").pack(side=tk.LEFT, padx=(20, 5))
        self.speed_slider = tk.Scale(
            control_frame,
            from_=50,     # самая высокая скорость — 50 мс
            to=1000,      # самая низкая — 1000 мс
            orient=tk.HORIZONTAL,  # горизонтальный ползунок
            length=200,   # длина в пикселях
            command=self.update_speed,  # вызывается при любом движении ползунка
            resolution=10  # шаг изменения — 10 мс
        )
        self.speed_slider.set(self.speed)  # устанавливаем начальное значение
        self.speed_slider.pack(side=tk.LEFT, padx=5)

        # === ПЕРВОНАЧАЛЬНАЯ ОТРИСОВКА ПОЛЯ ===
        # Рисуем пустое поле (все клетки мёртвые)
        self.draw_grid()

    def on_click(self, event):
        """
        Обрабатывает клик мышью по холсту.
        Если симуляция НЕ запущена — переключает состояние клетки под курсором.
        """
        if self.running:
            return  # нельзя редактировать поле во время игры

        # Определяем, в какую клетку попал клик:
        # делим координаты клика на размер клетки - получаем номер строки и столбца
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        # Проверяем, что клик был внутри поля (а не за его пределами)
        if 0 <= row < self.rows and 0 <= col < self.cols:
            # Меняем состояние клетки: если была жива — умирает, и наоборот
            self.grid[row][col] = not self.grid[row][col]
            # Перерисовываем только эту одну клетку (эффективнее, чем всё поле)
            self.draw_cell(row, col)

    def draw_cell(self, row, col):
        """
        Рисует одну клетку на холсте по заданным координатам (row, col).
        """
        # Вычисляем координаты прямоугольника в пикселях
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        # Выбираем цвет: чёрный, если клетка жива; белый — если мертва
        color = 'black' if self.grid[row][col] else 'white'

        # Рисуем прямоугольник (клетку) на холсте
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='lightgray')

    def draw_grid(self):
        """
        Перерисовывает все поле целиком.
        """
        self.canvas.delete("all")  # Сначала удаляем всё, что было на холсте
        # Проходим по каждой клетке и рисуем её
        for row in range(self.rows):
            for col in range(self.cols):
                self.draw_cell(row, col)



    def count_neighbors(self, row, col):
        """
        Считает, сколько живых соседей у клетки с координатами (row, col).
        """
        count = 0
        # Проверяем все 8 соседних позиций: смещения -1, 0, +1 по строкам и столбцам
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # пропускаем саму клетку (центр)
                # Вычисляем координаты соседа
                r, c = row + dr, col + dc
                # Проверяем, что сосед находится внутри поля
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    if self.grid[r][c]:  # если сосед жив — увеличиваем счётчик
                        count += 1
        return count

    def next_generation(self):
        """
        Создаёт новое поле, применяет правила ко всем клеткам,
        затем заменяет старое поле на новое и перерисовывает.
        """
        # Создаём новое пустое поле (все клетки мёртвые)
        new_grid = [[False for _ in range(self.cols)] for _ in range(self.rows)]

        # Проходим по каждой клетке
        for row in range(self.rows):
            for col in range(self.cols):
                neighbors = self.count_neighbors(row, col)
                is_alive = self.grid[row][col]

                if is_alive:
                    # Живая клетка выживает, только если у неё 2 или 3 соседа
                    if neighbors == 2 or neighbors == 3:
                        new_grid[row][col] = True
                    # Иначе — умирает (остаётся False)
                else:
                    # Мёртвая клетка оживает, только если ровно 3 живых соседа
                    if neighbors == 3:
                        new_grid[row][col] = True

        # Заменяем старое поле на новое
        self.grid = new_grid
        # Обновляем изображение на экране
        self.draw_grid()

    def run_simulation(self):
        """
        Главный цикл симуляции.
        Если симуляция запущена — вычисляет следующее поколение,
        затем планирует вызов самого себя через self.speed миллисекунд.
        """
        if self.running:
            self.next_generation()
            # Через self.speed миллисекунд снова вызвать этот же метод
            self.root.after(self.speed, self.run_simulation)


    def start(self):
        """Запускает симуляцию, если она ещё не запущена."""
        if not self.running:
            self.running = True
            self.run_simulation()  # запускаем цикл

    def stop(self):
        """Останавливает симуляцию."""
        self.running = False

    def clear(self):
        """Очищает всё поле: все клетки становятся мёртвыми."""
        self.stop()  # на всякий случай останавливаем симуляцию
        # Создаём новое пустое поле
        self.grid = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.draw_grid()  # перерисовываем

    def randomize(self):
        """
        Заполняет поле случайным количеством живых клеток.
        Количество берётся из спинбокса (random_count).
        """
        self.stop()  # сначала останавливаем симуляцию

        count = self.random_count.get()  # сколько клеток оживить?
        total = self.rows * self.cols

        # Защита от глупостей: нельзя выбрать больше клеток, чем есть на поле
        if count > total:
            count = total

        # Генерируем список всех возможных координат (row, col)
        all_positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        # Случайно выбираем `count` уникальных позиций без повторений
        positions = random.sample(all_positions, count)

        # Обнуляем всё поле
        self.grid = [[False for _ in range(self.cols)] for _ in range(self.rows)]

        # Оживляем выбранные клетки
        for r, c in positions:
            self.grid[r][c] = True

        # Перерисовываем всё поле
        self.draw_grid()

    def update_speed(self, value):
        """
        Вызывается при движении ползунка скорости.
        Обновляет внутреннюю переменную self.speed.
        Значение приходит как строка, поэтому преобразуем в int.
        """
        self.speed = int(value)


if __name__ == "__main__":
    root = tk.Tk()  # создаём главное окно
    app = GameOfLife(root)  # создаём объект игры, передавая ему окно
    root.mainloop()  # запускаем цикл обработки событий (ожидание кликов, нажатий и т.д.)
