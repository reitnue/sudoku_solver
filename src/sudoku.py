'''
provides functional-styled functions to act on sudoku boards
and related data structures
'''
from typing import List, Dict
import numpy as np

INDICES = [0, 3, 6]

'''
row and col are 0-indexed
square refers to the group of 9
'''

def compute_square(row: int, col: int) -> int:
    '''
    Given (row, col) returns the corresponding
    square number on the sudoku board
    '''
    return ((row // 3) * 3) + (col // 3)

def compute_row_col(square: int) -> (int, int):
    '''
    Given square number on the sudoku board
    Returns the (row, col) pair
    '''
    row = 3 * (square // 3)
    col = 3 * (square % 3)
    return row, col


def create_sudoku(board: List[List[int]]) -> Dict:
    result = {}
    result['guesses'] = 0
    result['removes'] = 0
    result['solves'] = 0
    result['board'] = np.array(board) # 2d array
    result['rows'] = [set(filter((lambda x: x != 0), row)) for row in result['board']]
    result['cols'] = [set(filter((lambda x: x != 0), col)) for col in result['board'].T]
    result['squares'] = [set(filter(
        lambda x: x != 0,
        result['board'][i:i+3, j:j+3].flatten()
    )) for i in INDICES for j in INDICES]
    return result


def print_board(sudoku: dict) -> str:
    return '\n'.join([' '.join(map(str, x)) for x in sudoku['board']])


def empty_cell_count(sudoku: dict) -> int:
    return len([x for x in sudoku['board'].flatten() if x == 0])


def valid_numbers(sudoku: dict, row: int, col: int) -> int:
    '''
    given row, col and board
    returns sorted list of valid numbers in the cell
        - based on current state of row, col, square
    '''
    if sudoku['board'][row, col] != 0:
        return [sudoku['board'][row, col]]

    result = set(range(1, 10))
    result -= sudoku['rows'][row]
    result -= sudoku['cols'][col]
    result -= sudoku['squares'][compute_square(row, col)]
    return sorted(list(result))


def fill_number(sudoku: dict, row: int, col: int, number: int) -> dict:
    sudoku = sudoku.copy()
    if number not in valid_numbers(sudoku, row, col) or \
        sudoku['board'][row, col] != 0:
        # invalid fill or already filled
        return sudoku

    sudoku['board'][row, col] = number
    sudoku['rows'][row].add(number)
    sudoku['cols'][col].add(number)
    sudoku['squares'][compute_square(row, col)].add(number)
    sudoku['solves'] += 1
    return sudoku


def remove_number(sudoku: dict, row: int, col: int) -> dict:
    sudoku = sudoku.copy()
    num = sudoku['board'][row, col]
    sudoku['removes'] += 1
    sudoku['solves'] -= 1
    sudoku['board'][row, col] = 0
    sudoku['rows'][row].discard(num)
    sudoku['cols'][col].discard(num)
    sudoku['squares'][compute_square(row, col)].discard(num)
    return sudoku


def is_completed(sudoku: dict):
    result = True
    result &= all(map(lambda x: x == 9, map(len, sudoku['rows'])))
    result &= all(map(lambda x: x == 9, map(len, sudoku['cols'])))
    result &= all(map(lambda x: x == 9, map(len, sudoku['squares'])))
    return result


def valid_positions(sudoku: dict, number: int, index: int, axis: int) -> List:
    sudoku = sudoku.copy()
    set_lists = sudoku['rows'] if axis == 0 else sudoku['cols']
    if number in set_lists[index]:
        # already in row or col
        return []
    valid = []
    for jndex in range(9):
        if axis == 0:
            row, col = index, jndex
        elif axis == 1:
            row, col = jndex, index
        if sudoku['board'][row, col] == 0 and number in valid_numbers(sudoku, row, col):
            valid.append((row, col))
    return valid


def valid_positions_square(sudoku: dict, number: int, square: int) -> List:
    if number in sudoku['squares'][square]:
        # already in square
        return []
    valid = []
    row, col = compute_row_col(square)
    for index in range(row, row+3):
        for jndex in range(col, col+3):
            if sudoku['board'][index, jndex] == 0:
                if number in valid_numbers(sudoku, index, jndex):
                    valid.append((index, jndex))
    return valid


def number_count(sudoku: dict) -> dict:
    number_count = {}
    for x in map(int, sudoku['board'].flatten()):
        if x not in number_count:
            number_count[x] = 0
        number_count[x] += 1
    return number_count