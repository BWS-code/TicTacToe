from random import choice
from time import sleep

class TicTacToe:

    def __init__(self, game_size):
        self.game_size = game_size
        self.game_sizes = [3,4]
        self.ends_of_game = ['X wins', 'O wins', 'Draw']
        self.valid_players = {'user', 'easy', 'medium', 'hard'}

        self.header_len = '-' * (game_size * 3 - self.game_sizes.index(game_size))
        self.game_progress = [' ' for x in range(pow(game_size, 2))]
        self.game_is_ON = 1  # game is ON
        self.player = 0  # 1st player in submitted list
        self.winnerX = ['X' for x in range(self.game_size)]
        self.winnerO = ['O' for x in range(self.game_size)]
        self.marks = ['X','O']

    def get_board(self):
        print(self.header_len)
        for i in range(0, pow(self.game_size, 2), self.game_size):
            print('|', *self.game_progress[i: i + self.game_size], '|')
        print(self.header_len)

    def entry_check_OK_user(self):
        while 555 < 666:
            coords = input('Enter the coordinates (col row): ').split(' ')
            self.col, self.row = coords if len(coords) == 2 else ('FiveFiveFive', 'SixSixSix')
            if not self.col.isnumeric() or not self.row.isnumeric():
                print('You should enter numbers!')
            elif not all([x in [str(x) for x in range(1, self.game_size + 1)] for x in [self.col, self.row]]):
                print(f'Coordinates should be from 1 to {self.game_size}!')
            elif self.game_progress[(self.game_size - int(self.row)) * self.game_size + (int(self.col) - 1)] != ' ':
                print('This cell is occupied! Choose another one!')
            else:
                return True
                break

    def entry_check_OK_AI(self, AI_lvl, virt_mark):
        empties = [i for i, x in enumerate(self.game_progress) if x == ' ']
        if AI_lvl == 'easy':
            self.move_cell = int(choice(empties))
            return True
        if AI_lvl == 'medium':
            if self.game_progress.count('X') >= self.game_size - 1:
                virt_empties = [i for i in empties]

                while len(virt_empties) > 0:
                    self.move_cell = int(choice(virt_empties))
                    self.game_progress[self.move_cell] = virt_mark
                    self.check_rules()

                    virt_winner = self.winnerX if virt_mark == "X" else self.winnerO
                    if virt_winner in self.rules:
                        self.game_progress[self.move_cell] = ' '
                        print('self win found ->', self.move_cell)  #debug
                        return True
                        break
                    self.game_progress[self.move_cell] = ' '
                    virt_empties.remove(self.move_cell)
                    # here ends self win check
                else:
                    # here starts oppo win check
                    virt_mark = 'X' if virt_mark == 'O' else 'O'
                    virt_empties = [i for i in empties]

                    while len(virt_empties) > 0:
                        self.move_cell = int(choice(virt_empties))
                        self.game_progress[self.move_cell] = virt_mark
                        self.check_rules()

                        virt_winner = self.winnerX if virt_mark == "X" else self.winnerO
                        if virt_winner in self.rules:
                            self.game_progress[self.move_cell] = ' '
                            print('oppo win found ->', self.move_cell)  #debug
                            return True
                            break
                        self.game_progress[self.move_cell] = ' '
                        virt_empties.remove(self.move_cell)

                    else:
                        print('no wins both found so far')  #debug
                        self.move_cell = int(choice(empties))
                        return True
            else:
                self.move_cell = int(choice(empties))
                return True

        if AI_lvl == 'hard':
            self.winn = virt_mark
            self.oppo = 'O' if virt_mark == 'X' else 'X'
            self.move_cell = self.mini_max(virt_mark)[1]
            return True

    def winning(self, virt_mark):
        self.check_rules()
        if self.game_size * [virt_mark] in self.rules:
            return True
        return False

    def mini_max(self, virt_mark):

        if self.winning(self.oppo):
            return -10, None
        elif self.winning(self.winn):
            return 10, None
        elif self.game_progress.count(' ') == 0:
            return 0, None

        virt_moves = []
        empties = [i for i, x in enumerate(self.game_progress) if x == ' ']
        for i in empties:
            self.game_progress[i] = virt_mark
            res = self.mini_max(self.oppo) if virt_mark == self.winn else self.mini_max(self.winn)
            virt_move = (res[0], i)
            self.game_progress[i] = ' '

            virt_moves.append(virt_move)

        return min(virt_moves) if virt_mark == self.oppo else max(virt_moves)


    def make_move(self, who, mark):
        if who == 'user':
            if self.entry_check_OK_user():
                move_cell = (self.game_size - int(self.row)) * self.game_size + (int(self.col) - 1)
                self.game_progress[move_cell] = mark
        else:
            if self.entry_check_OK_AI(self.players_list[self.player], self.marks[self.player]):  # submitting AI lvl & mark
                print(f'Making move level {self.players_list[self.player]}')
                sleep(1.5)
                self.game_progress[self.move_cell] = mark

    def check_rules(self):

        self.rules = [self.game_progress[:self.game_size],
                      self.game_progress[self.game_size: self.game_size * 2],
                      self.game_progress[self.game_size * 2: self.game_size * 3],

                      self.game_progress[self.game_size * 3: self.game_size * 4],


                      self.game_progress[::self.game_size],
                      self.game_progress[1::self.game_size],
                      self.game_progress[2::self.game_size],

                      self.game_progress[3::self.game_size],


                      self.game_progress[::self.game_size + 1],
                      self.game_progress[self.game_size - 1:
                                         pow(self.game_size, 2) - self.game_size + 1:
                                         self.game_size - 1]

                      ]

    def check_state(self):
        if self.winnerX in self.rules:
            print(self.ends_of_game[0])
            self.game_is_ON = 0
        elif self.winnerO in self.rules:
            print(self.ends_of_game[1])
            self.game_is_ON = 0
        elif ' ' not in self.game_progress:
            print(self.ends_of_game[2])
            self.game_is_ON = 0
        else:
            pass

    def get_players(self):
        while 555 < 666:
            inits = input('Input command: ').split()
            init_list = [i for i in inits]
            if len(init_list) == 3 and \
                    init_list[0] == 'start' and \
                    init_list[1] in self.valid_players and \
                    init_list[2] in self.valid_players:
                self.players_list = init_list[1:]
                print(self.players_list)
                break
            else:
                print('Bad parameters!')

    def main_driver(self):
        self.get_players()
        self.get_board()
        while self.game_is_ON:
            self.make_move \
                (self.players_list[self.player],  # submitting who    0 or 1
                 self.marks[self.player])         # submitting mark   X or O
            self.get_board()
            self.check_rules()
            self.check_state()
            self.player = 1 if self.player == 0 else 0

    def run(self):
        if self.game_size in self.game_sizes:
            self.main_driver()
        else:
            print('select allowed game size')

BWS_game = TicTacToe(3)
BWS_game.run()