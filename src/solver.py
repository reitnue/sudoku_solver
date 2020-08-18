import sys
import json
import heapq
import random as rand
import copy
import src.sudoku as sudoku
from src.time_utils import Timer

'''
heuristics
'''
def cellwise(game, test=False):
    game = copy.deepcopy(game)
    if test: print('cellwise')
    solves = []
    count = 0
    while True:
        if test: print('--------{}--------'.format(count))
        count += 1
        change = False
        for i in range(9):
            for j in range(9):
                if game['board'][i, j] == 0:
                    if len(sudoku.valid_numbers(game, i, j)) == 1:
                        game = sudoku.fill_number(game, i, j, sudoku.valid_numbers(game, i, j)[0])
                        solves.append((i, j))
                        change = True
        if test: print(game)
        # print('-----------------')
        if not change:
            break
    return game, solves

def numberwise(game, test=False):
    game = copy.deepcopy(game)
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
                    pos = sudoku.valid_positions(game, number, index, axis=ax)
                    if len(pos) == 1:
                        game = sudoku.fill_number(game, pos[0][0], pos[0][1], number)
                        solves.append((pos[0][0], pos[0][1]))
                        change = True
        # squares
        for square in range(9):
            for number in range(1, 10):
                pos = sudoku.valid_positions_square(game, number, square)
                if len(pos) == 1:
                    game = sudoku.fill_number(game, pos[0][0], pos[0][1], number)
                    solves.append((pos[0][0], pos[0][1]))
                    change = True
        if test: print(game)
        if not change:
            break
    return game, solves


def aggregate_pure_solver(game, heuristics):
    '''
    function to aggregate pure heuristics
    heuristics: list of heuristic solver fxns
    game: game
    returns: game, solves (standard heuristic return form)
    '''
    game = copy.deepcopy(game)
    solves = []
    while True:
        curr_solves = []
        for heuristic in heuristics:
            game, new_solves = heuristic(game)
            curr_solves += new_solves
        if len(curr_solves) == 0:
            break
        solves += curr_solves
    return game, solves


def backtracking(game, test=False):
    game = copy.deepcopy(game) 
    if sudoku.is_completed(game):
        return True, game 
    for row in range(9):
        for col in range(9):
            if game['board'][row, col] == 0:
                for num in range(1, 10):
                    if num not in sudoku.valid_numbers(game, row, col):
                        continue
                    game = sudoku.fill_number(game, row, col, num)
                    game['guesses'] += 1
                    result, game = backtracking(game)
                    if not result: # did not work -> backtrack
                        # remove number
                        game = sudoku.remove_number(game, row, col)
                    else:
                        return True, game 
                if game['board'][row, col] == 0:
                    return False, game 


def priority_backtracking_heap(game, random=False, test=False):
    game = copy.deepcopy(game)
    if sudoku.is_completed(game):
        return True, game
    pq = []
    for row in range(9):
        for col in range(9):
            if game['board'][row, col] == 0:
                weight = rand.random()/2 if random else 0
                heapq.heappush(pq, (len(sudoku.valid_numbers(game, row, col))+weight, row, col))

    priority, row, col = heapq.heappop(pq)
    # print(priority)
    for num in sudoku.valid_numbers(game, row, col):
        sudoku.fill_number(game, row, col, num)
        game['guesses'] += 1
        done, game = priority_backtracking_heap(game)
        if not done: # did not work -> backtrack
            # remove number
            sudoku.remove_number(game, row, col)
        else:
            return True, game
    if game['board'][row, col] == 0:
        return False, game


'''
cellwise -> numberwise (fastest)
'''
def human_first_backtracking(game, humans, test=False):
    game = copy.deepcopy(game)
    while True:
        change = False
        for human in humans:
            game, solves = human(game, test=test)
            if len(solves) > 0:
                change = True
        if not change:
            break
    return backtracking(game)


'''
backtrack with human methods
1. backtrack method one -> 
keep track of which cells were filled in remove then for backtrack
2. keep this information in game board ->
keep a tuple (#, level) for each level/depth of the backtracking
'''
def human_mixed_backtracking(game, heuristic, test=False):
    game = copy.deepcopy(game)
    # heuristic
    game, solved = heuristic(game, test=test)
    if sudoku.is_completed(game):
        return True, game
    # guess -> backtracking
    for row in range(9):
        for col in range(9):
            if game['board'][row, col] == 0:
                for num in range(1, 10):
                    if num not in sudoku.valid_numbers(game, row, col):
                        continue
                    game = sudoku.fill_number(game, row, col, num)
                    game['guesses'] += 1
                    done, game = human_mixed_backtracking(game, heuristic, test=test)
                    if not done:
                        # remove past fill ins
                        for x, y in solved:
                            game = sudoku.remove_number(game, x, y)
                        game = sudoku.remove_number(game, row, col)
                    else:
                        return True, game
                if game['board'][row, col] == 0:
                    for x, y in solved:
                        game = sudoku.remove_number(game, x, y)
                    return False, game # impossible


def priority_valid_nums(game):
    pq = []
    for row in range(9):
        for col in range(9):
            if game['board'][row, col] == 0:
                p = len(sudoku.valid_numbers(game, row, col))
                for num in sudoku.valid_numbers(game, row, col):
                    noise = rand.random()
                    heapq.heappush(pq, (p+noise, num, row, col))
    while len(pq) > 0:
        yield heapq.heappop(pq)


def priority_number_count(game):
    '''
    assigns priority based on how many of each number is left
    '''
    game_number_count = sudoku.number_count(game)
    pq = []
    for row in range(9):
        for col in range(9):
            if game['board'][row, col] == 0:
                for num in sudoku.valid_numbers(game, row, col):
                    noise = rand.random()
                    p = game_number_count.get(num, 9) + noise
                    heapq.heappush(pq, (p, num, row, col))

    while len(pq) > 0:
        yield heapq.heappop(pq)


def pr_valid_nums(game, num, row, col):
    return len(sudoku.valid_numbers(game, row, col))


def pr_number_count(game, num, row, col):
    return sudoku.number_count(game).get(num, 9)


def priority_func(game, priorities, weights=None):
    if weights == None:
        weights = len(priorities) * [1]
    assert len(weights) == len(priorities)
    pq = []
    for row in range(9):
        for col in range(9):
            if game['board'][row, col] == 0:
                for num in sudoku.valid_numbers(game, row, col):
                    noise = rand.random()
                    p = sum([pr(game, num, row, col)*wt for pr, wt in zip(priorities, weights)]) + noise
                    heapq.heappush(pq, (p, num, row, col))

    while len(pq) > 0:
        yield heapq.heappop(pq)

def mixed_heuristic_priority_backtracking(game, heuristic, priority, test=False):
    game = copy.deepcopy(game)
    # heuristic
    guesses = 0
    game, solved = heuristic(game)
    if sudoku.is_completed(game):
        return True, game
    
    for priority, num, row, col in priority(game):
        game = sudoku.fill_number(game, row, col, num)
        game['guesses'] += 1
        done, game = human_mixed_priority_backtracking_heap(game, heuristic, test=test)
        if not done:
            # remove past fill ins
            for x, y in solved:
                game = sudoku.remove_number(game, x, y)
            game = sudoku.remove_number(game, row, col)
        else:
            return True, game

    if game['board'][row, col] == 0: # for backtracking...
        for x, y in solved:
            game = sudoku.remove_number(game, x, y)
        return False, game


def human_mixed_priority_backtracking_heap(game, heuristic, test=False):
    game = copy.deepcopy(game)
    # heuristic
    guesses = 0
    game, solved = heuristic(game)
    if sudoku.is_completed(game):
        return True, game
    
    # begin priority
    pq = []
    for row in range(9):
        for col in range(9):
            if game['board'][row, col] == 0:
                heapq.heappush(pq, (len(sudoku.valid_numbers(game, row, col)), row, col))
    
    priority, row, col = heapq.heappop(pq)
    
    # guessing
    for num in sudoku.valid_numbers(game, row, col):
        game = sudoku.fill_number(game, row, col, num)
        game['guesses'] += 1
        done, game = human_mixed_priority_backtracking_heap(game, heuristic, test=test)
        if not done:
            # remove past fill ins
            for x, y in solved:
                game = sudoku.remove_number(game, x, y)
            game = sudoku.remove_number(game, row, col)
        else:
            return True, game

    if game['board'][row, col] == 0: # for backtracking...
        for x, y in solved:
            game = sudoku.remove_number(game, x, y)
        return False, game


if __name__ == '__main__':
    # test1
    with open('tests/easy_tests.json', 'r') as test_file:
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
        temp = Sudoku(tests[0])
        # cellwise(temp)
        # print(temp)
        num_empty = temp.number_empty()
        temp_timer.start()
        print(temp)
        done, guesses = random_priority_backtracking_manual(temp, test=False)
        print(guesses)
        print(temp)
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