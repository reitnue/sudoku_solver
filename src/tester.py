import os
import sys
import json
import requests

from sudoku import Sudoku
import solver
from time_utils import Timer

TEST_FILE = "../test/{}_tests.json"
DIFFICULTIES = ['easy', 'medium', 'hard', 'random']

def tester(solvers, difficulty='easy'):
    boards = get_test_boards(difficulty=difficulty)
    
    timers = [Timer(f.__name__) for f in solvers]
    for timer, solver in zip(timers, solvers):
        for board in boards:
            game = Sudoku(board)
            timer.start()
            if not solver(game):
                print('unsolved')
            timer.stop()
    for timer in timers:
        timer.summary()

    return 0

def get_test_boards(difficulty='easy'):
    with open(TEST_FILE.format(difficulty), 'r') as test:
        return json.loads(test.read())

'''
level: easy, medium, hard, random
'''
def get_sugoku_board(level):
    req = requests.get("https://sugoku.herokuapp.com/board?difficulty={}".format(level))
    return json.loads(req.text)['board']

def generate_more_boards(num_test):
    difficulty = ['easy', 'medium', 'hard', 'random']
    for diff in difficulty:
        boards = [get_sugoku_board(diff) for _ in range(num_test)]
        if os.path.exists(TEST_FILE.format(diff)):
            with open(TEST_FILE.format(diff), 'r') as test:
                boards += json.loads(test.read())
        with open(TEST_FILE.format(diff), 'w') as test:
            test.write(json.dumps(boards))

if __name__ == '__main__':
    solvers = [solver.backtracking, solver.human_first_backtracking]
    tester(solvers, difficulty='easy')

    # generate_more_boards(20)