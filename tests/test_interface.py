import pytest

from chess.game import Game
from chess.interface import GameInterface
from chess.models import ChessColor, name_2_position
from chess.pieces import Bishop, King, Knight, Pawn, Rock


def test_parse_algebraic_notation():
    game = Game(
        pieces=[
            King(color=ChessColor.WHITE, current_position=name_2_position("e3")),
            Rock(color=ChessColor.WHITE, current_position=name_2_position("h1")),
            Rock(color=ChessColor.WHITE, current_position=name_2_position("f3")),
            Knight(color=ChessColor.WHITE, current_position=name_2_position("b4")),
            Knight(color=ChessColor.WHITE, current_position=name_2_position("f6")),
            Pawn(color=ChessColor.WHITE, current_position=name_2_position("h7")),
            King(color=ChessColor.BLACK, current_position=name_2_position("f8")),
            Rock(color=ChessColor.BLACK, current_position=name_2_position("a7")),
            Bishop(color=ChessColor.BLACK, current_position=name_2_position("c6")),
            Pawn(color=ChessColor.BLACK, current_position=name_2_position("d5")),
            Pawn(color=ChessColor.BLACK, current_position=name_2_position("c2")),
        ]
    )

    interface = GameInterface(game)

    test_info = [
        (
            "Ng4",
            ChessColor.WHITE,
            ("f6", "g4", None, False, None, False, None),
        ),  # Knight at f6 goes to g4
        (
            "Ra4",
            ChessColor.BLACK,
            ("a7", "a4", None, False, None, False, None),
        ),  # Rock at a7 goes to a4
        (
            "h8=B",
            ChessColor.WHITE,
            ("h7", "h8", Bishop, False, None, False, None),
        ),  # Pawn at h7 promoted to Bishop at h8
        (
            "Rxh7",
            ChessColor.BLACK,
            ("a7", "h7", None, False, None, False, None),
        ),  # Rock at a7 takes pawn at h7
        (
            "NxBc6",
            ChessColor.WHITE,
            ("b4", "c6", None, False, None, False, None),
        ),  # Knight at b4 takes Bishop at c6
        (
            "Nbxd5",
            ChessColor.WHITE,
            ("b4", "d5", None, False, None, False, None),
        ),  # Knight at b4 takes pawn at d5
        (
            "N6xd5",
            ChessColor.WHITE,
            ("f6", "d5", None, False, None, False, None),
        ),  # Knight at f6 takes pawn at d5
        (
            "Nfxd5",
            ChessColor.WHITE,
            ("f6", "d5", None, False, None, False, None),
        ),  # Knight at f6 takes pawn at d5
        (
            "Rfh3",
            ChessColor.WHITE,
            ("f3", "h3", None, False, None, False, None),
        ),  # Rock at f6 goes to h3
        (
            "R1h3",
            ChessColor.WHITE,
            ("h1", "h3", None, False, None, False, None),
        ),  # Rock at h1 goes to h3
    ]

    for notation, color, expected_result in test_info:
        result = interface.get_move_info_from_algebraic_notation(notation, color)
        assert result == expected_result


def test_en_passant_notation_01():
    game = Game(
        pieces=[
            King(color=ChessColor.WHITE, current_position=name_2_position("c1")),
            Pawn(color=ChessColor.WHITE, current_position=name_2_position("f5")),
            King(color=ChessColor.BLACK, current_position=name_2_position("f8")),
            Pawn(color=ChessColor.BLACK, current_position=name_2_position("g5")),
        ]
    )

    interface = GameInterface(game)
    """
        origin,
        destination,
        promotion_class,
        en_passant,
        enemy_pawn_position,
        castling,
        rock_position,
        """
    (
        origin,
        destination,
        _,
        en_passant,
        enemy_pawn_position,
        _,
        _,
    ) = interface.get_move_info_from_algebraic_notation("fxg6 e.p.", ChessColor.WHITE)

    assert origin == "f5"
    assert destination == "g6"
    assert en_passant == True
    assert enemy_pawn_position == "g5"


def test_en_passant_notation_02():
    game = Game(
        pieces=[
            King(color=ChessColor.WHITE, current_position=name_2_position("c1")),
            Pawn(color=ChessColor.WHITE, current_position=name_2_position("d5")),
            Pawn(color=ChessColor.WHITE, current_position=name_2_position("f5")),
            King(color=ChessColor.BLACK, current_position=name_2_position("f8")),
            Pawn(color=ChessColor.BLACK, current_position=name_2_position("e5")),
        ]
    )

    interface = GameInterface(game)
    """
        origin,
        destination,
        promotion_class,
        en_passant,
        enemy_pawn_position,
        castling,
        rock_position,
        """
    (
        origin,
        destination,
        _,
        en_passant,
        enemy_pawn_position,
        _,
        _,
    ) = interface.get_move_info_from_algebraic_notation("dxe6 e.p.", ChessColor.WHITE)

    assert origin == "d5"
    assert destination == "e6"
    assert en_passant == True
    assert enemy_pawn_position == "e5"


def test_castling_notation():
    interface = GameInterface(game=Game())

    (
        origin,
        destination,
        _,
        _,
        _,
        castling,
        rock_position,
    ) = interface.get_move_info_from_algebraic_notation("0-0", ChessColor.WHITE)

    assert origin == "e1"
    assert destination == "g1"
    assert castling == True
    assert rock_position == "h1"

    (
        origin,
        destination,
        _,
        _,
        _,
        castling,
        rock_position,
    ) = interface.get_move_info_from_algebraic_notation("0-0", ChessColor.BLACK)

    assert origin == "e8"
    assert destination == "g8"
    assert castling == True
    assert rock_position == "h8"

    (
        origin,
        destination,
        _,
        _,
        _,
        castling,
        rock_position,
    ) = interface.get_move_info_from_algebraic_notation("0-0-0", ChessColor.WHITE)

    assert origin == "e1"
    assert destination == "c1"
    assert castling == True
    assert rock_position == "a1"

    (
        origin,
        destination,
        _,
        _,
        _,
        castling,
        rock_position,
    ) = interface.get_move_info_from_algebraic_notation("0-0-0", ChessColor.BLACK)

    assert origin == "e8"
    assert destination == "c8"
    assert castling == True
    assert rock_position == "a8"
