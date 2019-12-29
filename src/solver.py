import sys
import json
from sudoku import Sudoku
from time_utils import Timer

def cellwise(game, test=False):
    if test: print('cellwise')
    solves = []
    count = 0
    while True:
        if test: print('--------{}--------'.format(count))
        count += 1
        change = False
        for i in range(9):
            for j in range(9):
                if not game.is_filled(i, j):
                    if len(game.valid_numbers(i, j)) == 1:
                        if game.fill_number(i, j, game.valid_numbers(i, j)[0]) == 0:
                            solves.append((i, j))
                            change = True
        if test: print(game)
        # print('-----------------')
        if not change:
            break
    return solves

def numberwise(game, test=False):
    if test: print('numberwise')
    count = 0
    solves = []
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
                        if game.fill_number(pos[0][0], pos[0][1], number) == 0:
                            solves.append((pos[0][0], pos[0][1]))
                            change = True
        # squares
        for square in range(9):
            for number in range(1, 10):
                pos = game.number_check_square(number, square)
                if len(pos) == 1:
                    if game.fill_number(pos[0][0], pos[0][1], number) == 0:
                        solves.append((pos[0][0], pos[0][1]))
                        change = True
        if test: print(game)
        if not change:
            break
    return solves

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

# order matters
'''
cellwise -> numberwise (fastest)
'''
def human_first_backtracking(game, humans, test=False):
    while True:
        change = False
        for human in humans:
            change |= len(human(game, test=test)) > 0
        if not change:
            break
    return backtracking(game)

def numberwise_backtracking(game, test=False):
    return human_first_backtracking(game, [numberwise])

def numberwise_cellwise_backtracking(game, test=False):
    return human_first_backtracking(game, [numberwise, cellwise])

def cellwise_backtracking(game, test=False):
    return human_first_backtracking(game, [cellwise])

def cellwise_numberwise_backtracking(game, test=False):
    return human_first_backtracking(game, [cellwise, numberwise])

'''
backtrack with human methods
1. backtrack method one -> 
keep track of which cells were filled in remove then for backtrack
2. keep this information in game board ->
keep a tuple (#, level) for each level/depth of the backtracking
'''
def human_mixed_backtracking_1(game, heuristic, test=False):
    # heuristic
    solved = heuristic(game, test=test)
    if game.is_completed():
        return True
    for row in range(9):
        for col in range(9):
            if not game.is_filled(row, col):
                for num in range(1, 10):
                    if game.fill_number(row, col, num) == 0:
                        if not human_mixed_backtracking_1(game, heuristic, test=test):
                            # remove past fill ins
                            for x, y in solved:
                                game.remove_number(x, y)
                            game.remove_number(row, col)
                        else:
                            return True
                if not game.is_filled(row, col):
                    for x, y in solved:
                        game.remove_number(x, y)
                    return False # impossible

def cellwise_mixed_backtracking(game, test=False):
    return human_mixed_backtracking_1(game, cellwise)

def numberwise_mixed_backtracking(game, test=False):
    return human_mixed_backtracking_1(game, numberwise)


def priority_based_backtracking(game, test=False):
    pass

if __name__ == '__main__':
    # test1
    with open('../test/easy_tests.json', 'r') as test_file:
        tests = json.loads(test_file.read())
    
    temp_timer = Timer('temp')
    for _ in range(50):
        temp = Sudoku(tests[0])
        numberwise(temp)        
        print(temp)
        temp_timer.start()
        # print(backtracking(temp))
        print(human_mixed_backtracking_1(temp, numberwise, test=True))
        temp_timer.stop()
        break
    # temp_timer.summary()