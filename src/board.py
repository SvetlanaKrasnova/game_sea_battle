from typing import Optional
from src.dot import Dot
from src.ship import Ship
from exceptions.exceptions import BoardOutException, RepeatShotException, BadShipException


class Collor:
    """
    Это для раскраски текста для отображения
    позиций кораблей на доске. Чтоб лучше видно было
    """
    BOLD = '\033[1m'
    END = '\033[0m'


class ResultShot:
    """
    Класс описывает ответ выстрела по доске
    """

    def __init__(self, index_ship: Optional[int] = None, repeat_move: bool = True, hit: bool = False):
        """

        :param index_ship: Индекс корабля с доски (Board.ships.index(ship))
        :param repeat_move: Нужен ли повторный ход
        """
        self.repeat_move = repeat_move
        self.index_ship = index_ship
        self.hit = hit  # Попали или нет

    @property
    def index_ship(self):
        return self._index_ship

    @index_ship.setter
    def index_ship(self, value: Optional[int]):
        try:
            # Всего 7 кораблей
            if isinstance(value, bool):
                raise ValueError
            elif value is None:
                self._index_ship = value
            elif -1 < value < 7:
                self._index_ship = value
            else:
                raise ValueError
        except Exception as e:
            raise ValueError('Некорректно указан индекс корабля')


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
        # Двумерный список, в котором хранятся состояния каждой из клеток
        self.board = [['О' for _i in range(6)] for _ in range(6)]

    def add_ship(self, ship: Ship):
        """
        Метод добавляет корабль на доску
        :return:
        """
        try:
            for dot in ship.dots():
                self.board[dot.x][dot.y] = chr(9632)  # ■
                self.dots_ships.append(dot)

            # Запоминаем сам корабль
            self.ships.append(ship)

            # И контур корабля
            self.dots_ships.extend(self.contour(ship))
            return True
        except Exception as e:
            raise BadShipException(e)

    def check_hit(self, dot: Dot):
        """
        Метод по точке определяет какой это корабль.
        Если никакой - вернет None
        :param dot: точка выстрела
        :return: None - если не попали
                 index_ship - индекс корабля на доске, в который попали
        """
        index_ship = None
        for ship in self.ships:
            if dot in ship.dots():
                index_ship = self.ships.index(ship)

        return index_ship

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

    def print_contour_kill_ship(self, index_ship: int):
        """
        Метод добавляет контур убитого корабля
        Нужно для дальнейшего отображения на доске
        :param index_ship: индекс корабля из Board.ships
        :return:
                True - точки убитого корабля были добавлены
                False - у корабля ещё есть жизни (обводить не нужно)
        """
        if self.ships[index_ship].ship_life == 0:
            for dot in self.contour(self.ships[index_ship]):
                try:
                    self.shot(dot.x, dot.y)
                except:
                    # Если в эту точку ранее стрелял пользователь, например
                    pass

            return True

        return False

    def out(self, dot: Dot):
        """
        Метод для точки (объекта класса Dot). Проверяет,
        выходит ли точка за границы поля
        :param dot: объект точки
        :return: возвращает
                True, если точка выходит за пределы поля, и
                False, если не выходит
        """
        try:
            _check_dot = self.board[dot.x][dot.y]
            return False
        except Exception:
            return True

    def shot(self, x: int, y: int) -> ResultShot:
        """
        Метод делает выстрел по доске
        (если есть попытка выстрелить за пределы и в использованную точку,
        будет исключение).
        :return:
                BoardOutException - ход за пределы доски
                RepeatShotException - такой выстрел уже был
                ResultShot - результат выстрела
        """
        try:
            dot = Dot(x, y)

            # Проверяем, в пределах доски ли сделан ход
            if self.out(dot):
                raise BoardOutException()

            if dot in self.user_move:
                # Такой выстрел уже был
                raise RepeatShotException()

            if self.board[x][y] == 'О':
                # Если выстрела в указанную точку ещё не было - ставим T
                self.board[x][y] = f'{Collor.BOLD}T{Collor.END}'
                self.user_move.append(Dot(x, y))
                return ResultShot(repeat_move=False, hit=False)
            elif self.board[x][y] == chr(9632):
                # Если попали по кораблю - Сообщаем, что корабль подбит
                self.board[x][y] = f'{Collor.BOLD}X{Collor.END}'

                # Запоминаем точку выстрела
                self.user_move.append(dot)

                return ResultShot(repeat_move=True,  # Нужен повторный ход
                                  hit=True,  # Попали по кораблю
                                  index_ship=self.check_hit(dot))  # Какой именно это корабль
            else:
                raise Exception('Некорректный ход :(')

        except Exception as e:
            raise e

    def take_life_ship(self, index_ship: int):
        """
        Метод отнимает жизнь у корабля
        :param index_ship: это индекс корабля в листе self.ships текущей доски
        :return: True
        """
        self.ships[index_ship].ship_life -= 1

        return True

    def current_game_board(self) -> list:
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
        st_map = [f'     {header} |']
        if self.hid:
            for i, l in enumerate(self.board):
                l = [i if i != chr(9632) else "О" for i in l]  # mask
                st_map.append(f'{Collor.BOLD}{i}{Collor.END}  | {" | ".join(l)} |')
        else:
            # Показываем доску с кораблями
            for i, l in enumerate(self.board):
                st_map.append(f'{Collor.BOLD}{i}{Collor.END}  | {" | ".join(l)} |')

        return st_map
