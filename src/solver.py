import sys
import json
from sudoku import Sudoku

def cellwise(game, test=False):
    print('cellwise')
    count = 1
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
    return game.is_completed()

def numberwise(game, test=False):
    print('numberwise')
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


if __name__ == '__main__':
    # test1
    with open('../test/easy_tests.json', 'r') as test_file:
        tests = json.loads(test_file.read())
    
    temp = Sudoku(tests[0])
    cellwise(temp, test=True)
    temp = Sudoku(tests[0])
    numberwise(temp, test=True)


    # for test in tests:
    #     temp = Sudoku(test)
    #     cellwise(temp, test=True)
    #     numberwise(temp, test=True)

    #     break
