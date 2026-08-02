import copy

import pytest

import app as app_module


@pytest.fixture
def client():
    app_module.CURRENT['puzzle'] = None
    app_module.CURRENT['solution'] = None
    app_module.app.config.update(TESTING=True)
    with app_module.app.test_client() as test_client:
        yield test_client


def test_index_route_returns_home_page(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b'Sudoku Game' in response.data


def test_new_game_route_returns_a_valid_puzzle(client):
    response = client.get('/new?clues=35')

    assert response.status_code == 200
    payload = response.get_json()

    assert 'puzzle' in payload
    puzzle = payload['puzzle']
    assert len(puzzle) == 9
    for row in puzzle:
        assert len(row) == 9
        assert all(isinstance(value, int) for value in row)

    assert app_module.CURRENT['solution'] is not None
    assert len(app_module.CURRENT['solution']) == 9


def test_new_game_route_uses_selected_difficulty(client, monkeypatch):
    captured = {}

    def fake_generate_puzzle(clues):
        captured['clues'] = clues
        return [[0] * 9 for _ in range(9)], [[1] * 9 for _ in range(9)]

    monkeypatch.setattr(app_module.sudoku_logic, 'generate_puzzle', fake_generate_puzzle)

    response = client.get('/new?difficulty=easy')

    assert response.status_code == 200
    assert captured['clues'] == 40


def test_check_route_returns_error_when_no_game_exists(client):
    response = client.post('/check', json={'board': [[0] * 9 for _ in range(9)]})

    assert response.status_code == 400
    assert response.get_json()['error'] == 'No game in progress'


def test_check_route_reports_incorrect_cells(client):
    client.get('/new?clues=35')
    solution = app_module.CURRENT['solution']
    board = copy.deepcopy(solution)
    board[0][0] = 1 if solution[0][0] != 1 else 2

    response = client.post('/check', json={'board': board})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload['incorrect'] == [[0, 0]]
