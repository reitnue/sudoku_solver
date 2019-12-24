import sys
import json
import numpy as np

INDICES = [0, 3, 6]

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


if __name__ == '__main__':
    with open('../test/test1.json', 'r') as test1_file:
        test1 = json.loads(test1_file.read())
    temp = Sudoku(test1)
    print(temp)
    print(temp.rows)
    print(temp.cols)
    print(temp.squares)