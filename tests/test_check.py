import pytest

from chess.game import Game
from chess.models import ChessColor, name_2_position
from chess.pieces import Bishop, King, Queen, Knight, Pawn, Rock


def test_if_king_is_in_check_01():
    game = Game(
        pieces=[
            King(color=ChessColor.WHITE, current_position=name_2_position("e5")),
            Queen(color=ChessColor.WHITE, current_position=name_2_position("d6")),
            Pawn(color=ChessColor.WHITE, current_position=name_2_position("g7")),
            King(color=ChessColor.BLACK, current_position=name_2_position("c7")),
            Knight(color=ChessColor.BLACK, current_position=name_2_position("b5")),
        ]
    )

    assert game.verify_if_king_is_in_check(king_color=ChessColor.WHITE) == False
    assert len(game.threatening_pieces[ChessColor.BLACK]) == 0
    assert game.verify_if_king_is_in_check(king_color=ChessColor.BLACK) == True
    assert len(game.threatening_pieces[ChessColor.BLACK]) == 1


def test_if_king_is_in_check_02():
    game = Game(
        pieces=[
            King(color=ChessColor.WHITE, current_position=name_2_position("e5")),
            Pawn(color=ChessColor.WHITE, current_position=name_2_position("g7")),
            King(color=ChessColor.BLACK, current_position=name_2_position("c7")),
            Queen(color=ChessColor.BLACK, current_position=name_2_position("d6")),
            Knight(color=ChessColor.BLACK, current_position=name_2_position("b5")),
        ]
    )

    assert game.verify_if_king_is_in_check(king_color=ChessColor.WHITE) == True
    assert game.verify_if_king_is_in_check(king_color=ChessColor.BLACK) == False


def test_if_king_is_in_check_03():
    game = Game(
        pieces=[
            King(color=ChessColor.WHITE, current_position=name_2_position("e5")),
            Queen(color=ChessColor.WHITE, current_position=name_2_position("c2")),
            Pawn(color=ChessColor.WHITE, current_position=name_2_position("g7")),
            King(color=ChessColor.BLACK, current_position=name_2_position("c7")),
            Knight(color=ChessColor.BLACK, current_position=name_2_position("g4")),
        ]
    )

    assert game.verify_if_king_is_in_check(king_color=ChessColor.WHITE) == True
    assert game.verify_if_king_is_in_check(king_color=ChessColor.BLACK) == True


def test_check_mate_01():
    # Check mate. White wins
    game = Game(
        pieces=[
            King(color=ChessColor.WHITE, current_position=name_2_position("d6")),
            Queen(color=ChessColor.WHITE, current_position=name_2_position("c7")),
            Bishop(color=ChessColor.WHITE, current_position=name_2_position("f3")),
            King(color=ChessColor.BLACK, current_position=name_2_position("b8")),
            Knight(color=ChessColor.BLACK, current_position=name_2_position("g5")),
        ]
    )

    assert game.verify_check_mate(king_color=ChessColor.WHITE) == False
    assert game.verify_check_mate(king_color=ChessColor.BLACK) == True


def test_check_mate_02():
    # King saves himself
    game = Game(
        pieces=[
            King(color=ChessColor.WHITE, current_position=name_2_position("e6")),
            Queen(color=ChessColor.WHITE, current_position=name_2_position("d7")),
            Bishop(color=ChessColor.WHITE, current_position=name_2_position("f3")),
            King(color=ChessColor.BLACK, current_position=name_2_position("c8")),
            Knight(color=ChessColor.BLACK, current_position=name_2_position("f6")),
        ]
    )

    assert game.verify_check_mate(king_color=ChessColor.WHITE) == False
    assert (
        game.verify_check_mate(king_color=ChessColor.BLACK) == False
    )  # King can move to b8


def test_check_mate_03():
    # King captures Queen
    game = Game(
        pieces=[
            King(color=ChessColor.WHITE, current_position=name_2_position("e6")),
            Queen(color=ChessColor.WHITE, current_position=name_2_position("c7")),
            Bishop(color=ChessColor.WHITE, current_position=name_2_position("f3")),
            King(color=ChessColor.BLACK, current_position=name_2_position("c8")),
            Knight(color=ChessColor.BLACK, current_position=name_2_position("f6")),
        ]
    )

    assert game.verify_check_mate(king_color=ChessColor.WHITE) == False
    assert (
        game.verify_check_mate(king_color=ChessColor.BLACK) == False
    )  # King takes Queen


def test_check_mate_04():
    # King is saved by another piece
    game = Game(
        pieces=[
            King(color=ChessColor.WHITE, current_position=name_2_position("d6")),
            Queen(color=ChessColor.WHITE, current_position=name_2_position("c7")),
            Bishop(color=ChessColor.WHITE, current_position=name_2_position("f3")),
            King(color=ChessColor.BLACK, current_position=name_2_position("b8")),
            Knight(color=ChessColor.BLACK, current_position=name_2_position("e6")),
        ]
    )

    assert game.verify_check_mate(king_color=ChessColor.WHITE) == False
    assert (
        game.verify_check_mate(king_color=ChessColor.BLACK) == False
    )  # Knight takes Queen


def test_check_mate_05():
    # Other piece can block the way
    game = Game(
        pieces=[
            King(color=ChessColor.WHITE, current_position=name_2_position("c7")),
            Queen(color=ChessColor.WHITE, current_position=name_2_position("h1")),
            Rock(color=ChessColor.WHITE, current_position=name_2_position("g6")),
            King(color=ChessColor.BLACK, current_position=name_2_position("h8")),
            Knight(color=ChessColor.BLACK, current_position=name_2_position("f4")),
        ]
    )

    assert game.verify_check_mate(king_color=ChessColor.WHITE) == False
    assert (
        game.verify_check_mate(king_color=ChessColor.BLACK) == False
    )  # Knight can block the Queen


def test_check_mate_06():
    # Check mate again
    game = Game(
        pieces=[
            King(color=ChessColor.WHITE, current_position=name_2_position("c7")),
            Queen(color=ChessColor.WHITE, current_position=name_2_position("h1")),
            Rock(color=ChessColor.WHITE, current_position=name_2_position("g6")),
            King(color=ChessColor.BLACK, current_position=name_2_position("h8")),
            Pawn(color=ChessColor.BLACK, current_position=name_2_position("f4")),
        ]
    )

    assert game.verify_check_mate(king_color=ChessColor.WHITE) == False
    assert game.verify_check_mate(king_color=ChessColor.BLACK) == True


def test_check_mate_07():
    # Double check. It's mate.
    game = Game(
        pieces=[
            King(color=ChessColor.WHITE, current_position=name_2_position("c7")),
            Queen(color=ChessColor.WHITE, current_position=name_2_position("g3")),
            Rock(color=ChessColor.WHITE, current_position=name_2_position("h6")),
            Bishop(color=ChessColor.WHITE, current_position=name_2_position("c3")),
            King(color=ChessColor.BLACK, current_position=name_2_position("h8")),
            Pawn(color=ChessColor.BLACK, current_position=name_2_position("e4")),
        ]
    )

    assert game.verify_check_mate(king_color=ChessColor.WHITE) == False
    assert len(game.threatening_pieces[ChessColor.BLACK]) == 0
    assert game.verify_check_mate(king_color=ChessColor.BLACK) == True
    assert len(game.threatening_pieces[ChessColor.BLACK]) == 2
