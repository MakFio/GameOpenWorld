import random
import math

from IntItems import InteractiveItems
from Shop import Shop
from game_functions import PoisonCloud

class Walls:
    def __init__(self, world_size, seed=None):
        self.world_size = world_size
        self.seed = seed if seed is not None else random.randint(0, 1_000_000)  # Генерируем случайный seed, если не указан
        random.seed(self.seed)  # Устанавливаем seed для воспроизводимости
        self.walls = []
        self.interactive_items = InteractiveItems(world_size)  # Экземпляр для интерактивных предметов
        self.shop = Shop(world_size)  # Экземпляр для магазинов
        self.cloud = PoisonCloud(world_size)  # Экземпляр для ядовитых облаков
        self.grid_size = 50  # Размер секции (ячейки сетки)
        self.grid = {}  # Пространственная индексация

    def generate_walls(self):
        """Генерирует стены, замки, магазины, облака и интерактивные предметы."""
        num_castles = random.randint(5, 10)  # Общее количество замков

        for _ in range(num_castles):
            x_center = random.randint(-self.world_size + 50, self.world_size - 50)
            y_center = random.randint(-self.world_size + 50, self.world_size - 50)

            # Генерируем размер замка
            castle_width = random.randint(30, 60)
            castle_height = random.randint(30, 60)

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
                self.interactive_items.generate_kringle_piles_around_castle(
                    self.walls, x_center, y_center, castle_width, castle_height
                )

        # Генерируем кучки кринжиков по всей карте (за исключением области вокруг замков)
        self.interactive_items.generate_kringle_piles_global(self.walls, total_kringle_piles=0)

        # Генерируем магазины
        self.shop.generate_shops()

        # Генерируем ядовитые облака
        self.cloud.generate_clouds()

        # Интегрируем магазины в общий список стен
        self.integrate_shops()

        # Создаем пространственную индексацию
        self.create_spatial_index()

    def create_spatial_index(self):
        """Создает пространственную индексацию для стен и других объектов."""
        for wall in self.walls:
            grid_x = wall['x'] // self.grid_size
            grid_y = wall['y'] // self.grid_size
            key = (grid_x, grid_y)
            if key not in self.grid:
                self.grid[key] = {'walls': [], 'interactive': []}
            self.grid[key]['walls'].append(wall)

        for potion in self.interactive_items.healing_potions:
            grid_x = potion['x'] // self.grid_size
            grid_y = potion['y'] // self.grid_size
            key = (grid_x, grid_y)
            if key not in self.grid:
                self.grid[key] = {'walls': [], 'interactive': []}
            self.grid[key]['interactive'].append(potion)

        for pile in self.interactive_items.kringle_piles:
            grid_x = pile['x'] // self.grid_size
            grid_y = pile['y'] // self.grid_size
            key = (grid_x, grid_y)
            if key not in self.grid:
                self.grid[key] = {'walls': [], 'interactive': []}
            self.grid[key]['interactive'].append(pile)

        for cloud in self.cloud.clouds:
            grid_x = cloud['x'] // self.grid_size
            grid_y = cloud['y'] // self.grid_size
            key = (grid_x, grid_y)
            if key not in self.grid:
                self.grid[key] = {'walls': [], 'interactive': []}
            self.grid[key]['interactive'].append(cloud)

    def remove_object_from_spatial_index(self, obj):
        """Удаляет объект из пространственной индексации."""
        grid_x = obj['x'] // self.grid_size
        grid_y = obj['y'] // self.grid_size
        key = (grid_x, grid_y)

        if key in self.grid:
            # Удаляем объект из списка walls или interactive
            if 'walls' in obj:
                if obj in self.grid[key]['walls']:
                    self.grid[key]['walls'].remove(obj)
            else:
                if obj in self.grid[key]['interactive']:
                    self.grid[key]['interactive'].remove(obj)

            # Если ячейка пуста, удаляем её из сетки
            if not self.grid[key]['walls'] and not self.grid[key]['interactive']:
                del self.grid[key]


    def get_objects_in_range(self, x, y):
        """Возвращает объекты в текущей секции и соседних секциях."""
        grid_x = x // self.grid_size
        grid_y = y // self.grid_size
        objects = {'walls': [], 'interactive': []}

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                key = (grid_x + dx, grid_y + dy)
                if key in self.grid:
                    objects['walls'].extend(self.grid[key]['walls'])
                    objects['interactive'].extend(self.grid[key]['interactive'])

        return objects

    def is_in_wall(self, x, y):
        """Проверяет, находится ли точка (например, позиция игрока) внутри стены."""
        objects = self.get_objects_in_range(x, y)
        for obj in objects.get('walls', []):  # Проверяем только стены
            if (
                obj['x'] <= x <= obj['x'] + obj['width'] and
                obj['y'] <= y <= obj['y'] + obj['height']
            ):
                return True
        return False

    def integrate_shops(self):
        """Добавляет стены и разрушения магазинов в общий список."""
        for shop in self.shop.shops:
            self.walls.extend(shop['walls'])  # Добавляем стены магазина
            self.walls.extend(shop['rubble'])  # Добавляем разрушения вокруг магазина

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