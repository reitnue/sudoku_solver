import sys
import json
from sudoku import Sudoku
from solver import cellwise

def tester(number, solver):
    board = get_test_board(number)
    # solved = get_solved_board(number)
    game = Sudoku(board)
    solver(game)
    return game.is_completed()

def get_test_board(number):
    with open('../test/test{:02}.json'.format(number), 'r') as test1_file:
        test1 = json.loads(test1_file.read())
    return test1

def get_solved_board(number):
    with open('../test/test{:02}_solved.json'.format(number), 'r') as test1_file:
        test1 = json.loads(test1_file.read())
    return test1

if __name__ == '__main__':
    for num in range(1, 4):
        print(num, tester(num, cellwise))
    # test1
    # with open('../test/test01.json', 'r') as test1_file:
    #     test1 = json.loads(test1_file.read())

    # temp = Sudoku(test1)
