import random
from .player import Player
from src.dot import Dot


class AI(Player):
    """
    Противник/Напарник.
    """

    def __init__(self):
        super(AI, self).__init__()

    def ask(self):
        """
        Метод выбирает случайную свободную клетку
        :return:
        """
        while True:
            x = random.randrange(5)
            y = random.randrange(5)

            if Dot(x, y) in self.enemy_s_board.user_move:
                print(f'АI - Такой выстрел уже был ({x} {y})')
                continue
            else:
                break

        print(f'\nХод AI (строка, столбец): {x} {y}')
        return x, y
