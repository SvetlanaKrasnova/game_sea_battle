class BoardOutException(Exception):
    """
    Игрок пытается выстрелить в клетку за пределами поля
    """

    def __init__(self):
        self.message = 'Некорректный ход. Пожалуйста, введите координаты в пределах доски (от 0 до 5).' \
                       '\nПример: "Куда стреляем (строка, столбец)?: 1 5"\n'


class BadShipException(Exception):
    """
    Возникает, если неудалось поставить корабль на доску
    """

    def __init__(self, ex):
        self.exception = ex
        self.message = 'Неудалось поставить корабль'


class RepeatShotException(Exception):
    """
    Попытка сделать выстрел в клетку, куда уже стреляли
    """

    def __init__(self):
        super(RepeatShotException, self).__init__()
        self.message = 'В эту клетку выстрел уже был. Попробуйте ещё раз.'


class NotFreeCellAIException(Exception):
    """
    Игра ещё идет, но у AI не осталось клеток.
    """

    def __init__(self):
        super(NotFreeCellAIException, self).__init__()
        self.message = 'Ошибка AI: Что-то совсем пошло не так. Не осталось свободных ячеек.\n' \
                       'Попробуйте сыграть ещё раз.'
