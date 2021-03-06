import os
import sys
import json
import requests
import statistics as stat
from scipy import stats as sci_stats

from sudoku import Sudoku
import solver
from time_utils import Timer

TEST_FILE = "../test/{}_tests.json"
DIFFICULTIES = ['easy', 'medium', 'hard', 'random']

def tester(solvers, verbose=False, difficulty='easy', trials=1):
    boards = get_test_boards(difficulty=difficulty)
    
    timers = [Timer(f.__name__) for f in solvers]
    for timer, solver in zip(timers, solvers):
        solver_guesses = []
        for board in boards:
            for _ in range(trials):
                game = Sudoku(board)
                empty = game.number_empty()
                timer.start()
                done, guesses = solver(game)
                timer.stop(verbose=verbose)
                if not done:
                    print('unsolved')
                else:
                    solver_guesses.append(guesses / empty)
        print("{:50}: Avg Number of Percentage Guess: {:.5f}".format(solver.__name__, stat.mean(solver_guesses)))
    for timer in timers:
        timer.summary()

    return 0

def t_tester(solver_a, solver_b, verbose=False, difficulty='easy', trials=10):
    board = get_sugoku_board(difficulty)
    
    solvers = [solver_a, solver_b]
    timers = [Timer(f.__name__) for f in solvers]
    
    for timer, solver in zip(timers, solvers):
        solver_guesses = []
        for _ in range(trials):
            game = Sudoku(board)
            empty = game.number_empty()
            
            timer.start()
            done, guesses = solver(game)
            timer.stop(verbose=verbose)
            
            if not done:
                print('unsolved')
            else:
                solver_guesses.append(guesses / empty)
        print("{:50}: Avg Number of Percentage Guess: {:.5f}".format(solver.__name__, stat.mean(solver_guesses)))
    
    for timer in timers:
        timer.summary()

    print(sci_stats.ttest_rel(timers[0].times, timers[1].times))

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
    solvers = []
    # solvers.append(solver.numberwise_backtracking)
    # solvers.append(solver.cellwise_backtracking)

    # solvers.append(solver.numberwise_cellwise_backtracking)
    # solvers.append(solver.cellwise_numberwise_backtracking)
    # solvers.append(solver.numberwise_mixed_backtracking)
    # solvers.append(solver.cellwise_mixed_backtracking)
    # solvers.append(solver.numberwise_mixed_priority_backtracking_heap)
    solvers.append(solver.cellwise_mixed_priority_backtracking_heap)

    # solvers.append(solver.numberwise_mixed_priority_backtracking_manual)
    solvers.append(solver.cellwise_mixed_priority_backtracking_manual)
    solvers.append(solver.not_random_cellwise_mixed_priority_backtracking_manual)
    solvers.append(solver.random_cellwise_mixed_priority_backtracking_manual)

    # solvers.append(solver.priority_backtracking_heap)
    solvers.append(solver.priority_backtracking_manual)
    solvers.append(solver.random_priority_backtracking_manual)
    # solvers.append(solver.backtracking)
    # solvers.append(solver.random_backtracking)

    # print(sys.argv[1])
    # if sys.argv[1] not in DIFFICULTIES:
    #     sys.stderr.write("invalid option\n")
    # tester(solvers, difficulty=sys.argv[1], verbose=False, trials=int(sys.argv[2]))

    t_tester(solver.cellwise_mixed_priority_backtracking_manual, solver.random_priority_backtracking_manual)
    t_tester(solver.random_priority_backtracking_manual, solver.cellwise_mixed_priority_backtracking_manual)