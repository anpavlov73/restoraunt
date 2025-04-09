class Restaurant:
    def __init__(self, name):
        self.name = name
        self.menu = Menu()  # Меню ресторана
        self.orders = []    # Список текущих заказов
        self.tables = []    # Список столиков

    def add_table(self, table):
        """Добавляет столик в ресторан"""
        self.tables.append(table)

    def take_order(self, table_number, order):
        """Принимает заказ для указанного столика"""
        for table in self.tables:
            if table.number == table_number:
                table.assign_order(order)
                self.orders.append(order)
                print(f'Заказ принят для столика {table_number}')
                return
        print('Столик не найден')

    def mark_order_ready(self, table_number):
        """Помечает заказ как готовый"""
        for order in self.orders:
            if order.table_number == table_number and not order.is_ready:
                order.mark_ready()
                print(f'Заказ для столика {table_number} готов.')
                return
        print(f'Заказ для столика {table_number} не найден или уже готов.')

    def deliver_order(self, table_number):
        """Отдает готовый заказ и удаляет его из списка"""
        for order in self.orders:
            if order.table_number == table_number and order.is_ready:
                self.orders.remove(order)
                print(f'Заказ для столика {table_number} отдан.')
                return
        print(f'Заказ для столика {table_number} не найден или еще не готов.')

    def show_menu(self):
        """Показывает меню ресторана"""
        self.menu.show_menu()

    def interface(self):
        """Основной интерфейс взаимодействия с рестораном"""
        while True:
            print(F'\nДобро пожаловать в ресторан {self.name}!')
            print('1. Показать меню')
            print('2. Создать заказ')
            print('3. Показать заказы')
            print('4. Показать столики')
            print('5. Отметить заказ как готовый')
            print('6. Отдать заказ')
            print('7. Выйти')
            choice = input('Выберите действие: ')

            if choice == '1':
                self.show_menu()
            elif choice == '2':
                self.create_order()
            elif choice == '3':
                self.show_orders()
            elif choice == '4':
                self.show_tables()
            elif choice == '5':
                table_number = int(input('Введите номер столика: '))
                self.mark_order_ready(table_number)
            elif choice == '6':
                table_number = int(input('Введите номер столика: '))
                self.deliver_order(table_number)
            elif choice == '7':
                break
            else:
                print('Неверный выбор. Попробуйте снова.')

    def create_order(self):
        """Создает новый заказ для столика"""
        self.show_tables()  # Показать доступные столики перед вводом номера столика
        table_number = int(input('Введите номер столика: '))
        if not self.is_table_exists(table_number):
            print('Столик не найден. Попробуйте снова.')
            return
        order = Order(table_number)
        while True:
            self.show_menu()
            dish_name = input('Введите название блюда для добавления в заказ (или Enter для завершения): ')
            if dish_name == '':
                break
            dish = self.menu.get_dish(dish_name)
            if dish:
                order.add_dish(dish)
                print(f'{dish_name} добавлен в заказ.')
            else:
                print('Блюдо не найдено в меню.')
        self.take_order(table_number, order)
        print(f'Итоговая стоимость заказа: {order.get_total()} руб.')

    def show_orders(self):
        """Показывает все текущие заказы"""
        print('\nТекущие заказы:')
        if not self.orders:
            print('Нет текущих заказов.')
        for order in self.orders:
            dishes = ', '.join(dish.name for dish in order.dishes)
            total = order.get_total()
            ready_status = 'Готов' if order.is_ready else 'Не готов'
            print(f'Столик {order.table_number}: {dishes} - {total} руб. ({ready_status})')

    def show_tables(self):
        """Показывает все столики в ресторане"""
        print('\nСписок столиков:')
        for table in self.tables:
            print(f'Столик {table.number}')

    def is_table_exists(self, table_number):
        """Проверяет, существует ли столик с указанным номером"""
        return any(table.number == table_number for table in self.tables)


class Menu:
    """Класс, представляющий меню ресторана"""
    def __init__(self):
        self.dishes = []  # Список блюд в меню

    def add_dish(self, dish):
        """Добавляет блюдо в меню"""
        self.dishes.append(dish)

    def remove_dish(self, dish_name):
        """Удаляет блюдо из меню по названию"""
        self.dishes = [dish for dish in self.dishes if dish.name != dish_name]

    def show_menu(self):
        """Выводит меню на экран"""
        print('\nМеню ресторана:')
        for dish in self.dishes:
            print(f'{dish.name} - {dish.price} руб.')

    def get_dish(self, dish_name):
        """Возвращает блюдо по названию или None, если не найдено"""
        for dish in self.dishes:
            if dish.name == dish_name:
                return dish
        return None


class Order:
    """Класс, представляющий заказ в ресторане"""
    def __init__(self, table_number):
        self.table_number = table_number  # Номер столика
        self.dishes = []                 # Список блюд в заказе
        self.is_ready = False            # Статус готовности заказа

    def add_dish(self, dish):
        """Добавляет блюдо в заказ"""
        self.dishes.append(dish)

    def remove_dish(self, dish_name):
        """Удаляет блюдо из заказа по названию"""
        self.dishes = [dish for dish in self.dishes if dish.name != dish_name]

    def get_total(self):
        """Возвращает общую стоимость заказа"""
        return sum(dish.price for dish in self.dishes)

    def mark_ready(self):
        """Помечает заказ как готовый"""
        self.is_ready = True


class Table:
    """Класс, представляющий столик в ресторане"""
    def __init__(self, number):
        self.number = number  # Номер столика
        self.order = None     # Текущий заказ для этого столика

    def assign_order(self, order):
        """Назначает заказ для этого столика"""
        self.order = order


class Dish:
    """Класс, представляющий блюдо в меню"""
    def __init__(self, name, price):
        self.name = name   # Название блюда
        self.price = price # Цена блюда


# Пример использования
restaurant = Restaurant('Гурман')

# Добавление блюд в меню
dish1 = Dish('Пицца', 500)
dish2 = Dish('Паста', 300)
dish3 = Dish('Кофе', 100)
restaurant.menu.add_dish(dish1)
restaurant.menu.add_dish(dish2)
restaurant.menu.add_dish(dish3)

# Добавление столиков
table1 = Table(1)
table2 = Table(2)
restaurant.add_table(table1)
restaurant.add_table(table2)

# Запуск интерфейса
restaurant.interface()
