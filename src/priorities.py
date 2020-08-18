import src.sudoku as sudoku

def pr_valid_nums(game, num, row, col):
    return len(sudoku.valid_numbers(game, row, col))


def pr_number_count(game, num, row, col):
    return sudoku.number_count(game).get(num, 9)