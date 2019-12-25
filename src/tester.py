import sys
import json
import requests

from sudoku import Sudoku
from solver import cellwise

def tester_number(number, solver):
    board = get_test_board(number)
    # solved = get_solved_board(number)
    game = Sudoku(board)
    solver(game)
    return game.is_completed()

def tester_board(board, solver):
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

'''
level: easy, medium, hard, random
'''
def get_sugoku_board(level):
    req = requests.get("https://sugoku.herokuapp.com/board?difficulty={}".format(level))
    return json.loads(req.text)['board']

if __name__ == '__main__':
    for num in range(1, 4):
        print(num, tester_number(num, cellwise))
    
    num_test = 10
    count = 0
    for _ in range(num_test):
        temp_board = get_sugoku_board('easy')
        print(temp_board)
        if tester_board(temp_board, cellwise):
            count += 1
    print(count / num_test)