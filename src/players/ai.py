import random
from typing import Optional
from datetime import datetime
from .player import Player
from src.dot import Dot
from exceptions.exceptions import BoardOutException, RepeatShotException, NotFreeCellAIException

class AI(Player):
    """
    Противник/Напарник.
    """

    def __init__(self):
        super(AI, self).__init__()
        self._last_hit: Optional[Dot] = None # Последня ячейка с попаданием в какой-нибудь корабль

    def neighbors(self, index: int) -> list:
        """
        Метод возвращает число стоящее перед index и после него
        :param index: число от которого считаем
        :return:
        """
        return [index + 1, index - 1]

    def _generation_cell(self) -> list:
        """
        Метод генерирует 4 соседние ячейки (если они не выходят за границу)
        Например:
            Точка старта 1,4
            Результат метода 1,3 1,5 0,4 2,4
        :return: list[Dot]
        """
        dots = [[x, y] for x, y in zip(self.neighbors(self._last_hit.x), [self._last_hit.y] * 2)]
        dots.extend([[x, y] for x, y in zip([self._last_hit.x] * 2, self.neighbors(self._last_hit.y))])

        free_dots = []

        # Формируем точки
        for _d in dots:
            try:
                _dot = Dot(_d[0], _d[1])

                # Если выходит за границу - не берем
                if self.enemy_s_board.out(_dot):
                    raise BoardOutException()

                # Если стреляли в клетку - не берем
                if _dot in self.enemy_s_board.user_move:
                    raise RepeatShotException()
            except:
                continue

            free_dots.append(Dot(_d[0], _d[1]))

        return free_dots

    def _random_cell(self) -> Dot:
        """
        Метод генерирует случайную клетку.
        На определение свободной клетки даётся 2 секунды.
        Если за это время выбор будет попадать на уже занятые клетки
         - то вернется ошибка
        :return: Dot
        """
        start_time = datetime.now()
        while int((datetime.now() - start_time).total_seconds()) <= 2:
            x = random.randrange(5)
            y = random.randrange(5)
            if Dot(x, y) in self.enemy_s_board.user_move:
                continue
            break
        else:
            raise TimeoutError('Время генерации значений вышло')
        return Dot(x, y)

    def get_first_free_cell(self):
        """
        Метод возвращает первую ячейка сверху по которой AI ещё не стрелял
        :return: Dot
        """
        # 1. Оставляем только те клетки, по которым мы ещё не стреляли

        for i, l in enumerate(self.enemy_s_board.board):
            for k, j in enumerate(l):
                if not Dot(i, k) in self.enemy_s_board.user_move:
                    return Dot(i, k)

        # На всякий случай. Пустоту возвращать - такой себе вариант
        raise NotFreeCellAIException()

    def ask(self):
        """
        Метод по выбору свободной клетки
        :return: x: int, y: int
        """
        # Если попадания не было - выбираем случайную клетку
        if not self._last_hit:
            try:
                dot = self._random_cell()
            except TimeoutError:
                # Первую ячейку по которой ещё не стреляли
                dot = self.get_first_free_cell()
        else:
            # Если попали - берем 4 соседние клетки
            # И выбираем случайную
            self.captured_dots = self._generation_cell()
            if self.captured_dots:
                while True:
                    dot = random.choice(self.captured_dots)

                    # Убираем эту точку (она записана в выстрелах)
                    self.captured_dots.pop(self.captured_dots.index(dot))

                    if not dot in self.enemy_s_board.user_move:
                        break
            else:
                # Если свободных ячеек рядом нет - сбрасываем значение
                # И выбираем случайную клетку
                self._last_hit = None
                try:
                    dot = self._random_cell()
                except TimeoutError:
                    # Первую ячейку по которой ещё не стреляли
                    dot = self.get_first_free_cell()

        # Если попали - меняем значение последнего успешного выстрела
        if self.enemy_s_board.board[dot.x][dot.y].__contains__(chr(9632)):
            self._last_hit = dot # Обновляем клетку выстрела

        print(f'Ход AI (строка, столбец): {dot.x} {dot.y}')
        return dot.x, dot.y
