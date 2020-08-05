import pytest
from src import sudoku
from src import func_sudoku

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
def class_board(board):
    return sudoku.Sudoku(board)


@pytest.fixture
def func_board(board):
    return func_sudoku.create_sudoku(board)


def test_creation(class_board, func_board):
    '''
    tests creation and initialization of boards
    '''
    for key in ['board', 'rows', 'cols', 'squares']:
        a = getattr(class_board, key)
        b = func_board[key]
        if key == 'board':
            assert (a == b).all()
        else:
            assert a == b

def test_print(class_board, func_board):
    '''
    tests return string of boards
    '''
    assert str(class_board) == func_sudoku.print_board(func_board)


def test_number_empty(class_board, func_board):
    '''
    tests number empty counts correctly
    '''
    assert class_board.number_empty == func_sudoku.empty_cell_count(func_board)


def test_valid_numbers(class_board, func_board):
    '''
    tests valid numbers in any givne row, col
    '''
    for row in sudoku.NUMBERS:
        for col in sudoku.NUMBERS:
            assert class_board.valid_numbers(row, col) == func_sudoku.valid_numbers(func_board)


# stateful methods
def test_valid_fill_number(class_board, func_board):
    '''
    tests both methods fill the board and update necessary fields
    '''
    assert False

def test_invalid_fill_number(class_board, func_board):
    '''
    tests both methods fail to insert and stops
    '''
    assert False


def test_valid_remove_number(class_board, func_board):
    '''
    tests both methods removes number and updates fields accordingly
    '''
    assert False


def test_invalid_remove_number(class_board, func_board):
    '''
    tests both methods fails to removes number and does nothing
    - not implemented in class
    '''
    assert True 


def test_is_completed(class_board, func_board):
    '''
    tests both functions to notify completion match
    '''
    assert False


def test_valid_positions_axis(class_board, func_board):
    '''
    tests both fxns for valid positions of a number in a specificed index, axis
    '''
    assert False


def test_valid_positions_square(class_board, func_board):
    '''
    tests fxns for valid possitions, (row, col), for number in specified square
    '''
    assert False