from src.ship import Ship
from src.dot import Dot


class Collor:
    BOLD = '\033[1m'
    END = '\033[0m'


class Board:
    """
    Класс отрисовки доски с расположением всех
    кораблей
    """
    def __init__(self, hid: bool = False):
        self.ships = []  # Список всеx кораблей доски
        self.dots_ships = []  # Список всех точек с контурами
        self.user_move = []  # Список всех выстрелов
        self.hid = hid  # Нужно ли скрывать корабль или нет (для вывода доски врага)
        self.col_life_ships = 7  # Количество живых кораблей на доске
        self.board = self.get_board()

    def get_board(self):
        """
        Метод создает двумерный список
        :return:
        """
        game_board = []
        for i in range(6):
            game_board.append(['О' for _i in range(6)])
        return game_board

    def add_ship(self, ship: Ship):
        """
        Метод добавляет корабль на доску
        :return:
        """
        try:
            for dot in ship.ship_dots():
                self.board[dot.x][dot.y] = chr(9632)  # ■
                self.dots_ships.append(dot)

            # Запоминаем сам корабль
            self.ships.append(ship)

            # И контур корабля
            self.dots_ships.extend(self.contour(ship))
            return True
        except Exception as e:
            raise 'Неудалось поставить корабль'

    def contour(self, ship: Ship):
        """
        Метод обводит корабль по контуру.
        Так как по ТЗ, корабли нужно ставить на расстоянии в 1 клетку
        :return: лист с точками контура корабля
            [Dot, Dot, ...]
        """
        contour_dots = []
        if ship.line_ship == 'horizontal':
            # 1. Добавляем точки верхнего и нижнего ряда
            for x in [ship.head_dot_ship.x - 1,
                      ship.head_dot_ship.x + 1]:
                if x >= 0 and x < 6:
                    y = ship.head_dot_ship.y - 1
                    for _i in range(ship.ship_length + 2):
                        if y >= 0:
                            dot = Dot(x, y)
                            if not self.out(dot):
                                contour_dots.append(dot)
                        y += 1

            y = ship.head_dot_ship.y + ship.ship_length
            if y < 6:
                contour_dots.append(Dot(ship.head_dot_ship.x, y))
            y = ship.head_dot_ship.y - 1
            if y >= 0:
                contour_dots.append(Dot(ship.head_dot_ship.x, y))

        if ship.line_ship == 'vertical':
            # 1. Добавляем точки левого и правого ряда
            for y in [ship.head_dot_ship.y - 1,
                      ship.head_dot_ship.y + 1]:
                if y >= 0 and y < 6:
                    x = ship.head_dot_ship.x - 1
                    for _i in range(ship.ship_length + 2):
                        if x >= 0:
                            dot = Dot(x, y)
                            if not self.out(dot):
                                contour_dots.append(dot)
                        x += 1

            x = ship.head_dot_ship.x + ship.ship_length
            if x < 6:
                contour_dots.append(Dot(x, ship.head_dot_ship.y))
            x = ship.head_dot_ship.x - 1
            if x >= 0:
                contour_dots.append(Dot(x, ship.head_dot_ship.y))

        return contour_dots

    def print_contour_kill_ship(self, x: int, y: int):
        """
        Метод добавляет контур на точку убитого корабля
        Нужно для дальнейшего отображения на доске
        :param x: строка
        :param y: столбец
        :return:
        """
        dot = Dot(x, y)
        for ship in self.ships:
            if dot not in ship.ship_dots():
                continue
            if ship.ship_life == 0:
                dots_contour = self.contour(ship)
                for _d in dots_contour:
                    self.shot(_d.x, _d.y)
            break

        return True

    def out(self, dot: Dot):
        """
        Метод для точки (объекта класса Dot) возвращает
            True, если точка выходит за пределы поля, и
            False, если не выходит
        :return:
        """
        try:
            _check_dot = self.board[dot.x][dot.y]
            return False
        except:
            return True

    def shot(self, x: int, y: int):
        """
        Метод делает выстрел по доске
        (если есть попытка выстрелить за пределы и в использованную точку,
        будет исключение).
        :return:
                True - игроку требуется повторный ход
                False - ход противника
        """
        try:
            if Dot(x, y) in self.user_move:
                print('\nВ эту клетку выстрел уже был. Попробуйте ещё раз.')
                return True
            # Если выстрела в указанную точку ещё не было
            if self.board[x][y] == 'О':
                # Если в этой клетки нет корабля - ставим T
                self.board[x][y] = f'{Collor.BOLD}T{Collor.END}'
                self.user_move.append(Dot(x, y))
                return False
            elif self.board[x][y] == chr(9632):
                # Если попали на корабль - Сообщаем, что корабль подбит
                self.board[x][y] = f'{Collor.BOLD}X{Collor.END}'

                self.user_move.append(Dot(x, y))

                return True
            else:
                raise Exception
        except Exception as e:
            print('\nВ указанную точку выстрелить нельзя. Попробуйте ещё раз')
            return True

    def take_life_ship(self, index_ship: int):
        """
        Метод отнимает жизнь у корабля
        :param index_ship: это индекс корабля в листе self.ships текущей доски
        :return: True
        """
        self.ships[index_ship].ship_life -= 1

        return True

    def current_game_board(self):
        """
        Метод возвращает текущую карту
        Формат:
          | 0 | 1 | 2 | 3 | 4 | 5 |
        1 | О | О | О | О | О | О |
        2 | О | О | О | О | О | О |
        3 | О | О | О | О | О | О |
        4 | О | О | О | О | О | О |
        5 | О | О | О | О | О | О |
        6 | О | О | О | О | О | О |

        :return:
        """
        header = ' | '.join([f'{Collor.BOLD}{index}{Collor.END}' for index in range(6)])
        st_map = [f'   {header} |']
        if self.hid:
            for i, l in enumerate(self.board):
                l = [i if i != chr(9632) else "О" for i in l]  # mask
                st_map.append(f'{Collor.BOLD}{i}{Collor.END}  | {" | ".join(l)} |')
        else:
            # Показываем доску с кораблями
            for i, l in enumerate(self.board):
                st_map.append(f'{Collor.BOLD}{i}{Collor.END}  | {" | ".join(l)} |')

        return st_map