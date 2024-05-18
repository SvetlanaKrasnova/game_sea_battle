class Dot:
    """
    Класс точек на поле.
    Каждая точка описывается параметрами:
        Координата по оси x (номер строки).
        Координата по оси y (номер столбца).
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        """
        Для проверки точек на равенство.
        :param other:
        :return:
        """
        if not isinstance(other, Dot):
            raise Exception()

        return True if self.x == other.x and self.y == other.y else False

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: int):
        if value < 0:
            raise ValueError('Некорректный параметр')
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: int):
        if value < 0:
            raise ValueError('Некорректный параметр')
        self._y = value
