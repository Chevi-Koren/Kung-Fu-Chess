import pathlib, time

from GraphicsFactory import MockImgFactory
from Game import Game
from Command import Command
from GameFactory import create_game

import numpy as np

import pytest

PIECES_ROOT = pathlib.Path(__file__).parent.parent / "pieces"
BOARD_CSV = PIECES_ROOT / "board.csv"


# ---------------------------------------------------------------------------
#                          GAMEPLAY TESTS
# ---------------------------------------------------------------------------




def test_gameplay_pawn_move_and_capture():
    game = create_game("../pieces", MockImgFactory())
    game._time_factor = 1000000000
    game._update_cell2piece_map()
    pw = game.pos[(6, 0)][0]
    pb = game.pos[(1, 1)][0]
    game.user_input_queue.put(Command(game.game_time_ms(), pw.id, "move", [(6, 0), (4, 0)]))
    game.user_input_queue.put(Command(game.game_time_ms(), pb.id, "move", [(1, 1), (3, 1)]))
    time.sleep(0.5)
    game.run(num_iterations=100, is_with_graphics=False)
    assert pw.current_cell() == (4, 0)
    assert pb.current_cell() == (3, 1)
    time.sleep(0.5)
    game._run_game_loop(num_iterations=100, is_with_graphics=False)
    game.user_input_queue.put(Command(game.game_time_ms(), pw.id, "move", [(4, 0), (3, 1)]))
    time.sleep(0.5)
    game._run_game_loop(num_iterations=100, is_with_graphics=False)
    assert pw.current_cell() == (3, 1)
    assert pw in game.pieces
    assert pb not in game.pieces

