class AppException(Exception):
    def __init__(self):
        self.message = 'Недопустимый ход. Попробуйте ещё раз'


class BoardOutException(AppException):
    """
    Игрок пытается выстрелить в клетку за пределами поля
    """

    def __init__(self):
        super(BoardOutException, self).__init__()
        self.message = 'Некорректный ход. Пожалуйста, введите координаты в пределах доски (от 0 до 5).' \
                       '\nПример: "Куда стреляем (строка, столбец)?: 1 5"\n'


class RepeatShotException(AppException):
    """
    Попытка сделать выстрел в клетку, куда уже стреляли
    """

    def __init__(self):
        super(RepeatShotException, self).__init__()
        self.message = 'В эту клетку выстрел уже был. Попробуйте ещё раз.'
