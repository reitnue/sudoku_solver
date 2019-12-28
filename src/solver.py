import sys
import json
from sudoku import Sudoku
from time_utils import Timer

def cellwise(game, test=False):
    if test: print('cellwise')
    count = 0
    while True:
        if test: print('--------{}--------'.format(count))
        count += 1
        change = False
        for i in range(9):
            for j in range(9):
                if not game.is_filled(i, j):
                    if len(game.valid_numbers(i, j)) == 1:
                        game.fill_number(i, j, game.valid_numbers(i, j)[0])
                        change = True
        if test: print(game)
        # print('-----------------')
        if not change:
            break
    return count > 1

def numberwise(game, test=False):
    if test: print('numberwise')
    count = 0
    while True:
        if test: print('--------{}--------'.format(count))
        count += 1
        change = False
        # rows/cols
        for ax in range(2):
            for index in range(9):
                for number in range(1, 10):
                    pos = game.number_check(number, index, axis=ax)
                    if len(pos) == 1:
                        game.fill_number(pos[0][0], pos[0][1], number)
                        change = True
        # squares
        for square in range(9):
            for number in range(1, 10):
                pos = game.number_check_square(number, square)
                if len(pos) == 1:
                    game.fill_number(pos[0][0], pos[0][1], number)
                    change = True
        if test: print(game)
        if not change:
            break
    return count > 1

def backtracking(game, test=False):
    if game.is_completed():
        return True
    for row in range(9):
        for col in range(9):
            if not game.is_filled(row, col):
                for num in range(1, 10):
                    if game.fill_number(row, col, num) == 0:
                        if not backtracking(game): # did not work -> backtrack
                            # remove number
                            game.remove_number(row, col)
                        else:
                            return True
                if not game.is_filled(row, col): return False

def human_first_backtracking(game, test=False):
    while True:
        change = False
        change |= numberwise(game, test=test)
        change |= cellwise(game, test=test)
        if not change:
            break

    return backtracking(game)


def probabilistic_backtracking(game, test=False):
    pass

if __name__ == '__main__':
    # test1
    with open('../test/easy_tests.json', 'r') as test_file:
        tests = json.loads(test_file.read())
    
    # temp = Sudoku(tests[0])
    # temp = Sudoku(tests[1])
    # print(temp)
    # print('-' * 17)
    # print(temp)
    # cellwise(temp, test=False)
    # numberwise(temp, test=False)
    # print(temp)
    # print(backtracking(temp))
    # print(temp)
    human_time = Timer('Human Time')
    backtrack_time = Timer('Backtrack Time')
    for test in tests:
        temp = Sudoku(test)
        human_time.start()
        human_first_backtracking(temp)
        human_time.stop()
        # print(temp)

        temp = Sudoku(test)
        backtrack_time.start()
        backtracking(temp)
        backtrack_time.stop()
        
        # print(temp)
        # cellwise(temp, test=False)
        # numberwise(temp, test=False)
        # backtracking(temp)
        # print(temp.is_completed())
        # break

    human_time.summary()
    backtrack_time.summary()
