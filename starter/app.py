from flask import Flask, render_template, jsonify, request
import sudoku_logic

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None
}


def get_clues_for_difficulty(difficulty):
    difficulty = (difficulty or '').strip().lower()
    if difficulty == 'easy':
        return 40
    if difficulty == 'hard':
        return 25
    return 35


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new')
def new_game():
    clues_param = request.args.get('clues')
    if clues_param is not None:
        clues = int(clues_param)
    else:
        clues = get_clues_for_difficulty(request.args.get('difficulty', 'medium'))
    puzzle, solution = sudoku_logic.generate_puzzle(clues)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    return jsonify({'puzzle': puzzle})


@app.route('/hint')
def get_hint():
    puzzle = CURRENT.get('puzzle')
    solution = CURRENT.get('solution')
    if puzzle is None or solution is None:
        return jsonify({'hint': None})

    for row in range(sudoku_logic.SIZE):
        for col in range(sudoku_logic.SIZE):
            if puzzle[row][col] == 0:
                puzzle[row][col] = solution[row][col]
                return jsonify({'hint': {'row': row, 'col': col, 'value': solution[row][col]}})

    return jsonify({'hint': None})


@app.route('/validate-cell', methods=['POST'])
def validate_cell():
    data = request.json
    board = data.get('board')
    row = data.get('row')
    col = data.get('col')
    value = data.get('value')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    if value == 0:
        return jsonify({'valid': True, 'incorrect': False})

    if value != solution[row][col]:
        return jsonify({'valid': False, 'incorrect': True})

    for i in range(sudoku_logic.SIZE):
        if i != col and board[row][i] == value:
            return jsonify({'valid': False, 'incorrect': True})
        if i != row and board[i][col] == value:
            return jsonify({'valid': False, 'incorrect': True})

    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if (i != row or j != col) and board[i][j] == value:
                return jsonify({'valid': False, 'incorrect': True})

    return jsonify({'valid': True, 'incorrect': False})


@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    completed = len(incorrect) == 0
    return jsonify({'incorrect': incorrect, 'completed': completed})

if __name__ == '__main__':
    app.run(debug=True)