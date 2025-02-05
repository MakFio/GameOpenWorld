import random
import math

class Walls:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []

    def generate_walls(self):
        num_walls = random.randint(15, 30)
        for _ in range(num_walls):
            x_center = random.randint(-self.width + 30, self.width - 30)  # Увеличили отступы
            y_center = random.randint(-self.height + 30, self.height - 30)
            radius = random.randint(5, 30)  # Увеличили диапазон радиуса

            walls_to_add = [
                {'x': x_center - radius, 'y': y_center - 5, 'width': 40, 'height': 10},  # Горизонтальная стена 1
                {'x': x_center + 50 - radius, 'y': y_center - 5, 'width': 40, 'height': 10},  # Горизонтальная стена 2
                {'x': x_center - 8 - radius, 'y': y_center - 10, 'width': 10, 'height': 90},  # Вертикальная стена 1
                {'x': x_center + 90 - radius, 'y': y_center - 10, 'width': 10, 'height': 90},  # Вертикальная стена 2
                {'x': x_center - 8 - radius, 'y': y_center + 90, 'width': 100, 'height': 10}  # Горизонтальная стена 3
            ]

            if all(not self.is_too_close(wall) for wall in walls_to_add):
                self.walls.extend(walls_to_add)

    def is_too_close(self, new_wall):
        for wall in self.walls:
            distance = math.hypot(new_wall['x'] - wall['x'], new_wall['y'] - wall['y'])
            if distance < 40:  # Увеличили минимальное расстояние
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