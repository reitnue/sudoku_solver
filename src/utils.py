import copy
import src.sudoku as sudoku
import random as rand
import heapq

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


'''
cellwise -> numberwise (fastest time)
'''

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