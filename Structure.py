import random
import math

class Walls:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.healing_potions = []  # Список аптечек
        self.kringle_piles = []    # Список кучек кринжиков

    def generate_walls(self):
        num_castles = random.randint(5, 10)  # Общее количество замков
        total_kringle_piles = 0  # Счетчик кучек вне замков

        for _ in range(num_castles):
            x_center = random.randint(-self.width + 50, self.width - 50)
            y_center = random.randint(-self.height + 50, self.height - 50)

            # Генерируем размер замка
            castle_width = random.randint(40, 90)
            castle_height = random.randint(40, 90)

            # Создаем основу замка (прямоугольник)
            walls_to_add = [
                {'x': x_center, 'y': y_center, 'width': castle_width, 'height': 5},  # Верхняя стена
                {'x': x_center, 'y': y_center + castle_height - 5, 'width': castle_width, 'height': 5},  # Нижняя стена
                {'x': x_center, 'y': y_center, 'width': 5, 'height': castle_height},  # Левая стена
                {'x': x_center + castle_width - 5, 'y': y_center, 'width': 5, 'height': castle_height}  # Правая стена
            ]

            # Добавляем случайные внутренние стены для разнообразия
            if random.random() < 0.7:  # 70% шанс добавить внутреннюю стену
                inner_wall_x_min = x_center + 10
                inner_wall_x_max = x_center + castle_width - 15
                inner_wall_y_min = y_center + 10
                inner_wall_y_max = y_center + castle_height - 15

                if inner_wall_x_min < inner_wall_x_max and inner_wall_y_min < inner_wall_y_max:
                    inner_wall_x = random.randint(inner_wall_x_min, inner_wall_x_max)
                    inner_wall_y = random.randint(inner_wall_y_min, inner_wall_y_max)
                    walls_to_add.append({'x': inner_wall_x, 'y': inner_wall_y, 'width': 5, 'height': 10})

            # Применяем эффект разрушения (удаляем случайные части стен)
            walls_to_add = self.apply_destruction(walls_to_add)

            # Проверяем каждую стену на близость к существующим
            if all(not self.is_too_close(wall) for wall in walls_to_add):
                self.walls.extend(walls_to_add)

                # Генерируем аптечки возле замка
                self.generate_healing_potions(x_center, y_center, castle_width, castle_height)

                # Генерируем кучки кринжиков внутри и вокруг замка
                self.generate_kringle_piles_around_castle(x_center, y_center, castle_width, castle_height)

        # Генерируем кучки кринжиков по всей карте (за исключением области вокруг замков)
        self.generate_kringle_piles_global(total_kringle_piles)

    def apply_destruction(self, walls):
        """Применяет эффект разрушения к стенам."""
        destroyed_walls = []
        for wall in walls:
            if random.random() < 0.6:  # 60% шанс оставить стену intact
                destroyed_walls.append(wall)
        return destroyed_walls

    def is_too_close(self, new_wall):
        for wall in self.walls:
            distance = math.hypot(new_wall['x'] - wall['x'], new_wall['y'] - wall['y'])
            if distance < 60:  # Минимальное расстояние между замками
                return True
        return False

    def is_in_wall(self, x, y):
        for wall in self.walls:
            if (
                wall['x'] <= x <= wall['x'] + wall['width'] and
                wall['y'] <= y <= wall['y'] + wall['height']
            ):
                return True
        return False

    def generate_healing_potions(self, x_center, y_center, castle_width, castle_height):
        """Генерирует аптечки вокруг замка."""
        num_potions = random.randint(1, 7)  # От 1 до 7 аптечек
        for _ in range(num_potions):
            attempts = 0
            while attempts < 100:  # Максимум 100 попыток для каждой аптечки
                potion_x = random.randint(x_center - 30, x_center + castle_width + 20)
                potion_y = random.randint(y_center - 30, y_center + castle_height + 20)

                # Проверяем, что аптечка не находится внутри стен замка
                if not self.is_in_wall(potion_x, potion_y):
                    # Проверяем минимальное расстояние между аптечками
                    if all(math.hypot(potion_x - p['x'], potion_y - p['y']) >= 5 for p in self.healing_potions):
                        self.healing_potions.append({'x': potion_x, 'y': potion_y, 'width': 4, 'height': 4})
                        break
                attempts += 1

    def is_in_potion(self, x, y):
        """Проверяет, находится ли игрок в области аптечки."""
        for potion in self.healing_potions[:]:  # Итерируемся по копии списка
            if (
                potion['x'] <= x <= potion['x'] + potion['width'] and
                potion['y'] <= y <= potion['y'] + potion['height']
            ):
                self.healing_potions.remove(potion)  # Удаляем аптечку после использования
                return True
        return False

    def generate_kringle_piles_around_castle(self, x_center, y_center, castle_width, castle_height):
        """Генерирует кучки кринжиков внутри и вокруг замка."""
        max_piles = 20  # Максимум 20 кучек вокруг замка

        # Генерация кучек внутри замка (только большие)
        num_inside = random.randint(1, min(3, castle_width // 20))  # Зависит от размера замка
        for _ in range(num_inside):
            attempts = 0
            while attempts < 100:
                pile_x = random.randint(x_center + 5, x_center + castle_width - 9)
                pile_y = random.randint(y_center + 5, y_center + castle_height - 9)
                if not self.is_in_wall(pile_x, pile_y):
                    self.kringle_piles.append({'x': pile_x, 'y': pile_y, 'size': 'large', 'kringles': 15, 'width': 4, 'height': 4})
                    break
                attempts += 1

        # Генерация кучек вокруг замка (малые и средние)
        num_around = random.randint(5, max_piles - num_inside)
        for _ in range(num_around):
            attempts = 0
            while attempts < 100:
                pile_x = random.randint(x_center - 40, x_center + castle_width + 40)
                pile_y = random.randint(y_center - 40, y_center + castle_height + 40)
                if not self.is_in_wall(pile_x, pile_y):
                    category = random.choices(['small', 'medium'], weights=[0.6, 0.4])[0]
                    if category == 'small':
                        self.kringle_piles.append({'x': pile_x, 'y': pile_y, 'size': 'small', 'kringles': 2, 'width': 1, 'height': 1})
                    else:
                        self.kringle_piles.append({'x': pile_x, 'y': pile_y, 'size': 'medium', 'kringles': 5, 'width': 2, 'height': 2})
                    break
                attempts += 1

    def generate_kringle_piles_global(self, total_kringle_piles):
        """Генерирует кучки кринжиков по всей карте (за исключением области вокруг замков)."""
        while total_kringle_piles < 250:
            x = random.randint(-self.width + 10, self.width - 10)
            y = random.randint(-self.height + 10, self.height - 10)
            if not any(
                math.hypot(x - castle['x'], y - castle['y']) < 40
                for castle in self.walls
            ):
                category = random.choices(['small', 'medium'], weights=[0.7, 0.3])[0]
                if category == 'small':
                    self.kringle_piles.append({'x': x, 'y': y, 'size': 'small', 'kringles': 2, 'width': 1, 'height': 1})
                else:
                    self.kringle_piles.append({'x': x, 'y': y, 'size': 'medium', 'kringles': 5, 'width': 2, 'height': 2})
                total_kringle_piles += 1

    def is_in_kringle_pile(self, x, y):
        """Проверяет, находится ли игрок в области кучки кринжиков."""
        for pile in self.kringle_piles[:]:  # Итерируемся по копии списка
            if (
                pile['x'] <= x <= pile['x'] + pile['width'] and
                pile['y'] <= y <= pile['y'] + pile['height']
            ):
                kringles = pile['kringles']
                self.kringle_piles.remove(pile)  # Удаляем кучку после использования
                return kringles
        return 0