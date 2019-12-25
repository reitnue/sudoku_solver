import sys
import json
from sudoku import Sudoku

def cellwise(game, test=False):
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

if __name__ == '__main__':
    # test1
    with open('../test/test02.json', 'r') as test1_file:
        test1 = json.loads(test1_file.read())

    # test1 = [[0,0,0,0,0,0,0,6,4],[0,2,0,3,0,9,5,0,0],[0,8,9,0,0,7,0,2,0],[2,0,0,5,0,6,0,8,9],[0,5,6,0,0,0,2,3,0],[0,9,0,1,0,2,0,0,0],[0,0,0,0,0,5,0,0,0],[8,0,2,9,7,4,3,1,0],[0,0,0,0,0,0,8,0,0]]
    
    temp = Sudoku(test1)
    
    print(cellwise(temp))
