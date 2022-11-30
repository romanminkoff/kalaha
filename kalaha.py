from colorama import Fore, Style
from enum import Enum
import itertools


class Turn(Enum):
    is_over = True
    is_not_over = False

class HoleException(Exception):
    pass

class Hole:
    def __init__(self, id):
        self.id = id
        self.n_stones = 0
        self.next_hole = None
        self.player_hole_id = None

    def _is_other_players_hole(self, player_hole_id):
        if self.player_hole_id not in [None, player_hole_id]:
            return True

    def _put_stones(self, player_hole_id, stones_to_put):
        self.n_stones += 1
        stones_to_put -= 1

        if stones_to_put == 0:
            if self.player_hole_id == player_hole_id:
                return Turn.is_not_over
            elif self.n_stones == 1:
                return Turn.is_over
            else:
                stones_to_put = self.n_stones
                self.n_stones = 0
        return self.next_hole.move(player_hole_id, stones_to_put)

    def start_move(self, player_hole_id):
        if self.n_stones == 0:
            raise HoleException(f'No stones in hole #{self.id}')
        all_stones = self.n_stones
        self.n_stones = 0
        return self.next_hole.move(player_hole_id, all_stones)
    
    def move(self, player_hole_id, stones_to_put):
        if self._is_other_players_hole(player_hole_id):
            return self.next_hole.move(player_hole_id, stones_to_put)
        else:
            return self._put_stones(player_hole_id, stones_to_put)


def _player_hole_numbers(n_players, n_player_holes):
        a = [0]
        n_holes = n_players*n_player_holes + n_players
        for i in range(1, n_holes):
            if not i%(n_player_holes+1):
                a.append(i)
        return a    

class BoardInitException(Exception):
    pass

class BoardTurnException(Exception):
    pass

class Board:
    def __init__(self, n_stones_per_hole, n_player_holes, n_players=2):
        self.n_stones_per_hole = n_stones_per_hole
        self.n_player_holes = n_player_holes
        self.n_players = n_players
        self.holes = []
        self.player_hole_ids = []
        self._setup_board()

    def _validate_params(self):
        if self.n_stones_per_hole < 0 or self.n_player_holes < 1:
            raise BoardInitException('Number of stones & holes should be >0')
        if self.n_players < 2:
            raise BoardInitException('Incorrect number of players')

    def _create_holes(self):
        n_holes = self.n_player_holes * self.n_players + self.n_players
        for i in range(n_holes):
            self.holes.append(Hole(id=i))

    def _connect_holes(self):
        for i in range(len(self.holes)-1):
            self.holes[i].next_hole = self.holes[i+1]
        self.holes[-1].next_hole = self.holes[0]

    def _init_holes(self):
        for h in self.holes:
            if not h.next_hole:
                raise BoardInitException(f'Hole {h.id} has no next hole')
            if h.id in self.player_hole_ids:
                h.player_hole_id = h.id
            else:
                h.n_stones = self.n_stones_per_hole

    def _setup_board(self):
        self._validate_params()
        self.player_hole_ids = _player_hole_numbers(self.n_players,
            self.n_player_holes)
        self._create_holes()
        self._connect_holes()
        self._init_holes()

    def move(self, player_hole_id, start_hole_id):
        if start_hole_id in self.player_hole_ids:
            raise BoardTurnException('Cannot start from the players hole')
        return self.holes[start_hole_id].start_move(player_hole_id)


def print_col(txt, fore_color=None, end=''):
    if fore_color:
        print(fore_color, end='')
    print(txt, end=end)
    if fore_color:
        print(Style.RESET_ALL, end='')

def print_holes(board:Board):
    for h in board.holes:
        print_col(f'{h.id:4}', Fore.LIGHTBLACK_EX, end='')
    print('')
    for h in board.holes:
        color = Fore.GREEN if h.player_hole_id is not None else None
        print_col(f'{h.n_stones:4}', color, end='')
    print('')

class ConsoleGame:
    def __init__(self):
        self.board = None

    def _init_board(self):
        n_players = int(input("Number of players: "))
        n_player_holes = int(input("Number of player holes: "))
        n_stones_per_hole = int(input("Number of stones per hole: "))
        self.board = Board(n_stones_per_hole, n_player_holes, n_players)

    def _is_game_over(self):
        for h in self.board.holes:
            if h.player_hole_id is None and h.n_stones > 0:
                return False
        return True

    def _game_loop(self):
        player_holes = itertools.cycle(self.board.player_hole_ids)
        for players_hole in player_holes:
            turn = Turn.is_not_over
            while(turn == Turn.is_not_over):
                print(f"Player with hole #{players_hole} is moving.")
                hole = int(input("Which hole id to start with? "))
                try:
                    turn = self.board.move(players_hole, hole)
                    print_holes(self.board)
                    if self._is_game_over():
                        return
                except HoleException:
                    print(f"Try a different hole ({hole} is empty)")
                except BoardTurnException:
                    print(f"Cannot start from players hole {hole}.")

    def _print_board_layout(self):
        print("\n----- Board layout -----")
        print_holes(self.board)

    def _print_game_results(self):
        print("Game is over")
        for h in self.board.holes:
            if h.player_hole_id is not None:
                print(f"\tPlayer {h.player_hole_id}: {h.n_stones}")

    def new_game(self):
        self._init_board()
        self._print_board_layout()
        self._game_loop()
        self._print_game_results()