import pytest

from chess.game import Game
from chess.models import ChessColor, coordinates_2_position
from chess.pieces import Bishop, King, Knight, Pawn, Queen


def test_verify_if_path_is_blocked_01():
    # Diagonal is free
    pieces = [
        white_pawn := Pawn(
            color=ChessColor.WHITE, current_position=coordinates_2_position((4, 7))
        ),
        white_king := King(
            color=ChessColor.WHITE, current_position=coordinates_2_position((4, 6))
        ),
        black_knight := Knight(
            color=ChessColor.BLACK, current_position=coordinates_2_position((7, 5))
        ),
        black_bishop := Bishop(
            color=ChessColor.BLACK, current_position=coordinates_2_position((3, 4))
        ),
        black_king := King(
            color=ChessColor.BLACK, current_position=coordinates_2_position((6, 4))
        ),
    ]

    game = Game(pieces=pieces)

    assert game.verify_if_path_is_not_blocked_by_another_piece("c4", "f7") == True


def test_verify_if_path_is_blocked_02():
    # Diagonal is blocked
    pieces = [
        white_pawn := Pawn(
            color=ChessColor.WHITE, current_position=coordinates_2_position((4, 7))
        ),
        white_king := King(
            color=ChessColor.WHITE, current_position=coordinates_2_position((4, 6))
        ),
        black_knight := Knight(
            color=ChessColor.BLACK, current_position=coordinates_2_position((4, 5))
        ),
        black_bishop := Bishop(
            color=ChessColor.BLACK, current_position=coordinates_2_position((3, 4))
        ),
        black_king := King(
            color=ChessColor.BLACK, current_position=coordinates_2_position((6, 4))
        ),
    ]

    game = Game(pieces=pieces)

    assert (
        game.verify_if_path_is_not_blocked_by_another_piece("c4", "f7") == False
    )  # Black Knight is blocking the way at d5


def test_verify_if_path_is_blocked_03():
    # Row is free
    pieces = [
        white_pawn := Pawn(
            color=ChessColor.WHITE, current_position=coordinates_2_position((4, 7))
        ),
        white_king := King(
            color=ChessColor.WHITE, current_position=coordinates_2_position((4, 6))
        ),
        black_knight := Knight(
            color=ChessColor.BLACK, current_position=coordinates_2_position((6, 5))
        ),
        black_queen := Queen(
            color=ChessColor.BLACK, current_position=coordinates_2_position((3, 4))
        ),
        black_king := King(
            color=ChessColor.BLACK, current_position=coordinates_2_position((6, 6))
        ),
    ]

    game = Game(pieces=pieces)

    assert game.verify_if_path_is_not_blocked_by_another_piece("c4", "h4") == True


def test_verify_if_path_is_blocked_04():
    # Row is blocked
    pieces = [
        white_pawn := Pawn(
            color=ChessColor.WHITE, current_position=coordinates_2_position((4, 7))
        ),
        white_king := King(
            color=ChessColor.WHITE, current_position=coordinates_2_position((4, 6))
        ),
        black_knight := Knight(
            color=ChessColor.BLACK, current_position=coordinates_2_position((6, 4))
        ),
        black_queen := Queen(
            color=ChessColor.BLACK, current_position=coordinates_2_position((3, 4))
        ),
        black_king := King(
            color=ChessColor.BLACK, current_position=coordinates_2_position((6, 6))
        ),
    ]

    game = Game(pieces=pieces)

    assert (
        game.verify_if_path_is_not_blocked_by_another_piece("c4", "h4") == False
    )  # Black Knight is blocking the way at f4


def test_verify_if_path_is_blocked_05():
    # Column is free
    pieces = [
        white_pawn := Pawn(
            color=ChessColor.WHITE, current_position=coordinates_2_position((4, 7))
        ),
        white_king := King(
            color=ChessColor.WHITE, current_position=coordinates_2_position((4, 6))
        ),
        black_knight := Knight(
            color=ChessColor.BLACK, current_position=coordinates_2_position((6, 5))
        ),
        black_queen := Queen(
            color=ChessColor.BLACK, current_position=coordinates_2_position((3, 4))
        ),
        black_king := King(
            color=ChessColor.BLACK, current_position=coordinates_2_position((6, 6))
        ),
    ]

    game = Game(pieces=pieces)

    assert game.verify_if_path_is_not_blocked_by_another_piece("c4", "c7") == True


def test_verify_if_path_is_blocked_06():
    # Column is blocked
    pieces = [
        white_pawn := Pawn(
            color=ChessColor.WHITE, current_position=coordinates_2_position((4, 7))
        ),
        white_king := King(
            color=ChessColor.WHITE, current_position=coordinates_2_position((4, 6))
        ),
        black_knight := Knight(
            color=ChessColor.BLACK, current_position=coordinates_2_position((3, 6))
        ),
        black_queen := Queen(
            color=ChessColor.BLACK, current_position=coordinates_2_position((3, 4))
        ),
        black_king := King(
            color=ChessColor.BLACK, current_position=coordinates_2_position((6, 6))
        ),
    ]

    game = Game(pieces=pieces)

    assert (
        game.verify_if_path_is_not_blocked_by_another_piece("c4", "c7") == False
    )  # Black Knight is blocking at c6


def test_verify_if_path_is_blocked_08():
    # Reverse Diagonal is free
    pieces = [
        white_pawn := Pawn(
            color=ChessColor.WHITE, current_position=coordinates_2_position((4, 7))
        ),
        white_king := King(
            color=ChessColor.WHITE, current_position=coordinates_2_position((4, 6))
        ),
        white_knight := Knight(
            color=ChessColor.WHITE, current_position=coordinates_2_position((3, 5))
        ),
        black_queen := Queen(
            color=ChessColor.BLACK, current_position=coordinates_2_position((2, 5))
        ),
        black_king := King(
            color=ChessColor.BLACK, current_position=coordinates_2_position((6, 4))
        ),
    ]

    game = Game(pieces=pieces)

    assert game.verify_if_path_is_not_blocked_by_another_piece("b5", "d3") == True


def test_verify_if_path_is_blocked_08():
    # Reverse Diagonal is blocked
    pieces = [
        white_pawn := Pawn(
            color=ChessColor.WHITE, current_position=coordinates_2_position((4, 7))
        ),
        white_king := King(
            color=ChessColor.WHITE, current_position=coordinates_2_position((4, 6))
        ),
        white_knight := Knight(
            color=ChessColor.WHITE, current_position=coordinates_2_position((3, 4))
        ),
        black_queen := Queen(
            color=ChessColor.BLACK, current_position=coordinates_2_position((2, 5))
        ),
        black_king := King(
            color=ChessColor.BLACK, current_position=coordinates_2_position((6, 4))
        ),
    ]

    game = Game(pieces=pieces)

    assert (
        game.verify_if_path_is_not_blocked_by_another_piece("b5", "d3") == False
    )  # White Knight is blocking the way at c4


def test_verify_if_path_is_blocked_09():
    # Reversed Row is free
    pieces = [
        white_pawn := Pawn(
            color=ChessColor.WHITE, current_position=coordinates_2_position((4, 7))
        ),
        white_king := King(
            color=ChessColor.WHITE, current_position=coordinates_2_position((6, 6))
        ),
        white_rock := Knight(
            color=ChessColor.WHITE, current_position=coordinates_2_position((4, 6))
        ),
        black_queen := Queen(
            color=ChessColor.BLACK, current_position=coordinates_2_position((4, 3))
        ),
        black_king := King(
            color=ChessColor.BLACK, current_position=coordinates_2_position((6, 4))
        ),
    ]

    game = Game(pieces=pieces)

    assert game.verify_if_path_is_not_blocked_by_another_piece("d6", "b6") == True


def test_verify_if_path_is_blocked_10():
    # Reversed Row is free
    pieces = [
        white_pawn := Pawn(
            color=ChessColor.WHITE, current_position=coordinates_2_position((4, 7))
        ),
        white_king := King(
            color=ChessColor.WHITE, current_position=coordinates_2_position((3, 6))
        ),
        white_rock := Knight(
            color=ChessColor.WHITE, current_position=coordinates_2_position((4, 6))
        ),
        black_queen := Queen(
            color=ChessColor.BLACK, current_position=coordinates_2_position((4, 3))
        ),
        black_king := King(
            color=ChessColor.BLACK, current_position=coordinates_2_position((6, 4))
        ),
    ]

    game = Game(pieces=pieces)

    assert (
        game.verify_if_path_is_not_blocked_by_another_piece("d6", "b6") == False
    )  # King is blocking the way at c6
