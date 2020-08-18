# pylint: disable=redefined-outer-name

import pytest
from src import sudoku
from src import solver
from src import heuristics
from src import priorities
from src import utils

easy_board = [
    [0, 5, 8, 0, 0, 0, 0, 0, 0],
    [1, 2, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 9, 0, 0, 8, 0, 0, 7],
    [0, 0, 0, 0, 6, 0, 0, 0, 0],
    [0, 7, 0, 0, 0, 9, 0, 0, 0],
    [8, 0, 0, 0, 2, 0, 3, 0, 0],
    [5, 3, 0, 8, 4, 6, 9, 7, 0], 
    [6, 0, 0, 9, 0, 2, 5, 3, 0],
    [0, 4, 2, 5, 7, 3, 8, 6, 1],
]


@pytest.fixture
def board():
    board = easy_board[:]
    return board


@pytest.fixture
def game(board):
    return sudoku.create_sudoku(board)


def test_aggregate_pure_solver_numberwise(board):
    '''
    tests the aggregate pure solver in a basic way:
        does at least as well as number/cell wise
    '''
    game_a = sudoku.create_sudoku(board)
    game_b = sudoku.create_sudoku(board)
    game_c = sudoku.create_sudoku(board)

    new_game_a, a_solves = utils.aggregate_pure_solver(
                            game_a, 
                            [
                                heuristics.numberwise,
                                heuristics.cellwise
                            ])
    end_game_a, a_next_solves = heuristics.numberwise(new_game_a)
    assert len(a_next_solves) == 0 # no more solves
    
    new_game_b, b_solves = heuristics.numberwise(game_b)
    assert len(a_solves) >= len(b_solves) # does at least as good