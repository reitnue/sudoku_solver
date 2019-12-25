import sys
import json
import numpy as np

INDICES = [0, 3, 6]
NUMBERS = [x for x in range(1, 10)]
# NUMBERS_SET = set(NUMBERS)

def compute_square(row, col):
    return ((row // 3) * 3) + (col // 3)

'''
row, col are both zero-indexed
'''
class Sudoku:
    def __init__(self, board=None):
        self.board   = np.array(board) # 2d array
        self.rows    = [set() for _ in range(9)]
        self.cols    = [set() for _ in range(9)]
        self.squares = [set() for _ in range(9)]

        if len(self.board):
            self.rows    = [set(filter((lambda x: x != 0), row)) for row in self.board]
            self.cols    = [set(filter((lambda x: x != 0), col)) for col in self.board.T]
            self.squares = [set(filter((lambda x: x != 0), self.board[i:i+3, j:j+3].flatten())) for i in INDICES for j in INDICES]

    def __str__(self):    
        return '\n'.join([' '.join(map(str, x)) for x in self.board])

    # return a list of valid numbers for a square (row, col)
    def valid_numbers(self, row, col):
        if self.board[row, col] != 0:
            return [self.board[row, col]]
        result = set(NUMBERS)
        result -= self.rows[row]
        result -= self.cols[col]
        result -= self.squares[compute_square(row, col)]
        return sorted(list(result))

    def fill_number(self, row, col, number):
        if number not in self.valid_numbers(row, col):
            return -1
        self.board[row, col] = number
        self.rows[row].add(number)
        self.cols[col].add(number)
        self.squares[compute_square(row, col)].add(number)
        return 0

    def is_filled(self, row, col):
        return self.board[row, col] != 0

    def is_completed(self):
        result = True
        result &= all(map((lambda x: x == 9), map(len, self.rows)))
        result &= all(map((lambda x: x == 9), map(len, self.cols)))
        result &= all(map((lambda x: x == 9), map(len, self.squares)))
        return result

if __name__ == '__main__':
    with open('../test/test03.json', 'r') as test1_file:
        test1 = json.loads(test1_file.read())
    temp = Sudoku(test1)
    print(temp)
    

    # print('-----------------')
    count = 1
    while True:
        print('--------{}--------'.format(count))
        count += 1
        change = False
        for i in range(9):
            for j in range(9):
                if not temp.is_filled(i, j):
                    if len(temp.valid_numbers(i, j)) == 1:
                        temp.fill_number(i, j, temp.valid_numbers(i, j)[0])
                        change = True
        print(temp)
        # print('-----------------')
        if not change:
            break
    print(temp.is_completed())
    # with open('../test/test01_solved.json', 'w') as test1_solved:
    #     test1_solved.write(json.dumps(temp.board.tolist(), indent=2))
