import random
import math

def move_player(player_x, player_y, dx, dy):
    return player_x + dx, player_y + dy

def get_health_info(health):
    return f"Здоровье: {health}"

class PoisonCloud:
    def __init__(self, world_size):
        self.world_size = world_size
        self.clouds = []

    def generate_clouds(self):
        num_clouds = random.randint(75, 100)
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
                'height': 2 * radius
            }

            if not self.is_too_close(cloud):  # Проверяем близость к другим облакам
                self.clouds.append(cloud)

    def is_too_close(self, new_cloud):
        for cloud in self.clouds:
            distance = math.hypot(new_cloud['x'] - cloud['x'], new_cloud['y'] - cloud['y'])
            if distance < 40:  # Минимальное расстояние между облаками
                return True
        return False

    def is_in_cloud(self, x, y):
        for cloud in self.clouds:
            if (
                cloud['x'] <= x <= cloud['x'] + cloud['width'] and
                cloud['y'] <= y <= cloud['y'] + cloud['height']
            ):
                return True
        return False