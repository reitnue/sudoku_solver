import sys
import json
import numpy as np

INDICES = [0, 3, 6]
NUMBERS = [x for x in range(1, 10)]
# NUMBERS_SET = set(NUMBERS)

def compute_square(row, col):
    return ((row // 3) * 3) + (col // 3)

def compute_row_col(square):
    row = 3 * (square // 3)
    col = 3 * (square % 3)
    return row, col
'''
row, col are both zero-indexed
assumes all boards are valid
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

    def number_empty(self):
        num_empty = 0
        for row in range(9):
            for col in range(9):
                if not self.is_filled(row, col):
                    num_empty += 1
        return num_empty
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
        if number not in self.valid_numbers(row, col) or self.board[row, col] != 0:
            return -1
        self.board[row, col] = number
        self.rows[row].add(number)
        self.cols[col].add(number)
        self.squares[compute_square(row, col)].add(number)
        return 0

    def remove_number(self, row, col):
        num = self.board[row, col]
        self.board[row, col] = 0
        if num in self.rows[row]: self.rows[row].remove(num)
        if num in self.cols[col]: self.cols[col].remove(num)
        if num in self.squares[compute_square(row, col)]: self.squares[compute_square(row, col)].remove(num)
        return 0

    def is_filled(self, row, col):
        return self.board[row, col] != 0

    def is_completed(self):
        result = True
        result &= all(map((lambda x: x == 9), map(len, self.rows)))
        result &= all(map((lambda x: x == 9), map(len, self.cols)))
        result &= all(map((lambda x: x == 9), map(len, self.squares)))
        return result

    # axis 0 -> row
    # axis 1 -> col
    # returns possible positions for number in specified index
    def number_check(self, number, index, axis=0):
        set_lists = self.rows if axis == 0 else self.cols
        if number in set_lists[index]:
            return [] # alreayd in the row/col
        valid_pos = []
        for jndex in range(9):
            if axis == 0:
                if not self.is_filled(index, jndex):
                    valid_pos.append((index, jndex))
            elif axis == 1:
                if not self.is_filled(jndex, index):
                    valid_pos.append((jndex, index))

        return valid_pos

    # returns possible positions for number in specified square
    def number_check_square(self, number, square):
        if number in self.squares[square]:
            return [] # alreayd in the square
        valid_pos = []
        row, col = compute_row_col(square)
        for index in range(row, row+3):
            for jndex in range(col, col+3):
                if not self.is_filled(index, jndex):
                    if number in self.valid_numbers(index, jndex): # O(n) technically, but the list is constant sized - 9
                        valid_pos.append((index, jndex))
        
        return valid_pos

if __name__ == '__main__':
    with open('../test/test03.json', 'r') as test1_file:
        test1 = json.loads(test1_file.read())
    temp = Sudoku(test1)
    print(temp)
    for _ in range(2):
        for ax in range(2):
            for index in range(9):
                for number in range(1, 10):
                    pos = temp.number_check(number, index, axis=ax)
                    if len(pos) == 1:
                        temp.fill_number(pos[0][0], pos[0][1], number)
        for square in range(9):
            for number in range(1, 10):
                pos = temp.number_check_square(number, square)
                if len(pos) == 1:
                    temp.fill_number(pos[0][0], pos[0][1], number)

        print('-----------------')
        print(temp)
    print(temp.is_completed())
    # with open('../test/test01_solved.json', 'w') as test1_solved:
    #     test1_solved.write(json.dumps(temp.board.tolist(), indent=2))
