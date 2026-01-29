# Импортируем стандартную библиотеку tkinter для создания графического интерфейса
import tkinter as tk
# Импортируем модуль math для математических вычислений (синусы, косинусы, квадратные корни)
import math
# Импортируем декоратор dataclass для автоматического создания классов с данными
from dataclasses import dataclass
from typing import List, Optional


# Создаем класс Vector для удобной работы с векторами (направленными отрезками)
# Векторы нужны для представления скорости, ускорения и других физических величин с направлением
@dataclass
class Vector:
    """Вектор для работы с физическими величинами - имеет направление и длину (модуль)"""
    # Координата X вектора (горизонтальная составляющая)
    x: float = 0.0
    # Координата Y вектора (вертикальная составляющая)
    y: float = 0.0
    
    # Метод сложения двух векторов: результат - новый вектор с суммой координат
    # Например: (2, 3) + (1, 4) = (3, 7)
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    # Метод вычитания векторов: результат - вектор разности координат
    # Например: (5, 6) - (2, 1) = (3, 5)
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    # Метод умножения вектора на число (скаляр): масштабирует вектор
    # Например: (3, 4) * 2 = (6, 8) - вектор становится в 2 раза длиннее
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    # Метод вычисления длины (модуля) вектора по теореме Пифагора
    # Для вектора (3, 4) длина = sqrt(3² + 4²) = 5
    def magnitude(self):
        return math.hypot(self.x, self.y)
    
    # Метод нормализации вектора: превращает его в единичный вектор (длиной 1) 
    # с сохранением направления. Нужен для работы с направлениями без учета длины.
    def normalize(self):
        # Сначала вычисляем текущую длину вектора
        mag = self.magnitude()
        # Если длина равна нулю (вектор нулевой), возвращаем нулевой вектор
        if mag == 0:
            return Vector(0, 0)
        # Делим каждую координату на длину, получая вектор длиной 1
        return Vector(self.x / mag, self.y / mag)


# Базовый класс для всех фигур - содержит общую логику для кругов, квадратов и треугольников
class Shape:
    """Базовый класс для всех фигур - определяет общие свойства и поведение"""
    # Конструктор класса вызывается при создании любой фигуры
    def __init__(self, canvas, x, y, size, color, mass=1.0):
        # Ссылка на холст tkinter, на котором будет рисоваться фигура
        self.canvas = canvas
        # Горизонтальная координата центра фигуры (ось X)
        self.x = x
        # Вертикальная координата центра фигуры (ось Y)
        self.y = y
        # Характерный размер фигуры (диаметр для круга, сторона для квадрата)
        self.size = size
        # Цвет заливки фигуры в формате HEX (#RRGGBB)
        self.color = color
        # Масса фигуры для физических расчетов (в условных единицах)
        self.mass = mass
        # Вектор скорости фигуры - определяет направление и скорость движения
        self.velocity = Vector(0, 0)
        # Флаг: находится ли фигура сейчас в режиме перетаскивания мышью
        self.is_dragged = False
        # Идентификатор объекта на холсте tkinter (нужен для обновления позиции)
        self.shape_id = None
        # Вызываем метод создания визуального представления фигуры на холсте
        self.create_shape()
        
    # Абстрактный метод: создание фигуры на холсте (реализуется в подклассах)
    def create_shape(self):
        """Создать визуальное представление фигуры на холсте (реализуется в подклассах)"""
        pass
    
    # Абстрактный метод: обновление позиции фигуры на холсте после изменения координат
    def update_position(self):
        """Обновить позицию фигуры на холсте после изменения координат (реализуется в подклассах)"""
        pass
    
    # Метод перемещения фигуры на заданное расстояние по осям X и Y
    def move(self, dx, dy):
        """Переместить фигуру на расстояние dx по горизонтали и dy по вертикали"""
        # Увеличиваем текущую координату X на величину dx
        self.x += dx
        # Увеличиваем текущую координату Y на величину dy
        self.y += dy
        # Обновляем визуальное отображение фигуры на новой позиции
        self.update_position()
    
    # Метод применения силы гравитации к фигуре (ускорение вниз)
    def apply_gravity(self, gravity_strength):
        """Применить силу гравитации - увеличить вертикальную скорость вниз"""
        # Гравитация действует ТОЛЬКО если фигура не перетаскивается мышью
        if not self.is_dragged:
            # Увеличиваем вертикальную составляющую скорости (ось Y)
            # Чем больше gravity_strength, тем быстрее падает фигура
            self.velocity.y += gravity_strength
    
    # Метод применения трения для замедления горизонтального движения
    def apply_friction(self, friction=0.98):
        """Применить трение - постепенно замедлять горизонтальное движение"""
        # Трение действует ТОЛЬКО если фигура не перетаскивается мышью
        if not self.is_dragged:
            # Умножаем горизонтальную скорость на коэффициент < 1
            # Например: 0.98 означает потерю 2% скорости за каждый кадр
            self.velocity.x *= friction
    
    # Абстрактный метод: проверка, находится ли точка (px, py) внутри фигуры
    def contains_point(self, px, py):
        """Проверить, находится ли точка с координатами (px, py) внутри фигуры"""
        return False
    
    # Абстрактный метод: обработка столкновения с другой фигурой
    def on_collision(self, other):
        """Обработка столкновения с другой фигурой (логика зависит от типа фигур)"""
        pass
    
    # Метод обработки столкновения фигуры с границами холста (пол, стены, потолок)
    def resolve_boundary_collision(self, width, height, restitution=0.7):
        """Обработка столкновения с границами холста с учетом упругости"""
        # Проверяем столкновение с нижней границей (полом)
        if self.y + self.size/2 > height:
            # Корректируем позицию, чтобы фигура не проваливалась под пол
            self.y = height - self.size/2
            # Меняем направление вертикальной скорости (отскок вверх)
            # Умножаем на restitution (коэффициент упругости): 0.7 = 70% энергии сохраняется
            self.velocity.y = -self.velocity.y * restitution
            # Дополнительное трение при контакте с полом для замедления скольжения
            self.velocity.x *= 0.9
        
        # Проверяем столкновение с верхней границей (потолком)
        if self.y - self.size/2 < 0:
            # Корректируем позицию, чтобы фигура не вылетала за потолок
            self.y = self.size/2
            # Отскок вниз с потерей энергии
            self.velocity.y = -self.velocity.y * restitution
        
        # Проверяем столкновение с правой стеной
        if self.x + self.size/2 > width:
            # Корректируем позицию у правой стены
            self.x = width - self.size/2
            # Отскок влево с потерей энергии
            self.velocity.x = -self.velocity.x * restitution
        # Проверяем столкновение с левой стеной
        elif self.x - self.size/2 < 0:
            # Корректируем позицию у левой стены
            self.x = self.size/2
            # Отскок вправо с потерей энергии
            self.velocity.x = -self.velocity.x * restitution
        
        # Обновляем визуальное отображение фигуры на скорректированной позиции
        self.update_position()


# Класс круга - наследуется от базового класса Shape
class Circle(Shape):
    """Круг - отскакивает при падении благодаря высокому коэффициенту упругости"""
    # Переопределяем метод создания визуального представления для круга
    def create_shape(self):
        # Создаем овал на холсте с помощью метода create_oval
        # Координаты: левый верхний угол и правый нижний угол ограничивающего прямоугольника
        self.shape_id = self.canvas.create_oval(
            # Левая граница: центр минус половина размера
            self.x - self.size/2, 
            # Верхняя граница: центр минус половина размера
            self.y - self.size/2,
            # Правая граница: центр плюс половина размера
            self.x + self.size/2, 
            # Нижняя граница: центр плюс половина размера
            self.y + self.size/2,
            # Цвет заливки берется из параметра конструктора
            fill=self.color, 
            # Цвет и толщина контура
            outline="black", width=2
        )
    
    # Переопределяем метод обновления позиции для круга
    def update_position(self):
        # Обновляем координаты овала на холсте с новыми позициями центра
        self.canvas.coords(
            # Идентификатор объекта на холсте
            self.shape_id,
            # Новые координаты левого верхнего угла
            self.x - self.size/2, self.y - self.size/2,
            # Новые координаты правого нижнего угла
            self.x + self.size/2, self.y + self.size/2
        )
    
    # Переопределяем метод проверки попадания точки внутрь круга
    def contains_point(self, px, py):
        # Вычисляем разницу координат между точкой и центром круга
        dx = px - self.x
        dy = py - self.y
        # Точка внутри круга, если расстояние до центра меньше радиуса
        # Используем math.hypot для вычисления гипотенузы (расстояния)
        return math.hypot(dx, dy) <= self.size/2
    
    # Переопределяем метод обработки столкновения для круга (упругое столкновение)
    def on_collision(self, other):
        """Упругое столкновение с сохранением импульса и энергии"""
        # Вычисляем вектор между центрами двух кругов
        dx = self.x - other.x
        dy = self.y - other.y
        # Вычисляем расстояние между центрами по теореме Пифагора
        distance = math.hypot(dx, dy)
        
        # Проверяем, действительно ли произошло столкновение (дистанция меньше суммы радиусов)
        # и избегаем деления на ноль (distance > 0)
        if distance < (self.size/2 + other.size/2) and distance > 0:
            # Нормализуем вектор направления (делаем его длиной 1)
            nx = dx / distance
            ny = dy / distance
            
            # Вычисляем относительную скорость двух фигур
            dvx = self.velocity.x - other.velocity.x
            dvy = self.velocity.y - other.velocity.y
            
            # Вычисляем проекцию относительной скорости на линию столкновения
            # (1 + 0.8) - коэффициент восстановления (0.8 = 80% упругости)
            impulse = (dvx * nx + dvy * ny) * (1 + 0.8) / (1/self.mass + 1/other.mass)
            
            # Применяем импульс к первой фигуре (закон сохранения импульса)
            self.velocity.x -= impulse * nx / self.mass
            self.velocity.y -= impulse * ny / self.mass
            # Применяем противоположный импульс ко второй фигуре
            other.velocity.x += impulse * nx / other.mass
            other.velocity.y += impulse * ny / other.mass
            
            # Раздвигаем фигуры, чтобы избежать "залипания" при пересечении
            overlap = (self.size/2 + other.size/2) - distance
            if overlap > 0:
                # Первая фигура сдвигается вдоль нормали на половину пересечения
                self.x += nx * overlap * 0.5
                self.y += ny * overlap * 0.5
                # Вторая фигура сдвигается в противоположном направлении
                other.x -= nx * overlap * 0.5
                other.y -= ny * overlap * 0.5
                # Обновляем визуальное отображение обеих фигур
                self.update_position()
                other.update_position()


# Класс квадрата - наследуется от базового класса Shape
class Square(Shape):
    """Квадрат - падает без отскока благодаря низкому коэффициенту упругости"""
    # Переопределяем метод создания визуального представления для квадрата
    def create_shape(self):
        # Создаем прямоугольник на холсте с помощью метода create_rectangle
        self.shape_id = self.canvas.create_rectangle(
            # Левая граница: центр минус половина размера
            self.x - self.size/2, 
            # Верхняя граница: центр минус половина размера
            self.y - self.size/2,
            # Правая граница: центр плюс половина размера
            self.x + self.size/2, 
            # Нижняя граница: центр плюс половина размера
            self.y + self.size/2,
            # Цвет заливки
            fill=self.color, 
            # Цвет и толщина контура
            outline="black", width=2
        )
    
    # Переопределяем метод обновления позиции для квадрата
    def update_position(self):
        # Обновляем координаты прямоугольника на холсте
        self.canvas.coords(
            self.shape_id,
            self.x - self.size/2, self.y - self.size/2,
            self.x + self.size/2, self.y + self.size/2
        )
    
    # Переопределяем метод проверки попадания точки внутрь квадрата
    def contains_point(self, px, py):
        # Точка внутри квадрата, если её координаты находятся в пределах половины размера
        # от центра по обеим осям
        return (abs(px - self.x) <= self.size/2 and 
                abs(py - self.y) <= self.size/2)
    
    # Переопределяем метод обработки столкновения для квадрата (неупругое столкновение)
    def on_collision(self, other):
        """Неупругое столкновение - минимальный отскок, быстрая потеря энергии"""
        # Вычисляем вектор между центрами фигур
        dx = self.x - other.x
        dy = self.y - other.y
        # Вычисляем расстояние между центрами
        distance = math.hypot(dx, dy)
        
        # Проверяем факт столкновения
        if distance < (self.size/2 + other.size/2) and distance > 0:
            # Нормализуем вектор направления
            nx = dx / distance
            ny = dy / distance
            
            # Раздвигаем фигуры для предотвращения залипания
            overlap = (self.size/2 + other.size/2) - distance
            if overlap > 0:
                self.x += nx * overlap * 0.5
                self.y += ny * overlap * 0.5
                other.x -= nx * overlap * 0.5
                other.y -= ny * overlap * 0.5
                self.update_position()
                other.update_position()
            
            # Сильно гасим скорость обеих фигур (неупругое столкновение)
            # 0.95 означает потерю 5% скорости при каждом столкновении
            self.velocity.x *= 0.95
            self.velocity.y *= 0.95
            other.velocity.x *= 0.95
            other.velocity.y *= 0.95


# Класс треугольника - наследуется от базового класса Shape
class Triangle(Shape):
    """Треугольник - фигуры соскальзывают по его наклонным сторонам"""
    # Переопределяем конструктор для установки большей массы (треугольник почти неподвижен)
    def __init__(self, canvas, x, y, size, color, mass=2.0):
        # У треугольника больше масса (по умолчанию 2.0), чтобы он был "неподвижен"
        # при столкновениях с легкими фигурами
        super().__init__(canvas, x, y, size, color, mass)
        # Список вершин треугольника (каждая вершина - кортеж (x, y))
        self.points = []
    
    # Переопределяем метод создания визуального представления для треугольника
    def create_shape(self):
        # Вычисляем высоту равностороннего треугольника по формуле: h = a * sqrt(3) / 2
        h = self.size * math.sqrt(3) / 2
        # Определяем координаты трех вершин равностороннего треугольника
        self.points = [
            # Верхняя вершина (острие вверх)
            (self.x, self.y - h/2),
            # Левая нижняя вершина
            (self.x - self.size/2, self.y + h/2),
            # Правая нижняя вершина
            (self.x + self.size/2, self.y + h/2)
        ]
        # Создаем многоугольник на холсте с тремя вершинами
        self.shape_id = self.canvas.create_polygon(
            # Распаковываем список вершин в плоский список координат [x1, y1, x2, y2, x3, y3]
            *self._flatten_points(self.points),
            # Цвет заливки
            fill=self.color,
            # Цвет и толщина контура
            outline="black", width=2
        )
    
    # Вспомогательный метод: преобразование списка точек [(x1,y1), (x2,y2)] в [x1,y1,x2,y2]
    def _flatten_points(self, points):
        """Преобразовать список точек в плоский список координат для tkinter"""
        # Генератор списка: для каждой точки извлекаем обе координаты
        return [coord for point in points for coord in point]
    
    # Переопределяем метод обновления позиции для треугольника
    def update_position(self):
        # Пересчитываем координаты вершин при изменении позиции центра
        h = self.size * math.sqrt(3) / 2
        self.points = [
            (self.x, self.y - h/2),
            (self.x - self.size/2, self.y + h/2),
            (self.x + self.size/2, self.y + h/2)
        ]
        # Обновляем координаты многоугольника на холсте
        self.canvas.coords(self.shape_id, *self._flatten_points(self.points))
    
    # Переопределяем метод проверки попадания точки внутрь треугольника
    def contains_point(self, px, py):
        """Проверка точки внутри треугольника через барицентрические координаты"""
        # Вспомогательная функция для вычисления знака ориентации трех точек
        def sign(p1, p2, p3):
            # Возвращает положительное число, если точка p3 справа от вектора p1->p2
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        
        # Проверяем, находится ли точка по одну сторону от всех трех ребер треугольника
        b1 = sign((px, py), self.points[0], self.points[1]) < 0.0
        b2 = sign((px, py), self.points[1], self.points[2]) < 0.0
        b3 = sign((px, py), self.points[2], self.points[0]) < 0.0
        
        # Точка внутри треугольника, если все три проверки дали одинаковый результат
        return (b1 == b2) and (b2 == b3)
    
    # Метод определения нормали (перпендикуляра) к поверхности в точке контакта
    def get_surface_normal(self, px, py):
        """
        Определить нормаль к поверхности в точке контакта.
        Возвращает нормаль к ближайшей стороне треугольника.
        """
        # Инициализируем минимальное расстояние бесконечностью
        min_dist = float('inf')
        # Нормаль по умолчанию направлена вверх (0, -1)
        closest_normal = Vector(0, -1)
        
        # Проверяем все три стороны треугольника
        for i in range(3):
            # Берем две вершины, образующие сторону
            p1 = self.points[i]
            p2 = self.points[(i + 1) % 3]
            
            # Вычисляем вектор стороны (от p1 к p2)
            side_vec = Vector(p2[0] - p1[0], p2[1] - p1[1])
            # Нормаль к стороне получается поворотом вектора стороны на 90° против часовой
            normal = Vector(-side_vec.y, side_vec.x).normalize()
            
            # Вектор от первой вершины стороны к проверяемой точке
            to_point = Vector(px - p1[0], py - p1[1])
            # Длина проекции точки на сторону (параметр положения вдоль стороны)
            proj_length = (to_point.x * side_vec.x + to_point.y * side_vec.y) / side_vec.magnitude()
            # Ограничиваем проекцию пределами отрезка стороны
            proj_length = max(0, min(proj_length, side_vec.magnitude()))
            
            # Координаты ближайшей точки на стороне
            closest_point = Vector(
                p1[0] + side_vec.normalize().x * proj_length,
                p1[1] + side_vec.normalize().y * proj_length
            )
            
            # Расстояние от проверяемой точки до стороны
            dist = math.hypot(px - closest_point.x, py - closest_point.y)
            
            # Если эта сторона ближе предыдущих, запоминаем её нормаль
            if dist < min_dist:
                min_dist = dist
                # Проверяем направление нормали: должна быть НАРУЖУ треугольника
                center = Vector(self.x, self.y)
                to_center = Vector(center.x - closest_point.x, center.y - closest_point.y)
                # Если центр треугольника находится по ту же сторону от нормали - разворачиваем её
                if to_center.x * normal.x + to_center.y * normal.y > 0:
                    normal = Vector(-normal.x, -normal.y)
                closest_normal = normal
        
        # Возвращаем нормаль к ближайшей стороне
        return closest_normal
    
    # Переопределяем метод обработки столкновения для треугольника (соскальзывание)
    def on_collision(self, other):
        """
        Обработка столкновения: другие фигуры соскальзывают по сторонам треугольника.
        Треугольник почти неподвижен благодаря большой массе.
        """
        # Оптимизация: быстрая проверка пересечения ограничивающих прямоугольников
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)
        # Если фигуры слишком далеко друг от друга - столкновения нет
        if dx > (self.size/2 + other.size/2) or dy > (self.size/2 + other.size/2):
            return
        
        # Вычисляем высоту треугольника для дальнейших расчетов
        h = self.size * math.sqrt(3) / 2
        # Проверяем все три стороны треугольника на столкновение
        for i in range(3):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % 3]
            
            # Вектор стороны треугольника
            side_vec = Vector(p2[0] - p1[0], p2[1] - p1[1])
            # Вектор от вершины к центру другой фигуры
            to_point = Vector(other.x - p1[0], other.y - p1[1])
            
            # Нормаль к стороне (перпендикуляр), направленная наружу
            normal = Vector(-side_vec.y, side_vec.x).normalize()
            # Корректируем направление нормали наружу треугольника
            center_vec = Vector(self.x - p1[0], self.y - p1[1])
            if center_vec.x * normal.x + center_vec.y * normal.y > 0:
                normal = Vector(-normal.x, -normal.y)
            
            # Расстояние от центра фигуры до линии стороны (проекция на нормаль)
            distance = abs(to_point.x * normal.x + to_point.y * normal.y)
            
            # Если расстояние меньше радиуса фигуры + небольшой запас - есть столкновение
            if distance < other.size/2 + 2:
                # Точка проекции центра фигуры на линию стороны
                proj = to_point - normal * (to_point.x * normal.x + to_point.y * normal.y)
                proj_point = Vector(p1[0] + proj.x, p1[1] + proj.y)
                
                # Проверяем, что проекция лежит на отрезке стороны (не за его пределами)
                t = (proj.x * side_vec.x + proj.y * side_vec.y) / (side_vec.magnitude() ** 2)
                if 0 <= t <= 1:
                    # Раздвигаем фигуры чтобы избежать пересечения
                    overlap = other.size/2 + 2 - distance
                    if overlap > 0:
                        other.x += normal.x * overlap
                        other.y += normal.y * overlap
                        other.update_position()
                    
                    # Вычисляем касательный вектор (вдоль поверхности)
                    tangent = Vector(-normal.y, normal.x)
                    
                    # Скорость вдоль касательной (сохраняется при соскальзывании)
                    tangent_speed = other.velocity.x * tangent.x + other.velocity.y * tangent.y
                    
                    # Скорость по нормали (гасится при контакте с поверхностью)
                    normal_speed = other.velocity.x * normal.x + other.velocity.y * normal.y
                    
                    # Новая скорость: движение вдоль поверхности + слабое отталкивание от поверхности
                    other.velocity = tangent * tangent_speed + normal * (normal_speed * -0.3)
                    
                    # Добавляем эффект соскальзывания вниз по наклону
                    # Чем больше наклон (меньше |normal.y|), тем сильнее соскальзывание
                    if abs(normal.y) > 0.3:
                        slide_factor = 0.2 * (1 - abs(normal.y))
                        other.velocity.y += slide_factor * 2


# Основной класс симуляции - управляет всеми фигурами и физикой
class PhysicsSimulation:
    """Основной класс симуляции физики - координирует все объекты и анимацию"""
    # Конструктор приложения
    def __init__(self, root):
        # Сохраняем ссылку на главное окно tkinter
        self.root = root
        # Устанавливаем заголовок окна
        self.root.title("Симуляция")
        # Устанавливаем начальный размер окна (ширина x высота)
        self.root.geometry("900x650")
        # Разрешаем изменение размера окна пользователем
        self.root.resizable(True, True)
        
        # Параметры симуляции
        # Сила гравитации (ускорение вниз за один кадр)
        self.gravity = 0.3
        # Список всех фигур в симуляции
        self.shapes: List[Shape] = []
        # Текущая перетаскиваемая фигура (или None если ничего не перетаскивается)
        self.selected_shape: Optional[Shape] = None
        # Смещение курсора относительно центра фигуры при перетаскивании
        self.drag_offset = Vector(0, 0)
        # Флаг работы симуляции (пауза/старт)
        self.running = True
        
        # Настраиваем пользовательский интерфейс
        self.setup_ui()
        # Создаем начальные фигуры на холсте
        self.create_initial_shapes()
        # Запускаем основной цикл анимации
        self.animation_loop()
    
    # Метод настройки пользовательского интерфейса
    def setup_ui(self):
        """Настройка пользовательского интерфейса - панели управления и холст"""
        # Создаем верхнюю панель управления с серым фоном
        control_frame = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=10)
        # Размещаем панель вверху окна, растягивая по ширине
        control_frame.pack(fill=tk.X, side=tk.TOP)
        
        # Создаем заголовок приложения
        title_label = tk.Label(
            control_frame, 
            text="Симуляция", 
            font=("Arial", 16, "bold"),  # Жирный шрифт размером 16
            bg="#f0f0f0"  # Фон совпадает с панелью
        )
        # Размещаем заголовок слева с отступом справа
        title_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Создаем фрейм для ползунка гравитации
        gravity_frame = tk.Frame(control_frame, bg="#f0f0f0")
        gravity_frame.pack(side=tk.LEFT, padx=10)
        
        # Метка "Сила гравитации:"
        tk.Label(
            gravity_frame, 
            text="Сила гравитации:", 
            bg="#f0f0f0",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        # Создаем ползунок (шкалу) для регулировки гравитации
        self.gravity_slider = tk.Scale(
            gravity_frame,
            from_=0.0,      # Минимальное значение
            to=1.0,         # Максимальное значение
            resolution=0.05, # Шаг изменения
            orient=tk.HORIZONTAL,  # Горизонтальная ориентация
            length=200,     # Длина в пикселях
            bg="#f0f0f0",   # Цвет фона
            command=self.update_gravity  # Функция вызывается при изменении значения
        )
        # Устанавливаем начальное значение ползунка
        self.gravity_slider.set(self.gravity)
        # Размещаем ползунок в интерфейсе
        self.gravity_slider.pack(side=tk.LEFT)
        
        # Создаем фрейм для кнопок управления справа
        button_frame = tk.Frame(control_frame, bg="#f0f0f0")
        button_frame.pack(side=tk.RIGHT, padx=10)
        
        # Кнопка "Добавить круг"
        tk.Button(
            button_frame,
            text="Добавить круг",
            command=self.add_circle,  # Функция вызывается при нажатии
            bg="#4CAF50",             # Зеленый фон
            fg="black",               # Черный цвет текста (по требованию)
            padx=10,                  # Внутренний отступ по горизонтали
            pady=5,                   # Внутренний отступ по вертикали
            font=("Arial", 10, "bold") # Жирный шрифт для лучшей читаемости
        ).pack(side=tk.LEFT, padx=5)  # Размещаем слева с отступом 5px
        
        # Кнопка "Добавить квадрат"
        tk.Button(
            button_frame,
            text="Добавить квадрат",
            command=self.add_square,
            bg="#2196F3",    # Синий фон
            fg="black",
            padx=10,
            pady=5,
            font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        # Кнопка "Добавить треугольник"
        tk.Button(
            button_frame,
            text="Добавить треугольник",
            command=self.add_triangle,
            bg="#FF9800",    # Оранжевый фон
            fg="black",
            padx=10,
            pady=5,
            font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        # Кнопка "Сбросить" (возвращает начальное состояние)
        tk.Button(
            button_frame,
            text="Сбросить",
            command=self.reset_simulation,
            bg="#f44336",    # Красный фон
            fg="black",
            padx=10,
            pady=5,
            font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        # Кнопка "Пауза/Старт" (переключает симуляцию)
        tk.Button(
            button_frame,
            text="Пауза/Старт",
            command=self.toggle_simulation,
            bg="#9C27B0",    # Фиолетовый фон
            fg="black",
            padx=10,
            pady=5,
            font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        # Создаем холст для отрисовки фигур
        self.canvas = tk.Canvas(
            self.root, 
            width=850,                # Начальная ширина
            height=550,               # Начальная высота
            bg="#e8f4f8",             # Светло-голубой фон холста
            highlightthickness=1,     # Толщина границы холста
            highlightbackground="#aaa" # Цвет границы
        )
        # Размещаем холст с отступами, растягивая по свободному пространству
        self.canvas.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Привязываем обработчики событий мыши к холсту
        # Левая кнопка мыши нажата
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        # Движение мыши с зажатой левой кнопкой
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        # Левая кнопка мыши отпущена
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        # Изменение размера окна
        self.root.bind("<Configure>", self.on_resize)
    
    # Метод создания начальных фигур при запуске приложения
    def create_initial_shapes(self):
        """Создать начальные фигуры в определенных позициях"""
        # Получаем текущие размеры холста (или используем значения по умолчанию)
        canvas_width = self.canvas.winfo_width() or 850
        canvas_height = self.canvas.winfo_height() or 550
        
        # Вертикальная позиция "линии старта" для падающих фигур
        start_y = 80
        
        # Создаем два круга в верхней части экрана (будут отскакивать)
        self.shapes.append(Circle(self.canvas, canvas_width * 0.25, start_y, 50, "#4CAF50", mass=1.0))
        self.shapes.append(Circle(self.canvas, canvas_width * 0.35, start_y, 40, "#8BC34A", mass=0.8))
        
        # Создаем два квадрата (будут падать без отскока)
        self.shapes.append(Square(self.canvas, canvas_width * 0.55, start_y, 45, "#2196F3", mass=1.2))
        self.shapes.append(Square(self.canvas, canvas_width * 0.65, start_y, 55, "#03A9F4", mass=1.5))
        
        # Создаем два треугольника-платформы в нижней части экрана (фигуры будут соскальзывать)
        self.shapes.append(Triangle(self.canvas, canvas_width * 0.85, canvas_height * 0.7, 80, "#FF9800", mass=5.0))
        self.shapes.append(Triangle(self.canvas, canvas_width * 0.15, canvas_height * 0.6, 70, "#FF5722", mass=4.0))
    
    # Метод обновления силы гравитации при изменении ползунка
    def update_gravity(self, value):
        """Обновить силу гравитации из значения ползунка"""
        # Преобразуем строковое значение в число с плавающей точкой
        self.gravity = float(value)
    
    # Обработчик нажатия левой кнопки мыши
    def on_mouse_down(self, event):
        """Обработка нажатия мыши - выбор фигуры для перетаскивания"""
        # Ищем фигуру под курсором мыши, проверяя с конца списка (верхние фигуры первыми)
        for shape in reversed(self.shapes):
            # Проверяем, находится ли курсор внутри фигуры
            if shape.contains_point(event.x, event.y):
                # Запоминаем выбранную фигуру
                self.selected_shape = shape
                # Устанавливаем флаг перетаскивания
                self.selected_shape.is_dragged = True
                # Останавливаем фигуру (обнуляем скорость)
                self.selected_shape.velocity = Vector(0, 0)
                
                # Вычисляем смещение курсора относительно центра фигуры
                # Это нужно чтобы фигура перемещалась плавно, без "прыжка" к курсору
                self.drag_offset.x = event.x - self.selected_shape.x
                self.drag_offset.y = event.y - self.selected_shape.y
                
                # Перемещаем фигуру на передний план (поверх других фигур)
                self.canvas.tag_raise(self.selected_shape.shape_id)
                # Прерываем цикл - фигура найдена
                break
    
    # Обработчик движения мыши с зажатой кнопкой
    def on_mouse_drag(self, event):
        """Обработка перетаскивания фигуры мышью"""
        # Проверяем, что сейчас перетаскивается какая-то фигура
        if self.selected_shape:
            # Вычисляем новую позицию фигуры с учетом смещения курсора
            new_x = event.x - self.drag_offset.x
            new_y = event.y - self.drag_offset.y
            # Перемещаем фигуру на разницу между новой и текущей позицией
            self.selected_shape.move(new_x - self.selected_shape.x, new_y - self.selected_shape.y)
    
    # Обработчик отпускания кнопки мыши
    def on_mouse_up(self, event):
        """Обработка отпускания мыши - завершение перетаскивания"""
        # Если была выбрана фигура для перетаскивания
        if self.selected_shape:
            # Снимаем флаг перетаскивания
            self.selected_shape.is_dragged = False
            # Очищаем ссылку на выбранную фигуру
            self.selected_shape = None
    
    # Обработчик изменения размера окна
    def on_resize(self, event):
        """Обработка изменения размера окна - адаптация под новый размер"""
        # Проверяем, что событие относится к главному окну (а не к дочерним виджетам)
        if event.widget == self.root:
            # Обновляем позиции фигур под новые границы холста
            self.update_simulation_bounds()
    
    # Метод обновления границ симуляции при изменении размера окна
    def update_simulation_bounds(self):
        """Обновить границы симуляции при изменении размера окна"""
        # Получаем текущие размеры холста
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Перемещаем треугольники-платформы ближе к центру при изменении размера
        # Проверяем, что треугольники существуют (минимум 5 фигур в списке)
        if len(self.shapes) >= 5:
            # Правый треугольник - 85% ширины, 70% высоты
            self.shapes[-2].x = canvas_width * 0.85
            self.shapes[-2].y = canvas_height * 0.7
            self.shapes[-2].update_position()
            
            # Левый треугольник - 15% ширины, 60% высоты
            self.shapes[-1].x = canvas_width * 0.15
            self.shapes[-1].y = canvas_height * 0.6
            self.shapes[-1].update_position()
    
    # Метод добавления нового круга
    def add_circle(self):
        """Добавить новый круг в центр верхней части холста"""
        # Получаем ширину холста
        canvas_width = self.canvas.winfo_width() or 850
        # Создаем новый круг и добавляем в список фигур
        self.shapes.append(Circle(self.canvas, canvas_width * 0.5, 50, 45, "#4CAF50", mass=1.0))
    
    # Метод добавления нового квадрата
    def add_square(self):
        """Добавить новый квадрат в центр верхней части холста"""
        canvas_width = self.canvas.winfo_width() or 850
        self.shapes.append(Square(self.canvas, canvas_width * 0.5, 50, 50, "#2196F3", mass=1.2))
    
    # Метод добавления нового треугольника
    def add_triangle(self):
        """Добавить новый треугольник в центр нижней части холста"""
        canvas_width = self.canvas.winfo_width() or 850
        canvas_height = self.canvas.winfo_height() or 550
        self.shapes.append(Triangle(self.canvas, canvas_width * 0.5, canvas_height * 0.7, 75, "#FF9800", mass=5.0))
    
    # Метод сброса симуляции к начальному состоянию
    def reset_simulation(self):
        """Сбросить симуляцию - удалить все фигуры и создать заново"""
        # Удаляем все фигуры с холста через tkinter
        for shape in self.shapes:
            self.canvas.delete(shape.shape_id)
        
        # Очищаем список фигур
        self.shapes.clear()
        # Создаем начальный набор фигур
        self.create_initial_shapes()
    
    # Метод переключения паузы/старта симуляции
    def toggle_simulation(self):
        """Переключить паузу/старт симуляции - остановить или возобновить физику"""
        # Инвертируем флаг состояния
        self.running = not self.running
    
    # Метод проверки столкновений между всеми парами фигур
    def check_collisions(self):
        """Проверить столкновения между всеми фигурами в симуляции"""
        # Перебираем все пары фигур без повторений (каждую пару один раз)
        for i, shape1 in enumerate(self.shapes):
            for shape2 in self.shapes[i+1:]:
                # Пропускаем столкновения, если хотя бы одна фигура перетаскивается
                if shape1.is_dragged or shape2.is_dragged:
                    continue
                
                # Специальная обработка для треугольников: другие фигуры соскальзывают с них
                if isinstance(shape1, Triangle):
                    shape1.on_collision(shape2)
                elif isinstance(shape2, Triangle):
                    shape2.on_collision(shape1)
                else:
                    # Обычное столкновение между кругами и/или квадратами
                    shape1.on_collision(shape2)
    
    # Основной цикл анимации - вызывается постоянно для обновления состояния
    def animation_loop(self):
        """Основной цикл анимации - обновляет физику и положение всех фигур"""
        # Выполняем физические расчеты только если симуляция запущена (не на паузе)
        if self.running:
            # Получаем текущие размеры холста для обработки границ
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            # Применяем физику к каждой фигуре в симуляции
            for shape in self.shapes:
                # Физика не применяется к перетаскиваемым фигурам
                if not shape.is_dragged:
                    # Применяем гравитацию (ускорение вниз)
                    shape.apply_gravity(self.gravity)
                    # Применяем трение для замедления горизонтального движения
                    shape.apply_friction()
                    # Перемещаем фигуру согласно её текущей скорости
                    shape.move(shape.velocity.x, shape.velocity.y)
                    # Обрабатываем столкновения с границами холста с разной упругостью
                    if isinstance(shape, Circle):
                        # Круги: высокая упругость (0.75) - хорошо отскакивают
                        shape.resolve_boundary_collision(canvas_width, canvas_height, restitution=0.75)
                    elif isinstance(shape, Square):
                        # Квадраты: низкая упругость (0.15) - почти не отскакивают
                        shape.resolve_boundary_collision(canvas_width, canvas_height, restitution=0.15)
                    elif isinstance(shape, Triangle):
                        # Треугольники: очень низкая упругость, почти неподвижны
                        shape.velocity.x *= 0.95
                        shape.velocity.y *= 0.95
                        shape.resolve_boundary_collision(canvas_width, canvas_height, restitution=0.3)
            
            # Проверяем и обрабатываем столкновения между фигурами
            self.check_collisions()
        
        # Планируем следующий кадр анимации через 16 миллисекунд (~60 кадров в секунду)
        self.root.after(16, self.animation_loop)


# Точка входа в программу - выполняется только при запуске файла напрямую
if __name__ == "__main__":
    # Создаем главное окно приложения
    root = tk.Tk()
    # Создаем экземпляр симуляции, передавая ему главное окно
    app = PhysicsSimulation(root)
    # Запускаем главный цикл обработки событий tkinter
    root.mainloop()
