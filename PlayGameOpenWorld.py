import tkinter as tk
import random
import matplotlib.pyplot as plt
from game_functions import move_player, get_health_info, PoisonCloud
from Structure import Walls

class MiniGame:
    def __init__(self, master):
        self.master = master
        self.master.title("ТипоOpenGameWorld")
        self.master.geometry("550x600")  # Размер окна

        # Инициализация параметров мира
        self.world_size = 1001  # Размер мира (можно изменить)
        self.player_health = 100  # Текущее здоровье игрока
        self.max_health = 100  # Максимальное здоровье игрока (динамическая переменная)
        self.player_kringles = 0  # Количество кринжиков
        self.walls = Walls(self.world_size)  # Создание экземпляра класса Walls
        self.walls.generate_walls()  # Генерация стен с новыми параметрами
        self.cloud = PoisonCloud(self.world_size)
        self.cloud.generate_clouds()  # Генерация облаков с новыми параметрами
        self.restart_game()

    def restart_game(self):
        # Удаляем предыдущие элементы интерфейса
        for widget in self.master.winfo_children():
            widget.destroy()

        # Инициализация параметров игры
        self.player_x = random.randint(-self.world_size + 10, self.world_size - 10)
        self.player_y = random.randint(-self.world_size + 10, self.world_size - 10)
        self.player_health = self.max_health  # Восстанавливаем здоровье до максимума
        self.player_kringles = 0  # Сбрасываем количество кринжиков
        self.history = [(self.player_x, self.player_y)]

        # Создание пользовательского интерфейса
        self.label_position = tk.Label(self.master, text=f"Текущая позиция: X={self.player_x}, Y={self.player_y}")
        self.label_position.pack()

        self.label_health = tk.Label(self.master, text=get_health_info(self.player_health))
        self.label_health.pack()

        self.label_kringles = tk.Label(self.master, text=f"Кринжики: {self.player_kringles}")  # Метка для кринжиков
        self.label_kringles.pack()

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        # Создаем сетку 11x11
        self.grid_size = 11
        self.buttons = [[tk.Button(self.frame, width=4, height=2) for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.buttons[i][j].grid(row=i, column=j)

        # Обновление позиции игрока
        self.update_player_position()

        # Биндинг клавиш управления
        self.master.bind("<Up>", lambda event: self.move_player(0, 1))
        self.master.bind("<Down>", lambda event: self.move_player(0, -1))
        self.master.bind("<Left>", lambda event: self.move_player(-1, 0))
        self.master.bind("<Right>", lambda event: self.move_player(1, 0))
        self.master.bind("<Return>", lambda event: self.show_full_map())

    def move_player(self, dx, dy):
        new_x, new_y = move_player(self.player_x, self.player_y, dx, dy)
        if (
            -self.world_size <= new_x <= self.world_size and
            -self.world_size <= new_y <= self.world_size and
            not self.walls.is_in_wall(new_x, new_y)
        ):
            self.player_x, self.player_y = new_x, new_y
            self.check_poison_cloud()
            self.check_healing_potion()
            self.collect_kringles()  # Проверяем кучки кринжиков
            self.update_player_position()

    def check_poison_cloud(self):
        if self.cloud.is_in_cloud(self.player_x, self.player_y):
            self.player_health -= 1
            self.label_health.config(text=get_health_info(self.player_health))
            if self.player_health <= 0:
                self.restart_game()

    def check_healing_potion(self):
        """Проверяет, находится ли игрок в области аптечки."""
        if self.walls.interactive_items.is_in_potion(self.player_x, self.player_y):
            healing_amount = 25  # Количество здоровья, которое восстанавливает аптечка
            self.player_health = min(self.player_health + healing_amount, self.max_health)
            self.label_health.config(text=get_health_info(self.player_health))

    def collect_kringles(self):
        """Проверяет, находится ли игрок в области кучки кринжиков."""
        collected_kringles = self.walls.interactive_items.is_in_kringle_pile(self.player_x, self.player_y)
        if collected_kringles > 0:
            self.player_kringles += collected_kringles
            self.label_kringles.config(text=f"Кринжики: {self.player_kringles}")

    def update_player_position(self):
        # Сохраняем историю перемещений
        self.history.append((self.player_x, self.player_y))

        # Очищаем цвета кнопок
        for row in self.buttons:
            for button in row:
                button.config(bg="white")

        # Определяем видимую область (11x11 вокруг игрока)
        visible_area = {
            'min_x': self.player_x - 5,
            'max_x': self.player_x + 5,
            'min_y': self.player_y - 5,
            'max_y': self.player_y + 5
        }

        # Отображение объектов в видимой области
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x = visible_area['min_x'] + j
                y = visible_area['min_y'] + (self.grid_size - 1 - i)  # Инвертируем ось y

                if not (-self.world_size <= x <= self.world_size and -self.world_size <= y <= self.world_size):
                    self.buttons[i][j].config(bg="red")  # За пределами мира
                elif self.walls.is_in_wall(x, y):
                    self.buttons[i][j].config(bg="black")  # Стена
                elif self.cloud.is_in_cloud(x, y):
                    self.buttons[i][j].config(bg="green")  # Ядовитое облако
                elif any(
                    pile['x'] <= x <= pile['x'] + pile['width'] and
                    pile['y'] <= y <= pile['y'] + pile['height']
                    for pile in self.walls.interactive_items.kringle_piles
                ):
                    self.buttons[i][j].config(bg="yellow")  # Кучка кринжиков
                elif any(
                    potion['x'] <= x <= potion['x'] + potion['width'] and
                    potion['y'] <= y <= potion['y'] + potion['height']
                    for potion in self.walls.interactive_items.healing_potions
                ):
                    self.buttons[i][j].config(bg="orange")  # Аптечка
                elif x == self.player_x and y == self.player_y:
                    self.buttons[i][j].config(bg="blue")  # Игрок

        # Обновление метки позиции
        self.label_position.config(text=f"Текущая позиция: X={self.player_x}, Y={self.player_y}")

    def show_full_map(self):
        fig, ax = plt.subplots()
        ax.set_title('Полная карта мира')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        # Отображение истории перемещений
        x_values = [x for x, _ in self.history]
        y_values = [y for _, y in self.history]
        ax.plot(x_values, y_values, marker='o', color='b', alpha=0.5)
        ax.plot(x_values[-1], y_values[-1], marker='o', color='r', markersize=10)

        # Отображение границ мира
        world_boundary = self.world_size
        ax.plot(
            [-world_boundary, -world_boundary, world_boundary, world_boundary, -world_boundary],
            [-world_boundary, world_boundary, world_boundary, -world_boundary, -world_boundary],
            color='red'
        )

        # Отображение ядовитых облачков
        for cloud in self.cloud.clouds:
            ax.add_patch(plt.Rectangle((cloud['x'], cloud['y']), cloud['width'], cloud['height'], color='purple', alpha=0.5))

        # Отображение стен
        for wall in self.walls.walls:
            ax.add_patch(plt.Rectangle((wall['x'], wall['y']), wall['width'], wall['height'], color='black', alpha=0.5))

        # Отображение аптечек
        for potion in self.walls.interactive_items.healing_potions:
            ax.add_patch(plt.Rectangle((potion['x'], potion['y']), potion['width'], potion['height'], color='orange', alpha=0.7))

        # Отображение кучек кринжиков
        for pile in self.walls.interactive_items.kringle_piles:
            ax.add_patch(plt.Rectangle((pile['x'], pile['y']), pile['width'], pile['height'], color='yellow', alpha=0.7))

        plt.grid(True)
        plt.show()


def main():
    root = tk.Tk()
    game = MiniGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()