from src.dot import Dot


class Ship:
    """
    Класс для представления коробля
    """

    def __init__(self, ship_length: int, line_ship: str, head_dot_ship: Dot):
        """
        :param ship_length: Длина корабля
        :param line_ship: Направление корабля (вертикальное/горизонтальное)
        :param head_dot_ship: Точка, где размещён нос корабля.
        :param line_ship: Количество жизней корабля
        """
        self.ship_length = ship_length
        self.ship_life = ship_length
        self.head_dot_ship = head_dot_ship
        self.line_ship = line_ship

    @property
    def ship_length(self):
        return self._ship_length

    @ship_length.setter
    def ship_length(self, value: int):
        if value <= 0:
            raise ValueError('Некорректное значение. Длинна корабля не может быть меньше или равно нулю!')
        self._ship_length = value

    @property
    def line_ship(self):
        return self._line_ship

    @line_ship.setter
    def line_ship(self, value: str):
        if not value in ['vertical', 'horizontal']:
            raise ValueError('Некорректный параметр. Нужно указать положение "vertical" или "horizontal"')
        self._line_ship = value

    def ship_dots(self):
        """
        Метод возвращает точки корабля
        :return: list
        """
        ship = []

        if self.line_ship == 'vertical':
            # Вертикальное расположение
            for i in range(self.ship_length):
                ship.append(Dot(self.head_dot_ship.x + i, self.head_dot_ship.y))
        else:
            # Горизонтальное расположение
            for i in range(self.ship_length):
                ship.append(Dot(self.head_dot_ship.x, self.head_dot_ship.y + i))
        return ship

    def dots(self):
        """
        Возвращает все точки корабля
        :return:
        """
        return self.ship_dots
