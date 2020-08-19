import src.sudoku as sudoku

def pr_valid_nums(game, num, row, col):
    return len(sudoku.valid_numbers(game, row, col))


def pr_number_count(game, num, row, col):
    return sudoku.number_count(game).get(num, 9)


def destructive_approx(game, num, row, col):
    '''
    counts the number of empty "neighboring" cells
    '''
    priority = 0
    priority += 9 - len(game['rows'][row])
    priority += 9 - len(game['cols'][col])
    priority += 9 - len(game['squares'][sudoku.compute_square(row, col)])
    return priority


def destructive(game, num, row, col):
    '''
    assigns priority as the number of options of "neighboring" cells
    removed once placed
    '''
    priority = 0
    for tmp_col in range(9):
        priority += 1 if num in sudoku.valid_numbers(game, row, tmp_col) else 0
    for tmp_row in range(9):
        priority += 1 if num in sudoku.valid_numbers(game, tmp_row, col) else 0
    sq_row, sq_col = sudoku.compute_row_col(sudoku.compute_square(row, col))
    for i in range(3):
        for j in range(3):
            priority += 1 if num in sudoku.valid_numbers(game, sq_row+i, sq_col+j) else 0
    return priority - 3


def destructive_ratio(game, num, row, col):
    priority = 0
    for tmp_col in range(9):
        if tmp_col == col:
            continue
        valids = sudoku.valid_numbers(game, row, tmp_col)
        priority += 1/len(valids) if num in valids else 0
    for tmp_row in range(9):
        if tmp_row == row:
            continue
        valids = sudoku.valid_numbers(game, tmp_row, col)
        priority += 1/len(valids) if num in valids else 0
    sq_row, sq_col = sudoku.compute_row_col(sudoku.compute_square(row, col))
    for i in range(3):
        for j in range(3):
            if sq_row+i == row and sq_col+j == col:
                continue
            valids = sudoku.valid_numbers(game, sq_row+i, sq_col+j)
            priority += 1/len(valids) if num in valids else 0
    return priority

