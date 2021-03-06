# pylint: disable=redefined-outer-name

import pytest
from src import sudoku
from src import func_sudoku
from src import solver, func_solver

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

completed_board = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [4, 5, 6, 7, 8, 9, 1, 2, 3],
    [7, 8, 9, 1, 2, 3, 4, 5, 6],
    [2, 3, 4, 5, 6, 7, 8, 9, 1],
    [5, 6, 7, 8, 9, 1, 2, 3, 4],
    [8, 9, 1, 2, 3, 4, 5, 6, 7],
    [3, 4, 5, 6, 7, 8, 9, 1, 2],
    [6, 7, 8, 9, 1, 2, 3, 4, 5],
    [9, 1, 2, 3, 4, 5, 6, 7, 8],
]

@pytest.fixture
def board():
    board = easy_board[:]
    return board


@pytest.fixture
def completed_board():
    return completed_board[:]


@pytest.fixture
def class_board(board):
    return sudoku.Sudoku(board)


@pytest.fixture
def func_board(board):
    return func_sudoku.create_sudoku(board)


@pytest.fixture
def completed_class_board(completed_board):
    return sudoku.Sudoku(completed_board)


@pytest.fixture
def completed_func_board(completed_board):
    return func_sudoku.create_sudoku(completed_board)


def test_creation(class_board, func_board):
    '''
    tests creation and initialization of boards
    '''
    assert is_equal_boards(class_board, func_board)

def is_equal_boards(board_class, board_func):
    for key in ['board', 'rows', 'cols', 'squares']:
        a = getattr(board_class, key)
        b = board_func[key]
        if key == 'board':
            return (a == b).all()
        else:
            return a == b

def test_print(class_board, func_board):
    '''
    tests return string of boards
    '''
    assert str(class_board) == func_sudoku.print_board(func_board)


def test_number_empty(class_board, func_board):
    '''
    tests number empty counts correctly
    '''
    assert class_board.number_empty() == func_sudoku.empty_cell_count(func_board)


def test_valid_numbers(class_board, func_board):
    '''
    tests valid numbers in any givne row, col
    '''
    for row in range(9):
        for col in range(9):
            assert class_board.valid_numbers(row, col) == \
                func_sudoku.valid_numbers(func_board, row, col)


# stateful methods
def test_valid_fill_number(class_board, func_board):
    '''
    tests both methods fill the board and update necessary fields
    '''
    class_board.fill_number(0, 0, 7)
    next_board = func_sudoku.fill_number(func_board, 0, 0, 7)
    assert is_equal_boards(class_board, next_board)


def test_invalid_fill_number(class_board, func_board):
    '''
    tests both methods fail to insert and stops
    '''
    number = 5
    class_board.fill_number(0, 0, number)
    next_board = func_sudoku.fill_number(func_board, 0, 0, number)
    assert is_equal_boards(class_board, next_board)


def test_valid_remove_number(class_board, func_board):
    '''
    tests both methods removes number and updates fields accordingly
    '''
    class_board.remove_number(0, 1)
    next_board = func_sudoku.remove_number(func_board, 0, 1)
    assert is_equal_boards(class_board, next_board)


@pytest.mark.skip('not implemented')
def test_invalid_remove_number(class_board, func_board):
    '''
    tests both methods fails to removes number and does nothing
    - not implemented in class
    '''
    class_board.remove_number(0, 0)
    next_board = func_sudoku.remove_number(func_board, 0, 0)
    is_equal_boards(class_board, next_board)


def test_is_completed(class_board, func_board):
    '''
    tests both functions to notify completion match
    '''
    assert class_board.is_completed() == func_sudoku.is_completed(func_board)


def test_valid_positions_axis(class_board, func_board):
    '''
    tests both fxns for valid positions of a number in a specificed index, axis
    '''
    for index in range(9):
        for num in range(1, 10):
            for ax in [0, 1]:
                assert sorted(class_board.number_check(num, index, axis=ax)) == \
                    sorted(func_sudoku.valid_positions(func_board, num, index, axis=ax))



def test_valid_positions_square(class_board, func_board):
    '''
    tests fxns for valid possitions, (row, col), for number in specified square
    '''
    for square in range(9):
        for num in range(1, 10):
            assert sorted(class_board.number_check_square(num, square)) == \
                sorted(func_sudoku.valid_positions_square(func_board, num, square))


def test_cellwise(class_board, func_board):
    '''
    tests cellwise heuristic
    '''
    next_board, solves = func_solver.cellwise(func_board)
    assert sorted(solver.cellwise(class_board)) == \
        sorted(solves)
    assert is_equal_boards(class_board, next_board)


def test_numberwise(class_board, func_board):
    '''
    tests numberwise heuristic
    '''
    next_board, solves = func_solver.numberwise(func_board)
    assert sorted(solver.numberwise(class_board)) == \
        sorted(solves)
    assert is_equal_boards(class_board, next_board)


def test_backtracking(class_board, func_board):
    '''
    tests backtracking solver
    '''
    _, guesses = solver.backtracking(class_board)
    is_complete, func_board = func_solver.backtracking(func_board)
    assert is_complete
    assert is_equal_boards(class_board, func_board)
    assert guesses == func_board['guesses']


@pytest.mark.skip("bad solver method")
def test_random_backtracking(class_board, func_board):
    '''
    tests random backtracking solver
    '''
    _, guesses = solver.random_backtracking(class_board)
    is_complete, func_board = func_solver.random_backtracking(func_board)
    assert is_complete
    assert is_equal_boards(class_board, func_board)


def test_priority_backtracking_heap(class_board, func_board):
    _, guesses = solver.priority_backtracking_heap(class_board)
    is_complete, func_board = func_solver.priority_backtracking_heap(func_board)
    assert is_complete
    assert is_equal_boards(class_board, func_board)
    assert guesses == func_board['guesses']


def test_human_first_backtracking(class_board, func_board):
    solver.human_first_backtracking(class_board, [solver.numberwise])
    is_complete, func_board = func_solver.human_first_backtracking(func_board, [func_solver.numberwise])
    assert is_complete


def test_human_mixed_backtracking(class_board, func_board):
    solver.human_mixed_backtracking(class_board, solver.numberwise)
    is_complete, func_board = func_solver.human_mixed_backtracking(func_board, func_solver.numberwise)
    assert is_complete


def test_human_mixed_priority_backtracking(class_board, func_board):
    solver.human_mixed_priority_backtracking_heap(class_board, solver.numberwise)
    is_complete, func_board = func_solver.human_mixed_priority_backtracking_heap(func_board, func_solver.numberwise)
    assert is_complete