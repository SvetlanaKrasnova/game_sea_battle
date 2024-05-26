import random
from typing import Optional
from datetime import datetime
from .player import Player
from src.dot import Dot
from exceptions.exceptions import BoardOutException, RepeatShotException

class AI(Player):
    """
    Противник/Напарник.
    """

    def __init__(self):
        super(AI, self).__init__()
        self._last_hit: Optional[Dot] = None

    def neighbors(self, index: int):
        return [index + 1, index - 1]

    def _generation_cell(self) -> list:
        """
        Метод генерирует 4 соседние ячейки (если они не выходят за границу)
        Например:
            Точка старта 1,4
            Результат метода 1,3 1,5 0,4 2,4
        :return:
        """
        dots = [[x, y] for x, y in zip(self.neighbors(self._last_hit.x), [self._last_hit.y] * 2)]
        dots.extend([[x, y] for x, y in zip([self._last_hit.x] * 2, self.neighbors(self._last_hit.y))])

        free_dots = []

        # Формируем точки
        for _d in dots:
            try:
                _dot = Dot(_d[0], _d[1])

                # Если не выходит за границу
                if self.enemy_s_board.out(_dot):
                    raise BoardOutException()

                # Если не стреляли в клетку
                if _dot in self.enemy_s_board.user_move:
                    raise RepeatShotException()
            except:
                continue

            free_dots.append(Dot(_d[0], _d[1]))

        return free_dots

    def _random_cell(self):
        start_time = datetime.now()
        while int((datetime.now() - start_time).total_seconds()) <= 3:
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
        Метод возвращает первую свободную ячейка
        :return:
        """
        for i, l in enumerate(self.enemy_s_board.board):
            for k, j in enumerate(l):
                if self.enemy_s_board.board[i][k] == 'О':
                    return Dot(i, k)

    def ask(self):
        """
        Метод выбирает случайную свободную клетку
        :return:
        """
        # Если попадания не было - выбираем случайную клетку
        if not self._last_hit:
            try:
                dot = self._random_cell()
            except TimeoutError:
                # Первую свободную ячейку
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
                # Это, корабль из 1 клетки
                self._last_hit = None
                try:
                    dot = self._random_cell()
                except TimeoutError:
                    # Первую свободную ячейку
                    dot = self.get_first_free_cell()

        # Если попали - меняем значение последнего выстрела
        if self.enemy_s_board.board[dot.x][dot.y].__contains__(chr(9632)):
            self._last_hit = dot # Обновляем клетку выстрела

        print(f'Ход AI (строка, столбец): {dot.x} {dot.y}')
        return dot.x, dot.y
