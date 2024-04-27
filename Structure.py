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

            # Генерация первого горизонтального блока
            wall1 = {'x': x_center - radius, 'y': y_center - 3, 'width': 30, 'height': 6}

            # Генерация второго горизонтального блока
            wall2 = {'x': x_center + 40 - radius, 'y': y_center - 3, 'width': 30, 'height': 6}

            # Генерация первого вертикального блока, начиная от начала первого горизонтального блока
            wall3 = {'x': x_center - 6 - radius, 'y': y_center - 5, 'width': 6, 'height': 80}

            # Генерация второго вертикального блока, начиная от конца второго горизонтального блока
            wall4 = {'x': x_center + 70 - radius, 'y': y_center - 5, 'width': 6, 'height': 80}

            # Генерация третьего горизонтального блока
            wall5 = {'x': x_center - 6 - radius, 'y': y_center + 75, 'width': 82, 'height': 6}

            if not self.is_too_close(wall1) and not self.is_too_close(wall2) \
                    and not self.is_too_close(wall3) and not self.is_too_close(wall4):
                self.walls.append(wall1)
                self.walls.append(wall2)
                self.walls.append(wall3)
                self.walls.append(wall4)
                self.walls.append(wall5)

    def is_too_close(self, new_wall):
        for wall in self.walls:
            distance = math.sqrt((new_wall['x'] - wall['x']) ** 2 + (new_wall['y'] - wall['y']) ** 2)
            if distance < 30:
                return True
        return False

    def is_in_wall(self, x, y):
        for wall in self.walls:
            x_min = wall['x']
            x_max = wall['x'] + wall['width']
            y_min = wall['y']
            y_max = wall['y'] + wall['height']
            if x_min <= x <= x_max and y_min <= y <= y_max:
                return True
        return False
