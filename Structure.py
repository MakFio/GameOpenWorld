import random
import math
from IntItems import InteractiveItems

class Walls:
    def __init__(self, world_size):
        self.world_size = world_size
        self.walls = []
        self.interactive_items = InteractiveItems(world_size)  # Экземпляр для интерактивных предметов

    def generate_walls(self):
        num_castles = random.randint(5, 10)  # Общее количество замков

        for _ in range(num_castles):
            x_center = random.randint(-self.world_size + 50, self.world_size - 50)
            y_center = random.randint(-self.world_size + 50, self.world_size - 50)

            # Генерируем размер замка
            castle_width = random.randint(30, 40)
            castle_height = random.randint(30, 40)

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

                # Генерируем аптечки и кучки кринжиков вокруг замка
                self.interactive_items.generate_healing_potions(x_center, y_center, castle_width, castle_height)
                self.interactive_items.generate_kringle_piles_around_castle(x_center, y_center, castle_width, castle_height)

        # Генерируем кучки кринжиков по всей карте (за исключением области вокруг замков)
        self.interactive_items.generate_kringle_piles_global(self.walls, total_kringle_piles=0)

    def apply_destruction(self, walls):
        """Применяет эффект разрушения к стенам."""
        destroyed_walls = []
        for wall in walls:
            if random.random() < 0.8:  # 80% шанс оставить стену intact
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