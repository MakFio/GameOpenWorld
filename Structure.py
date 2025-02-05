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
            x_center = random.randint(-self.width + 25, self.width - 25)
            y_center = random.randint(-self.height + 25, self.height - 25)
            radius = random.randint(3, 25)

            walls_to_add = [
                {'x': x_center - radius, 'y': y_center - 3, 'width': 30, 'height': 6},  # Горизонтальная стена 1
                {'x': x_center + 40 - radius, 'y': y_center - 3, 'width': 30, 'height': 6},  # Горизонтальная стена 2
                {'x': x_center - 6 - radius, 'y': y_center - 5, 'width': 6, 'height': 80},  # Вертикальная стена 1
                {'x': x_center + 70 - radius, 'y': y_center - 5, 'width': 6, 'height': 80},  # Вертикальная стена 2
                {'x': x_center - 6 - radius, 'y': y_center + 75, 'width': 82, 'height': 6}  # Горизонтальная стена 3
            ]

            # Проверяем каждую стену на близость к существующим
            if all(not self.is_too_close(wall) for wall in walls_to_add):
                self.walls.extend(walls_to_add)

    def is_too_close(self, new_wall):
        for wall in self.walls:
            distance = math.sqrt((new_wall['x'] - wall['x']) ** 2 + (new_wall['y'] - wall['y']) ** 2)
            if distance < 30:
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