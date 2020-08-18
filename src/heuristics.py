import copy
import src.sudoku as sudoku

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
