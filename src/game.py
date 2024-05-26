import random
from src.dot import Dot
from src.ship import Ship
from src.board import Board
from src.players.ai import AI
from src.players.player import User
from exceptions.exceptions import *


class Game:
    """
    Основная логика игры
    """
    def __init__(self):
        self.user = User() # Игрок-пользователь
        self.ai = AI() # Игрок-компьютер
        self.current_player = 'user'  # Чей ход (user|ai)

        # Формируем доски
        self.user.own_board = self.random_board()
        self.ai.own_board = self.random_board(hid=True)

        # Добавлем cсылки на доски противника
        self.user.enemy_s_board = self.ai.own_board
        self.ai.enemy_s_board = self.user.own_board

    def start(self):
        """
        Метод запуска игры
        :return:
        """
        self._greet()
        self.loop()

    def random_board(self, hid: bool = False):
        """
        Метод генерирует случайную доску.
        (в бесконечном цикле пытаемся поставить корабль в случайную доску,
         пока наша попытка не окажется успешной).
         Расставляются сначала длинные корабли, а потом короткие.
         Если было сделано много неудачных попыток установить корабль, значит доска неудачная.
         Удаляем все корабли и пытаемся поставить ВСЕ заново.
        :return:
        """
        while True:
            game_board = Board(hid)

            # Идем по списку кораблей (от большего к меньшему)
            #  1 корабль на 3 клетки, 2 корабля на 2 клетки, 4 корабля на 1 клетку
            for ship_lenght in [_v['ship_lenght'] for _v in [{'ship_lenght': 3,
                                                              'ship_count': 1},
                                                             {'ship_lenght': 2,
                                                              'ship_count': 2},
                                                             {'ship_lenght': 1,
                                                              'ship_count': 4}] for _x in range(_v['ship_count'])]:
                # Флаг, удалось поставить корабль или нет
                ship_sailed = False

                # по ТЗ, каждый корабль пытаемся установить 1000 раз
                for _i in range(1000):
                    try:
                        # Генерируем корабль
                        ship = Ship(line_ship=random.choice(['horizontal', 'vertical']),
                                    head_dot_ship=Dot(random.randint(0, 5), random.randint(0, 5)),
                                    ship_length=ship_lenght)

                        # Если точки корабля выходят за границу - пропускаем его
                        if [True for dot in ship.ship_dots() if game_board.out(dot)].__len__() != 0:
                            continue

                        # Если точки корабля пересекаются с уже имеющимеся кораблями - пропускаем его
                        if [True for dot in ship.ship_dots() if dot in game_board.dots_ships].__len__() != 0:
                            continue

                        # Если никого нет, ставим корабль на доску
                        game_board.add_ship(ship)
                        ship_sailed = True
                        break
                    except:
                        # Ничего не предпринимаем
                        pass

                if not ship_sailed:
                    break

            # Если все корабли поставлены - возвращаем карту
            if game_board.ships.__len__() == 7:
                break

        return game_board

    def _greet(self):
        """
        Метод приветствия пользователя и краткое описание как вводить значения
        :return: True
        """
        print('*' * 30)
        print('ИГРА МОРСКОЙ БОЙ')
        print('*' * 30)
        print('Приветствую вас!')
        print('Вы стреляете по доске противника. AI, ваш противник, по вашей.\n')
        print('Пример ввода')
        print('Необходимо вводить индексы строк и столбцов через пробел'
              '\nот 0 до 5 включительно:')
        print('\t"Куда стреляем (строка, столбец)?: 2 5"')
        print('\t"Куда стреляем (строка, столбец)?: 5 3"\n')
        print('Удачи!\n')
        print("СТАРТ ИГРЫ!\n")

        return True

    def loop(self):
        """
        Метод с игровым циклом
        :return:
        """
        self.print_board(user_board=self.user.own_board.current_game_board(),
                         ai_board=self.ai.own_board.current_game_board())

        while True:
            try:
                if self.current_player == 'user':
                    if self.user.move().repeat_move:
                        self.current_player = 'user'
                    else:
                        self.current_player = 'ai'
                if self.current_player == 'ai':
                    if self.ai.move().repeat_move:
                        self.current_player = 'ai'
                    else:
                        self.current_player = 'user'

                self.print_board(user_board=self.user.own_board.current_game_board(),
                                 ai_board=self.ai.own_board.current_game_board())

            except (BoardOutException, RepeatShotException) as e:
                print(e.message)
            except Exception as e:
                # Ошибки, которые не предусмотрели
                raise e
            else:
                # Проверяем, есть ли выйгрыш
                if self._finish():
                    break

        self.ai.own_board.hid = False
        self.print_board(user_board=self.user.own_board.current_game_board(),
                         ai_board=self.ai.own_board.current_game_board(),
                         finish=True)
        print('\nИГРА ОКОНЧЕНА!')

    def _finish(self):
        """
        Метод проверяет, выиграл ли кто-то или нет
        :return:
            True - выигрыш есть
            False - игра продолжается
        """
        if self.user.own_board.col_life_ships == 0:
            print('\nВы проиграли :(\nВ следующий раз точно повезет ;)')
            return True
        elif self.ai.own_board.col_life_ships == 0:
            print('\nВы выиграли!')
            return True
        return False

    def print_board(self, user_board: list, ai_board: list, finish: bool = False):
        """
        Метод печатает текущий результат игры
        Формат:

        Доска противника                Ваша доска
          | 0 | 1 | 2 | 3 | 4 | 5 |       | 0 | 1 | 2 | 3 | 4 | 5 |
        1 | О | О | О | О | О | О |     1 | О | О | О | О | О | О |
        2 | О | О | О | О | О | О |     2 | О | О | О | О | О | О |
        3 | О | О | О | О | О | О |     3 | О | О | О | О | О | О |
        4 | О | О | О | О | О | О |     4 | О | О | О | О | О | О |
        5 | О | О | О | О | О | О |     5 | О | О | О | О | О | О |
        6 | О | О | О | О | О | О |     6 | О | О | О | О | О | О |

        :return:
        """
        st_map = ['\nДоска противника                   Ваша доска']
        for a, u in zip(ai_board, user_board):
            st_map.append(f'{"".join(a)}       {"".join(u)}')

        if finish:
            print('\n'.join(st_map).replace('X', chr(9632)))
        else:
            print('\n'.join(st_map) + '\n')
        return True
