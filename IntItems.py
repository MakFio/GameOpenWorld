import random
import math

class InteractiveItems:
    def __init__(self, world_size):
        self.world_size = world_size
        self.healing_potions = []  # Список аптечек
        self.kringle_piles = []    # Список кучек кринжиков

    def generate_healing_potions(self, x_center, y_center, castle_width, castle_height):
        """Генерирует аптечки вокруг замка."""
        num_potions = random.randint(1, 7)  # От 1 до 7 аптечек
        for _ in range(num_potions):
            attempts = 0
            while attempts < 100:  # Максимум 100 попыток для каждой аптечки
                potion_x = random.randint(x_center - 30, x_center + castle_width + 20)
                potion_y = random.randint(y_center - 30, y_center + castle_height + 20)

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
                category = random.choices(['small', 'medium'], weights=[0.6, 0.4])[0]
                if category == 'small':
                    self.kringle_piles.append({'x': pile_x, 'y': pile_y, 'size': 'small', 'kringles': 2, 'width': 1, 'height': 1})
                else:
                    self.kringle_piles.append({'x': pile_x, 'y': pile_y, 'size': 'medium', 'kringles': 5, 'width': 2, 'height': 2})
                break
            attempts += 1

    def generate_kringle_piles_global(self, walls, total_kringle_piles=0):
        """Генерирует кучки кринжиков по всей карте (за исключением области вокруг замков)."""
        while total_kringle_piles < 250:
            x = random.randint(-self.world_size + 10, self.world_size - 10)
            y = random.randint(-self.world_size + 10, self.world_size - 10)
            if not any(
                math.hypot(x - wall['x'], y - wall['y']) < 40
                for wall in walls
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