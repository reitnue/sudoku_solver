# pylint: disable=redefined-outer-name

import pytest
from src import func_sudoku
from src import func_solver

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
def func_game(board):
    return func_sudoku.create_sudoku(board)


def test_aggregate_pure_solver_numberwise(board):
    '''
    tests the aggregate pure solver in a basic way:
        does at least as well as number/cell wise
    '''
    game_a = func_sudoku.create_sudoku(board)
    game_b = func_sudoku.create_sudoku(board)
    game_c = func_sudoku.create_sudoku(board)

    new_game_a, a_solves = func_solver.aggregate_pure_solver(
                            game_a, 
                            [
                                func_solver.numberwise,
                                func_solver.cellwise
                            ])
    end_game_a, a_next_solves = func_solver.numberwise(new_game_a)
    assert len(a_next_solves) == 0 # no more solves
    
    new_game_b, b_solves = func_solver.numberwise(game_b)
    assert len(a_solves) >= len(b_solves) # does at least as good