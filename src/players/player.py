from abc import ABC, abstractmethod
from src.board import Board, ResultShot


class Player(ABC):
    """
    Родитель класса для AI и User
    """

    def __init__(self):
        self.own_board = Board()  # Собственная доска
        self.enemy_s_board = Board(hid=True)  # Доска противника

    @abstractmethod
    def ask(self):
        """
        Метод «спрашивает» игрока, в какую клетку он делает выстрел
        :return:
        """
        # Если выстрел успешный - игрок повторяет ход
        pass

    def move(self) -> ResultShot:
        """
        Метод делает ход в игре
        :return: объект с результатом выстрела
        """
        x, y = self.ask()

        # Делаем выстрел по вражеской доске
        result = self.enemy_s_board.shot(x, y)

        # Если выстрел успешный
        if result.hit:
            # Отнимаем жизнь у корабля
            self.enemy_s_board.take_life_ship(result.index_ship)

            # Проверяем, убит ли полностью корабль. Если да - обводим контуром
            if self.enemy_s_board.print_contour_kill_ship(result.index_ship):
                self.enemy_s_board.col_life_ships -= 1

        return result


class User(Player):
    """
    Класс пользователя
    """

    def __init__(self):
        super(User, self).__init__()

    def ask(self):
        """
        Для игрока, метод спрашивает координаты с консоли
        :return:
        """
        x, y = str(input('\nКуда стреляем (строка, столбец)?: ')).strip().split(' ')
        return int(x), int(y)
