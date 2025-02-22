import tkinter as tk
import random
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
        self.max_health = 100  # Максимальное здоровье игрока
        self.player_kringles = 0  # Количество кринжиков
        self.history = []  # История перемещений

        # Спрашиваем игрока, как он хочет запустить игру
        self.ask_for_game_mode()

    def ask_for_game_mode(self):
        """Спрашивает игрока, как он хочет запустить игру."""
        self.mode_window = tk.Toplevel(self.master)
        self.mode_window.title("Сид есть? А если найду?")
        self.mode_window.geometry("320x200")

        tk.Label(self.mode_window, text="Введите seed для генерации мира (или оставьте пустым):").pack(pady=10)

        self.seed_entry = tk.Entry(self.mode_window)
        self.seed_entry.pack(pady=5)

        tk.Button(
            self.mode_window,
            text="Начать игру",
            command=self.start_game_with_seed
        ).pack(pady=5)

    def start_game_with_seed(self):
        """Запускает игру с указанным seed."""
        seed_input = self.seed_entry.get()
        seed = int(seed_input) if seed_input.isdigit() else None  # Если seed не указан, используем случайный

        # Закрываем окно выбора режима
        self.mode_window.destroy()

        # Инициализируем мир на основе seed
        self.walls = Walls(self.world_size, seed=seed)
        self.walls.generate_walls()

        # Инициализируем случайную позицию игрока
        self.player_x = random.randint(-self.world_size + 10, self.world_size - 10)
        self.player_y = random.randint(-self.world_size + 10, self.world_size - 10)

        # Создаем пользовательский интерфейс
        self.initialize_ui()

    def initialize_ui(self):
        """Инициализирует пользовательский интерфейс."""
        # Создание меток
        self.label_position = tk.Label(self.master, text=f"Текущая позиция: X={self.player_x}, Y={self.player_y}")
        self.label_position.pack()

        self.label_health = tk.Label(self.master, text=self.get_health_display())
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
        self.master.bind("<Return>", lambda event: self.show_full_map())  # Показываем полную карту
        self.master.bind("<Tab>", lambda event: self.open_shop_menu())  # Открываем меню магазина

    def get_health_display(self):
        """Возвращает строку для отображения здоровья."""
        return f"Здоровье: {self.player_health}/{self.max_health}"

    def move_player(self, dx, dy):
        new_x, new_y = move_player(self.player_x, self.player_y, dx, dy)
        if (
                -self.world_size <= new_x <= self.world_size and
                -self.world_size <= new_y <= self.world_size and
                not self.walls.is_in_wall(new_x, new_y)  # Проверяем только стены
        ):
            self.player_x, self.player_y = new_x, new_y

            # Проверяем ядовитые облака
            if self.walls.cloud.is_in_cloud(self.player_x, self.player_y):
                self.player_health -= 1
                self.label_health.config(text=self.get_health_display())
                if self.player_health <= 0:
                    self.restart_game()

            # Проверяем аптечки и кучки кринжиков
            self.check_healing_potion()
            self.collect_kringles()

            # Обновляем позицию игрока
            self.update_player_position()

    def check_healing_potion(self):
        """Проверяет, находится ли игрок в области аптечки."""
        objects = self.walls.get_objects_in_range(self.player_x, self.player_y)
        for obj in objects.get('interactive', []):  # Проверяем только интерактивные объекты
            if obj.get('width', None) == 4 and obj.get('height', None) == 4:  # Проверяем, является ли объект аптечкой
                # Проверяем, находится ли игрок в непосредственной близости от аптечки
                if (
                        obj['x'] <= self.player_x <= obj['x'] + obj['width'] and
                        obj['y'] <= self.player_y <= obj['y'] + obj['height']
                ):
                    healing_amount = 25  # Количество здоровья, которое восстанавливает аптечка
                    self.player_health = min(self.player_health + healing_amount, self.max_health)
                    self.label_health.config(text=self.get_health_display())

                    # Удаляем аптечку из списка и пространственной индексации
                    if obj in self.walls.interactive_items.healing_potions:
                        self.walls.interactive_items.healing_potions.remove(obj)
                        self.walls.remove_object_from_spatial_index(obj)
                    break

    def check_poison_cloud(self):
        """Проверяет, находится ли игрок в ядовитом облаке."""
        objects = self.walls.get_objects_in_range(self.player_x, self.player_y)
        for obj in objects.get('interactive', []):  # Проверяем только интерактивные объекты
            if obj.get('size', None) == 'cloud':  # Проверяем, является ли объект облаком
                # Проверяем, находится ли игрок в непосредственной близости от облака
                if (
                        obj['x'] <= self.player_x <= obj['x'] + obj['width'] and
                        obj['y'] <= self.player_y <= obj['y'] + obj['height']
                ):
                    self.player_health -= 1
                    self.label_health.config(text=self.get_health_display())
                    if self.player_health <= 0:
                        self.restart_game()
                    break

    def collect_kringles(self):
        """Проверяет, находится ли игрок в области кучки кринжиков."""
        objects = self.walls.get_objects_in_range(self.player_x, self.player_y)
        for obj in objects.get('interactive', []):  # Проверяем только интерактивные объекты
            if obj.get('kringles', None) is not None:  # Проверяем, является ли объект кучкой кринжиков
                # Проверяем, находится ли игрок в непосредственной близости от кучки кринжиков
                if (
                        obj['x'] <= self.player_x <= obj['x'] + obj['width'] and
                        obj['y'] <= self.player_y <= obj['y'] + obj['height']
                ):
                    collected_kringles = obj['kringles']
                    self.player_kringles += collected_kringles
                    self.label_kringles.config(text=f"Кринжики: {self.player_kringles}")

                    # Удаляем кучку кринжиков из списка и пространственной индексации
                    if obj in self.walls.interactive_items.kringle_piles:
                        self.walls.interactive_items.kringle_piles.remove(obj)
                        self.walls.remove_object_from_spatial_index(obj)  # Удаляем из пространственной индексации
                    break

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
                elif any(
                        cloud['x'] <= x <= cloud['x'] + cloud['width'] and
                        cloud['y'] <= y <= cloud['y'] + cloud['height']
                        for cloud in self.walls.cloud.clouds
                ):
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
                elif any(
                        shop['center_x'] - 5 <= x <= shop['center_x'] + 15 and
                        shop['center_y'] - 5 <= y <= shop['center_y'] + 15
                        for shop in self.walls.shop.shops
                ):
                    self.buttons[i][j].config(bg="purple")  # Магазин
                elif x == self.player_x and y == self.player_y:
                    self.buttons[i][j].config(bg="blue")  # Игрок

        # Обновление метки позиции
        self.label_position.config(text=f"Текущая позиция: X={self.player_x}, Y={self.player_y}")

    def open_shop_menu(self):
        """Открывает меню магазина, если игрок находится внутри."""
        shop = self.walls.shop.get_shop(self.player_x, self.player_y)
        if shop:
            items = self.walls.shop.open_shop_menu(self.player_kringles, self.max_health)

            # Создаем новое окно для меню магазина
            shop_window = tk.Toplevel(self.master)
            shop_window.title("Магазин")
            shop_window.geometry("300x300")

            # Отображаем информацию о кринжиках
            tk.Label(shop_window, text=f"Кринжики: {self.player_kringles}").pack(pady=5)

            # Добавляем кнопки для каждого товара
            for item in items:
                item_name = item['name']
                item_cost = item['cost']
                effect = item['effect']

                # Создаем кнопку для товара
                tk.Button(
                    shop_window,
                    text=f"{item_name} (+{effect.get('health_bonus', 0)}): {item_cost} кринжиков",
                    command=lambda cost=item_cost, health_bonus=effect.get('health_bonus', 0), max_bonus=effect.get('max_health_bonus', 0), name=item_name: self.buy_item(shop_window, cost, health_bonus, max_bonus, name)
                ).pack(pady=5)

            # Добавляем кнопку для выхода
            tk.Button(shop_window, text="Выход", command=shop_window.destroy).pack(pady=10)

    def buy_item(self, shop_window, cost, health_bonus, max_health_bonus, item_name):
        """Обрабатывает покупку выбранного товара."""
        if self.player_kringles >= cost:
            self.player_kringles -= cost
            if max_health_bonus > 0:  # Если товар увеличивает максимальное здоровье
                self.max_health += max_health_bonus
            else:  # Если товар восстанавливает текущее здоровье
                self.player_health = min(self.player_health + health_bonus, self.max_health)

            # Обновляем метки
            self.label_kringles.config(text=f"Кринжики: {self.player_kringles}")
            self.label_health.config(text=self.get_health_display())

            # Обновляем историю покупок в конкретном магазине
            for shop in self.walls.shop.shops:
                if shop['center_x'] - 5 <= self.player_x <= shop['center_x'] + 15 and \
                   shop['center_y'] - 5 <= self.player_y <= shop['center_y'] + 15:
                    shop['purchases'][item_name] = shop['purchases'].get(item_name, 0) + 1
                    break

            tk.messagebox.showinfo("Покупка успешна", f"Вы приобрели {item_name}.")
        else:
            tk.messagebox.showinfo("Недостаточно кринжиков", "У вас недостаточно кринжиков для покупки!")

        shop_window.destroy()  # Закрываем окно магазина

    def show_full_map(self):
        """Отображает полную карту мира с помощью Matplotlib."""
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        ax.set_title('Полная карта мира')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        # Отображение границ мира
        world_boundary = self.world_size
        ax.plot(
            [-world_boundary, -world_boundary, world_boundary, world_boundary, -world_boundary],
            [-world_boundary, world_boundary, world_boundary, -world_boundary, -world_boundary],
            color='red'
        )

        # Отображение стен
        for wall in self.walls.walls:
            ax.add_patch(plt.Rectangle((wall['x'], wall['y']), wall['width'], wall['height'], color='black', alpha=0.5))

        # Отображение ядовитых облачков
        for cloud in self.walls.cloud.clouds:
            ax.add_patch(plt.Rectangle((cloud['x'], cloud['y']), cloud['width'], cloud['height'], color='purple', alpha=0.5))

        # Отображение магазинов
        for shop in self.walls.shop.shops:
            ax.add_patch(plt.Rectangle(
                (shop['center_x'] - 5, shop['center_y'] - 5),
                11, 11,
                color='purple',
                alpha=0.7
            ))

        # Отображение аптечек
        for potion in self.walls.interactive_items.healing_potions:
            ax.add_patch(plt.Rectangle((potion['x'], potion['y']), potion['width'], potion['height'], color='orange', alpha=0.7))

        # Отображение кучек кринжиков
        for pile in self.walls.interactive_items.kringle_piles:
            ax.add_patch(plt.Rectangle((pile['x'], pile['y']), pile['width'], pile['height'], color='yellow', alpha=0.7))

        # Отображение игрока
        ax.plot(self.player_x, self.player_y, marker='o', color='r', markersize=10)

        plt.grid(True)
        plt.show()

    def restart_game(self):
        """Перезапускает игру."""
        # Удаляем предыдущие элементы интерфейса
        for widget in self.master.winfo_children():
            widget.destroy()

        # Инициализируем случайную позицию игрока
        self.player_x = random.randint(-self.world_size + 10, self.world_size - 10)
        self.player_y = random.randint(-self.world_size + 10, self.world_size - 10)
        self.player_health = self.max_health  # Восстанавливаем здоровье до максимума
        self.player_kringles = 0  # Сбрасываем количество кринжиков
        self.history = [(self.player_x, self.player_y)]  # Инициализируем историю перемещений

        # Создаем пользовательский интерфейс
        self.initialize_ui()


def main():
    root = tk.Tk()
    game = MiniGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()