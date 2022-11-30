import pytest

import kalaha
from kalaha import Board, BoardInitException


def test_board_init():
    b = Board(n_stones_per_hole=4, n_player_holes=6)
    assert b.n_stones_per_hole == 4
    assert b.n_player_holes == 6
    Board(1, 2)
    Board(100, 1000)

def test_board_init_raises_on_incorrect_holes():
    with pytest.raises(BoardInitException):
        Board(-1, 1)

def test_board_init_raises_on_zero_holes():
    with pytest.raises(BoardInitException):
        Board(1, 0)

def test_board_init_raises_on_unsupported_n_players():
    with pytest.raises(BoardInitException):
        Board(1, 1, n_players=1)
    with pytest.raises(BoardInitException):
        Board(1, 1, n_players=0)

def test_board_player_hole_numbers():
    assert kalaha._player_hole_numbers(2,1) == [0,2]
    assert kalaha._player_hole_numbers(2,2) == [0,3]
    assert kalaha._player_hole_numbers(3,1) == [0,2,4]
    assert kalaha._player_hole_numbers(3,2) == [0,3,6]

def test_board_setup():
    b = Board(n_stones_per_hole=4, n_player_holes=1)
    assert b.holes[0].n_stones == 0  # player A
    assert b.holes[1].n_stones == 4  # hole
    assert b.holes[2].n_stones == 0  # Player B
    assert b.holes[3].n_stones == 4  # hole

def test_board_player0_1_move_1_stone_1_hole():
    b = Board(n_stones_per_hole=1, n_player_holes=1)
    b.move(player_hole_id=0, start_hole_id=3)
    assert b.holes[0].n_stones == 1  # player A
    assert b.holes[1].n_stones == 1  # hole
    assert b.holes[2].n_stones == 0  # Player B
    assert b.holes[3].n_stones == 0  # hole

def test_board_player2_1_move_1_stone_1_hole():
    b = Board(n_stones_per_hole=1, n_player_holes=1)
    b.move(player_hole_id=2, start_hole_id=1)
    assert b.holes[0].n_stones == 0  # player A
    assert b.holes[1].n_stones == 0  # hole
    assert b.holes[2].n_stones == 1  # Player B
    assert b.holes[3].n_stones == 1  # hole

def test_board_two_player_game_2_stones_2_holes():
    b = Board(n_stones_per_hole=2, n_player_holes=2)
    # Player (hole) 0
    # Move 1
    is_turn_complete = b.move(player_hole_id=0, start_hole_id=4)
    assert is_turn_complete == kalaha.Turn.is_not_over
    assert b.holes[0].n_stones == 1  # player A
    assert b.holes[1].n_stones == 2  # hole
    assert b.holes[2].n_stones == 2  # hole
    assert b.holes[3].n_stones == 0  # Player B
    assert b.holes[4].n_stones == 0  # hole
    assert b.holes[5].n_stones == 3  # hole
    # Move 2
    is_turn_complete = b.move(player_hole_id=0, start_hole_id=5)
    assert is_turn_complete == kalaha.Turn.is_not_over
    assert b.holes[0].n_stones == 3  # player A
    assert b.holes[1].n_stones == 3  # hole
    assert b.holes[2].n_stones == 0  # hole
    assert b.holes[3].n_stones == 0  # Player B
    assert b.holes[4].n_stones == 1  # hole
    assert b.holes[5].n_stones == 1  # hole
    # Move 3
    is_turn_complete = b.move(player_hole_id=0, start_hole_id=5)
    assert is_turn_complete == kalaha.Turn.is_not_over
    assert b.holes[0].n_stones == 4  # player A
    assert b.holes[1].n_stones == 3  # hole
    assert b.holes[2].n_stones == 0  # hole
    assert b.holes[3].n_stones == 0  # Player B
    assert b.holes[4].n_stones == 1  # hole
    assert b.holes[5].n_stones == 0  # hole
    # Move 4
    is_turn_complete = b.move(player_hole_id=0, start_hole_id=1)
    assert is_turn_complete == kalaha.Turn.is_over
    assert b.holes[0].n_stones == 4  # player A
    assert b.holes[1].n_stones == 0  # hole
    assert b.holes[2].n_stones == 1  # hole
    assert b.holes[3].n_stones == 0  # Player B
    assert b.holes[4].n_stones == 2  # hole
    assert b.holes[5].n_stones == 1  # hole
    # Player (hole) 3
    # Move 1
    is_turn_complete = b.move(player_hole_id=3, start_hole_id=2)
    assert is_turn_complete == kalaha.Turn.is_not_over
    assert b.holes[0].n_stones == 4  # player A
    assert b.holes[1].n_stones == 0  # hole
    assert b.holes[2].n_stones == 0  # hole
    assert b.holes[3].n_stones == 1  # Player B
    assert b.holes[4].n_stones == 2  # hole
    assert b.holes[5].n_stones == 1  # hole
    # Move 2
    is_turn_complete = b.move(player_hole_id=3, start_hole_id=4)
    assert is_turn_complete == kalaha.Turn.is_over
    assert b.holes[0].n_stones == 4  # player A
    assert b.holes[1].n_stones == 1  # hole
    assert b.holes[2].n_stones == 0  # hole
    assert b.holes[3].n_stones == 1  # Player B
    assert b.holes[4].n_stones == 0  # hole
    assert b.holes[5].n_stones == 2  # hole