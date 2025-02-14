import random

class Shop:
    def __init__(self, world_size):
        self.world_size = world_size
        self.shops = []  # Список всех магазинов
        self.generate_shops()

    def generate_shops(self):
        """Генерирует магазины на карте."""
        min_shops = 1
        max_shops = 4
        num_shops = min_shops + random.randint(0, max_shops - min_shops)

        # Центры четырех областей карты
        center_points = [
            (-self.world_size // 2, self.world_size // 2),  # Левая верхняя область
            (self.world_size // 2, self.world_size // 2),   # Правая верхняя область
            (self.world_size // 2, -self.world_size // 2),  # Правая нижняя область
            (-self.world_size // 2, -self.world_size // 2)  # Левая нижняя область
        ]

        used_centers = set()  # Отслеживаем использованные центры

        for _ in range(num_shops):
            # Выбираем случайную область для магазина
            center_x, center_y = random.choice(center_points)
            if center_x in used_centers:
                continue  # Пропускаем уже использованные центры
            used_centers.add(center_x)

            # Добавляем погрешность к координатам центра
            center_x += random.randint(-100, 100)
            center_y += random.randint(-100, 100)

            # Генерируем размер магазина
            shop_width = 11
            shop_height = 11

            # Создаем стены вокруг магазина
            walls = [
                {'x': center_x - 5, 'y': center_y - 6, 'width': shop_width + 10, 'height': 3},  # Верхняя стена
                {'x': center_x - 5, 'y': center_y + shop_height + 3, 'width': shop_width + 10, 'height': 3},  # Нижняя стена
                {'x': center_x - 6, 'y': center_y - 5, 'width': 3, 'height': shop_height + 10},  # Левая стена
                {'x': center_x + shop_width + 3, 'y': center_y - 5, 'width': 3, 'height': shop_height + 10}  # Правая стена
            ]

            # Добавляем два обязательных входа
            entry_sides = random.sample(['top', 'bottom', 'left', 'right'], 2)  # Выбираем две стороны для входов

            if 'top' in entry_sides:
                walls[0]['width'] -= 6  # Уменьшаем ширину верхней стены
                walls[0]['x'] += 6
            if 'bottom' in entry_sides:
                walls[1]['width'] -= 6  # Уменьшаем ширину нижней стены
                walls[1]['x'] += 6
            if 'left' in entry_sides:
                walls[2]['height'] -= 6  # Уменьшаем высоту левой стены
                walls[2]['y'] += 6
            if 'right' in entry_sides:
                walls[3]['height'] -= 6  # Уменьшаем высоту правой стены
                walls[3]['y'] -= 6

            # Добавляем разрушения вокруг магазина
            rubble = self.generate_rubble(center_x, center_y, shop_width, shop_height)

            # Сохраняем информацию о магазине
            self.shops.append({
                'center_x': center_x,
                'center_y': center_y,
                'walls': walls,
                'rubble': rubble,
                'purchases': {}  # История покупок для увеличения цен
            })

    def generate_rubble(self, center_x, center_y, shop_width, shop_height):
        """Генерирует разрушения вокруг магазина."""
        rubble = []
        for _ in range(random.randint(5, 10)):  # От 5 до 10 разрушений
            rubble_x = random.randint(center_x - 30, center_x + shop_width + 30)
            rubble_y = random.randint(center_y - 30, center_y + shop_height + 30)
            rubble_width = random.randint(2, 5)
            rubble_height = random.randint(2, 5)
            rubble.append({'x': rubble_x, 'y': rubble_y, 'width': rubble_width, 'height': rubble_height})
        return rubble

    def is_in_shop(self, x, y):
        """Проверяет, находится ли игрок внутри магазина."""
        for shop in self.shops:
            if (
                shop['center_x'] - 5 <= x <= shop['center_x'] + 15 and
                shop['center_y'] - 5 <= y <= shop['center_y'] + 15
            ):
                return True
        return False

    def open_shop_menu(self, player_kringles, player_max_health):
        """Возвращает список товаров для магазина."""
        base_prices = {
            'Бинты': 5,
            'Аптечка': 15,
            'Набор травника': 30,
            'Улучшение здоровья': 50  # Начальная цена для улучшения здоровья
        }

        items = [
            {
                'name': 'Бинты',
                'cost': base_prices['Бинты'] + 5 * self.get_purchase_count('Бинты'),
                'effect': {'health_bonus': 10}
            },
            {
                'name': 'Аптечка',
                'cost': base_prices['Аптечка'] + 5 * self.get_purchase_count('Аптечка'),
                'effect': {'health_bonus': 20}
            },
            {
                'name': 'Набор травника',
                'cost': base_prices['Набор травника'] + 5 * self.get_purchase_count('Набор травника'),
                'effect': {'health_bonus': 50}
            },
            {
                'name': 'Улучшение здоровья',
                'cost': base_prices['Улучшение здоровья'] * (2 ** self.get_purchase_count('Улучшение здоровья')),
                'effect': {'max_health_bonus': 25}  # Эффект для увеличения максимального здоровья
            }
        ]
        return items

    def get_purchase_count(self, item_name):
        """Возвращает количество покупок конкретного товара."""
        for shop in self.shops:
            return shop['purchases'].get(item_name, 0)  # Возвращаем 0, если товар еще не покупался
        return 0