import sudoku_logic


def test_create_empty_board_has_expected_dimensions():
    board = sudoku_logic.create_empty_board()

    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert all(cell == sudoku_logic.EMPTY for row in board for cell in row)


def test_generate_puzzle_returns_puzzle_and_solution():
    puzzle, solution = sudoku_logic.generate_puzzle(35)

    assert len(puzzle) == sudoku_logic.SIZE
    assert len(solution) == sudoku_logic.SIZE
    assert puzzle != solution
    assert all(isinstance(cell, int) for row in puzzle for cell in row)
    assert all(isinstance(cell, int) for row in solution for cell in row)


def test_is_safe_detects_conflicts_in_rows_columns_and_boxes():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 1
    board[0][1] = 1

    assert sudoku_logic.is_safe(board, 0, 1, 1) is False

    board = sudoku_logic.create_empty_board()
    board[0][0] = 1
    board[1][0] = 1

    assert sudoku_logic.is_safe(board, 1, 0, 1) is False

    board = sudoku_logic.create_empty_board()
    board[0][0] = 1
    board[1][1] = 1

    assert sudoku_logic.is_safe(board, 1, 1, 1) is False
