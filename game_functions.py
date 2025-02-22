import random
import math

def move_player(player_x, player_y, dx, dy):
    """
    Обрабатывает перемещение игрока на карте.
    :param player_x: Текущая координата X игрока.
    :param player_y: Текущая координата Y игрока.
    :param dx: Изменение по оси X (например, +1 для движения вправо).
    :param dy: Изменение по оси Y (например, -1 для движения вниз).
    :return: Новые координаты игрока.
    """
    return player_x + dx, player_y + dy


def get_health_info(health, max_health):
    """
    Возвращает строку с информацией о здоровье игрока.
    :param health: Текущее здоровье игрока.
    :param max_health: Максимальное здоровье игрока.
    :return: Строка в формате "Здоровье: X/Y".
    """
    return f"Здоровье: {health}/{max_health}"


class PoisonCloud:
    def __init__(self, world_size):
        self.world_size = world_size
        self.clouds = []  # Список всех ядовитых облаков

    def generate_clouds(self):
        """Генерирует ядовитые облака на карте."""
        num_clouds = random.randint(75, 100)  # Количество облаков

        for _ in range(num_clouds):
            x_center = random.randint(-self.world_size + 30, self.world_size - 30)
            y_center = random.randint(-self.world_size + 30, self.world_size - 30)

            # Определяем категорию облака (Малое, Среднее, Большое)
            category = random.choices(
                ['small', 'medium', 'large'],
                weights=[0.6, 0.3, 0.1]  # Вероятности: 60%, 30%, 10%
            )[0]

            # Генерируем размер в зависимости от категории
            if category == 'small':
                radius = random.randint(5, 10)  # Малые облака
            elif category == 'medium':
                radius = random.randint(11, 22)  # Средние облака
            else:  # large
                radius = random.randint(23, 35)  # Большие облака

            cloud = {
                'x': x_center - radius,
                'y': y_center - radius,
                'width': 2 * radius,
                'height': 2 * radius,
                'size': category  # Добавляем категорию для идентификации
            }

            if not self.is_too_close(cloud):  # Проверяем близость к другим облакам
                self.clouds.append(cloud)

    def is_too_close(self, new_cloud):
        """Проверяет, находится ли новое облако слишком близко к существующим."""
        for cloud in self.clouds:
            distance = math.hypot(new_cloud['x'] - cloud['x'], new_cloud['y'] - cloud['y'])
            if distance < 40:  # Минимальное расстояние между облаками
                return True
        return False

    def is_in_cloud(self, x, y):
        """Проверяет, находится ли игрок внутри ядовитого облака."""
        for cloud in self.clouds:
            if (
                cloud['x'] <= x <= cloud['x'] + cloud['width'] and
                cloud['y'] <= y <= cloud['y'] + cloud['height']
            ):
                return True
        return False