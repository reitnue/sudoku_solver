import sys

class Sudoku:
    def __init__(self, board=None):
        self.board = board # 2d array
        self.squares = [set() for _ in range(9)]
        self.rows = [set() for _ in range(9)]
        self.cols = [set() for _ in range(9)]

