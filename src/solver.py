import sys
import json
import heapq
import random

from sudoku import Sudoku
from time_utils import Timer

'''
heuristics
'''
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
    guesses = 0
    if game.is_completed():
        return True, guesses
    for row in range(9):
        for col in range(9):
            if not game.is_filled(row, col):
                for num in range(1, 10):
                    if game.fill_number(row, col, num) == 0:
                        guesses += 1
                        result, other_guesses = backtracking(game)
                        guesses += other_guesses
                        if not result: # did not work -> backtrack
                            # remove number
                            game.remove_number(row, col)
                        else:
                            return True, guesses
                if not game.is_filled(row, col): return False, guesses

def random_backtracking(game, test=False):
    guesses = 0
    if test:
        print('-' * 17)
        print(game)
    if game.is_completed():
        return True, guesses
    open_squares = []
    for open_row in range(9):
        for open_col in range(9):
            if not game.is_filled(open_row, open_col):
                open_squares.append((open_row, open_col))
    random.shuffle(open_squares)
    # print(open_squares)
    nums = list(range(1, 10))
    random.shuffle(nums)
    for row, col in open_squares:
        if test: print(row, col)
        for num in nums:
            if game.fill_number(row, col, num) == 0:
                guesses += 1
                result, other_guesses = random_backtracking(game, test=test)
                guesses += other_guesses
                if not result: # did not work -> backtrack
                    # remove number
                    game.remove_number(row, col)
                else:
                    return True, guesses
        if not game.is_filled(row, col): return False, guesses

def priority_backtracking_heap(game, test=False):
    guesses = 0
    if game.is_completed():
        return True, guesses
    pq = []
    for row in range(9):
        for col in range(9):
            if not game.is_filled(row, col):
                heapq.heappush(pq, (len(game.valid_numbers(row, col)), row, col))

    priority, row, col = heapq.heappop(pq)
    # print(priority)
    for num in game.valid_numbers(row, col):
        if game.fill_number(row, col, num) == 0:
            done, other_guesses = priority_backtracking_heap(game)
            guesses += other_guesses + 1
            if not done: # did not work -> backtrack
                # remove number
                game.remove_number(row, col)
            else:
                return True, guesses
    if not game.is_filled(row, col): return False, guesses

def priority_backtracking_manual(game, test=False):
    guesses = 0
    if game.is_completed():
        return True, guesses

    curr_row, curr_col, options = -1, -1, list(range(9))
    for row in range(9):
        for col in range(9):
            if not game.is_filled(row, col):
                possible = game.valid_numbers(row, col)
                if len(possible) < len(options):
                    curr_row, curr_col, options = row, col, possible

    # print(priority)
    # print(len(options))
    for num in options:
        if game.fill_number(curr_row, curr_col, num) == 0:
            done, other_guesses = priority_backtracking_manual(game)
            guesses += other_guesses + 1
            if not done: # did not work -> backtrack
                # remove number
                game.remove_number(curr_row, curr_col)
                # print(game)
            else:
                return True, guesses
    if not game.is_filled(curr_row, curr_col): 
        # print(curr_row, curr_col)
        return False, guesses

def random_priority_backtracking_manual(game, test=False, randomized=True):
    guesses = 0
    if game.is_completed():
        return True, guesses

    option_dict = {}
    curr_row, curr_col, options = -1, -1, list(range(9))
    for row in range(9):
        for col in range(9):
            if not game.is_filled(row, col):
                possible = game.valid_numbers(row, col)
                if len(possible) not in option_dict:
                    option_dict[len(possible)] = []
                option_dict[len(possible)].append((row, col, possible))

                if len(possible) < len(options):
                    curr_row, curr_col, options = row, col, possible

    # print(priority)
    # print(len(options))
    if randomized:
        curr_row, curr_col, options = random.choice(option_dict[sorted(option_dict.keys())[0]])
    for num in options:
        if game.fill_number(curr_row, curr_col, num) == 0:
            done, other_guesses = random_priority_backtracking_manual(game)
            guesses += other_guesses + 1
            if not done: # did not work -> backtrack
                # remove number
                game.remove_number(curr_row, curr_col)
                # print(game)
            else:
                return True, guesses
    if not game.is_filled(curr_row, curr_col): 
        # print(curr_row, curr_col)
        return False, guesses

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
def human_mixed_backtracking(game, heuristic, test=False):
    guesses = 0
    # heuristic
    solved = heuristic(game, test=test)
    if game.is_completed():
        return True, guesses
    for row in range(9):
        for col in range(9):
            if not game.is_filled(row, col):
                for num in range(1, 10):
                    if game.fill_number(row, col, num) == 0:
                        done, other_guesses = human_mixed_backtracking(game, heuristic, test=test)
                        guesses += other_guesses + 1
                        if not done:
                            # remove past fill ins
                            for x, y in solved:
                                game.remove_number(x, y)
                            game.remove_number(row, col)
                        else:
                            return True, guesses
                if not game.is_filled(row, col):
                    for x, y in solved:
                        game.remove_number(x, y)
                    return False, guesses # impossible

def cellwise_mixed_backtracking(game, test=False):
    return human_mixed_backtracking(game, cellwise)

def numberwise_mixed_backtracking(game, test=False):
    return human_mixed_backtracking(game, numberwise)

def human_mixed_priority_backtracking_heap(game, heuristic, test=False):
    # heuristic
    guesses = 0
    solved = heuristic(game, test=test)
    if game.is_completed():
        return True, guesses
    pq = []
    for row in range(9):
        for col in range(9):
            if not game.is_filled(row, col):
                heapq.heappush(pq, (len(game.valid_numbers(row, col)), row, col))
    
    priority, row, col = heapq.heappop(pq)
    # print(priority)
    for num in game.valid_numbers(row, col):
        if game.fill_number(row, col, num) == 0:
            done, other_guesses = human_mixed_priority_backtracking_heap(game, heuristic, test=test)
            guesses += other_guesses + 1
            if not done:
                # remove past fill ins
                for x, y in solved:
                    game.remove_number(x, y)
                game.remove_number(row, col)
            else:
                return True, guesses
    if not game.is_filled(row, col):
        for x, y in solved:
            game.remove_number(x, y)
        return False, guesses # impossible

def cellwise_mixed_priority_backtracking_heap(game, test=False):
    return human_mixed_priority_backtracking_heap(game, cellwise)

def numberwise_mixed_priority_backtracking_heap(game, test=False):
    return human_mixed_priority_backtracking_heap(game, numberwise)

def human_mixed_priority_backtracking_manual(game, heuristic, test=False):
    # heuristic
    guesses = 0
    solved = heuristic(game, test=test)
    if game.is_completed():
        return True, guesses
    
    curr_row, curr_col, options = -1, -1, list(range(9))
    for row in range(9):
        for col in range(9):
            if not game.is_filled(row, col):
                possible = game.valid_numbers(row, col)
                if len(possible) < len(options):
                    curr_row, curr_col, options = row, col, possible

    # print(priority)
    # print(len(options))
    for num in options:# print(priority)
        if game.fill_number(curr_row, curr_col, num) == 0:
            done, other_guesses = human_mixed_priority_backtracking_manual(game, heuristic, test=test)
            guesses += other_guesses + 1
            if not done:
                # remove past fill ins
                for x, y in solved:
                    game.remove_number(x, y)
                game.remove_number(curr_row, curr_col)
            else:
                return True, guesses
    if not game.is_filled(curr_row, curr_col):
        for x, y in solved:
            game.remove_number(x, y)
        return False, guesses # impossible

def cellwise_mixed_priority_backtracking_manual(game, test=False):
    return human_mixed_priority_backtracking_manual(game, cellwise)

def numberwise_mixed_priority_backtracking_manual(game, test=False):
    return human_mixed_priority_backtracking_manual(game, numberwise)

def random_human_mixed_priority_backtracking_manual(game, heuristic, test=False, randomized=True):
    # heuristic
    guesses = 0
    solved = heuristic(game, test=test)
    if game.is_completed():
        return True, guesses
    
    option_dict = {}
    curr_row, curr_col, options = -1, -1, list(range(9))
    for row in range(9):
        for col in range(9):
            if not game.is_filled(row, col):
                possible = game.valid_numbers(row, col)
                if len(possible) not in option_dict:
                    option_dict[len(possible)] = []
                option_dict[len(possible)].append((row, col, possible))

                if len(possible) < len(options):
                    curr_row, curr_col, options = row, col, possible

    # print(priority)
    # print(len(options))
    if randomized:
        curr_row, curr_col, options = random.choice(option_dict[sorted(option_dict.keys())[0]])
    for num in options:# print(priority)
        if game.fill_number(curr_row, curr_col, num) == 0:
            done, other_guesses = human_mixed_priority_backtracking_manual(game, heuristic, test=test)
            guesses += other_guesses + 1
            if not done:
                # remove past fill ins
                for x, y in solved:
                    game.remove_number(x, y)
                game.remove_number(curr_row, curr_col)
            else:
                return True, guesses
    if not game.is_filled(curr_row, curr_col):
        for x, y in solved:
            game.remove_number(x, y)
        return False, guesses # impossible

def random_cellwise_mixed_priority_backtracking_manual(game, test=False):
    return random_human_mixed_priority_backtracking_manual(game, cellwise)

# same as cellwise_mixed_priority_backtracking_manual, but with option_dict
def not_random_cellwise_mixed_priority_backtracking_manual(game, test=False):
    return random_human_mixed_priority_backtracking_manual(game, cellwise, randomized=False)

if __name__ == '__main__':
    # test1
    with open('../test/easy_tests.json', 'r') as test_file:
        tests = json.loads(test_file.read())
    
    game = [[8,0,0,5,7,4,3,1,2],
            [0,5,4,0,0,0,8,7,6],
            [0,3,0,0,0,0,4,5,9],
            [6,8,3,1,9,5,2,4,7],
            [4,0,0,3,8,2,1,6,5],
            [5,1,2,7,4,6,9,8,3],
            [0,4,0,0,0,0,5,2,1],
            [0,0,0,4,5,0,0,9,8],
            [0,0,5,0,1,0,0,3,4]]
    temp_timer = Timer('temp')

    for _ in range(10):
        temp = Sudoku(tests[2])
        # cellwise(temp)
        # print(temp)
        num_empty = temp.number_empty()
        temp_timer.start()
        print(temp)
        done, guesses = random_priority_backtracking_manual(temp, test=False)
        print(guesses)
        # print(temp)
        # print(backtracking(temp))
        # print(numberwise_backtracking(temp))
        # print(priority_backtracking_manual(temp))
        # done, guesses = human_mixed_backtracking(temp, numberwise, test=False)
        # done, guesses = human_mixed_priority_backtracking_manual(temp, numberwise, test=False)
        # print(guesses / num_empty)
        temp_timer.stop()
        # break
    #     break
    temp_timer.summary()