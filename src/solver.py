import sys
import json
import heapq
import random as rand
import copy
import src.sudoku as sudoku
from src.time_utils import Timer


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