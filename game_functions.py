import random
import math

def move_player(player_x, player_y, dx, dy):
    return player_x + dx, player_y + dy

def get_health_info(health):
    return f"Здоровье: {health}"

class PoisonCloud:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.clouds = []

    def generate_clouds(self):
        num_clouds = random.randint(75, 100)
        for _ in range(num_clouds):
            x_center = random.randint(-self.width + 30, self.width - 30)  # Увеличили отступы
            y_center = random.randint(-self.height + 30, self.height - 30)
            radius = random.randint(5, 30)  # Увеличили диапазон радиуса

            cloud = {
                'x': x_center - radius,
                'y': y_center - radius,
                'width': 2 * radius,
                'height': 2 * radius
            }

            if not self.is_too_close(cloud):
                self.clouds.append(cloud)

    def is_too_close(self, new_cloud):
        for cloud in self.clouds:
            distance = math.hypot(new_cloud['x'] - cloud['x'], new_cloud['y'] - cloud['y'])
            if distance < 40:  # Увеличили минимальное расстояние
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