import pytest

from chess.board import Board
from chess.models import ChessColor
from chess.pieces import Bishop, King, Knight, Pawn, Queen, Rock


def test_board_initialization():
    board = Board()
    assert len(board.pieces) == 0
    assert len(board.position_map) == 0

    board.initialize_board()
    assert len(board.pieces) == 32
    assert len(board.position_map) == 32


def test_position_of_pieces_at_board_after_initialization():
    board = Board()
    board.initialize_board()

    assert isinstance(board.position_map["a1"], Rock)
    assert isinstance(board.position_map["b1"], Knight)
    assert isinstance(board.position_map["c1"], Bishop)
    assert isinstance(board.position_map["d1"], Queen)
    assert isinstance(board.position_map["e1"], King)
    assert isinstance(board.position_map["f1"], Bishop)
    assert isinstance(board.position_map["g1"], Knight)
    assert isinstance(board.position_map["h1"], Rock)

    for pos in [f"{x}2" for x in "abcdefgh"]:
        assert isinstance(board.position_map[pos], Pawn)

    assert isinstance(board.position_map["a8"], Rock)
    assert isinstance(board.position_map["b8"], Knight)
    assert isinstance(board.position_map["c8"], Bishop)
    assert isinstance(board.position_map["d8"], Queen)
    assert isinstance(board.position_map["e8"], King)
    assert isinstance(board.position_map["f8"], Bishop)
    assert isinstance(board.position_map["g8"], Knight)
    assert isinstance(board.position_map["h8"], Rock)

    for pos in [f"{x}7" for x in "abcdefgh"]:
        assert isinstance(board.position_map[pos], Pawn)


def test_color_of_pieces_at_board_after_initialization():
    right_colors_map = {f"{x}{i}": ChessColor.WHITE for x in "abcdefgh" for i in [1, 2]}
    right_colors_map.update(
        {f"{x}{i}": ChessColor.BLACK for x in "abcdefgh" for i in [7, 8]}
    )

    board = Board()
    board.initialize_board()

    for pos, color in right_colors_map.items():
        assert board.position_map[pos].color == color
