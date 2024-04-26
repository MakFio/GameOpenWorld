# Тут игровые функции
import random
import math

def move_player(player_x, player_y, dx, dy):
    new_x = player_x + dx
    new_y = player_y + dy
    return new_x, new_y

def get_health_info(health):
    return "Здоровье: {}".format(health)

class PoisonCloud:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.clouds = []

    def generate_clouds(self):
        num_clouds = random.randint(75, 100)
        for _ in range(num_clouds):
            x_center = random.randint(-self.width + 25, self.width - 25)
            y_center = random.randint(-self.height + 25, self.height - 25)
            radius = random.randint(3, 25)
            cloud = {'x': x_center - radius, 'y': y_center - radius, 'width': 2 * radius, 'height': 2 * radius}
            if not self.is_too_close(cloud):
                self.clouds.append(cloud)

    def is_too_close(self, new_cloud):
        for cloud in self.clouds:
            distance = math.sqrt((new_cloud['x'] - cloud['x']) ** 2 + (new_cloud['y'] - cloud['y']) ** 2)
            if distance < 30:
                return True
        return False

    def is_in_cloud(self, x, y):
        for cloud in self.clouds:
            x_min = cloud['x']
            x_max = cloud['x'] + cloud['width']
            y_min = cloud['y']
            y_max = cloud['y'] + cloud['height']
            if x_min <= x <= x_max and y_min <= y <= y_max:
                return True
        return False

