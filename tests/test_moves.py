import pytest

from chess.board import Board
from chess.models import ChessColor, coordinates_2_position, name_2_position
from chess.pieces import Bishop, King, Knight, Pawn, Queen, Rock


def test_move_piece_to_new_position():
    board = Board()
    board.initialize_board()

    with pytest.raises(KeyError):
        board.position_map["d3"]

    piece_before_move = board.position_map["d2"]
    assert str(piece_before_move.current_position) == "d2"
    board.move_piece_to_new_position("d2", "d3")
    piece = board.position_map["d3"]
    assert piece == piece_before_move

    with pytest.raises(KeyError):
        board.position_map["d2"]

    assert str(piece.current_position) == "d3"


def test_capture_piece():
    board = Board()
    board.initialize_board(
        pieces=[
            white_rock := Rock(
                color=ChessColor.WHITE, current_position=coordinates_2_position((3, 3))
            ),
            black_rock := Rock(
                color=ChessColor.BLACK, current_position=coordinates_2_position((7, 3))
            ),
        ]
    )

    assert white_rock in board.pieces
    assert black_rock in board.pieces
    assert len(board.captured_pieces[ChessColor.WHITE]) == 0
    assert len(board.captured_pieces[ChessColor.BLACK]) == 0

    board.capture_piece("c3", "g3")

    assert white_rock in board.pieces
    assert black_rock not in board.pieces
    assert len(board.captured_pieces[ChessColor.WHITE]) == 0
    assert len(board.captured_pieces[ChessColor.BLACK]) == 1


def test_check_if_en_passant_is_possible_01():
    board = Board()
    board.initialize_board()

    board.move_piece_to_new_position("e2", "e4")
    board.move_piece_to_new_position("b8", "c6")
    board.move_piece_to_new_position("e4", "e5")
    board.move_piece_to_new_position("f7", "f5")

    assert board.check_if_en_passant_is_possible("e5", "f5") == True


def test_check_if_en_passant_is_possible_02():
    board = Board()
    board.initialize_board()

    board.move_piece_to_new_position("e2", "e4")
    board.move_piece_to_new_position("b8", "c6")
    board.move_piece_to_new_position("e4", "e5")
    board.move_piece_to_new_position("f7", "f6")
    board.move_piece_to_new_position("c2", "c3")
    board.move_piece_to_new_position("f6", "f5")

    assert board.check_if_en_passant_is_possible("e5", "f5") == False


def test_check_if_en_passant_is_possible_03():
    board = Board()
    board.initialize_board()

    board.move_piece_to_new_position("e2", "e4")
    board.move_piece_to_new_position("f7", "f5")

    assert board.check_if_en_passant_is_possible("e5", "f5") == False


def test_check_if_kingside_castling_is_possible_01():
    sequence_of_moves = [
        ("g1", "f3"),
        ("d7", "d6"),
        ("g2", "g4"),
        ("g8", "f6"),
        ("f1", "g2"),
        ("d8", "c6"),
    ]
    board = Board()
    board.initialize_board()

    for position, next_position in sequence_of_moves:
        board.move_piece_to_new_position(position, next_position)

    assert board.check_if_castling_is_possible("e1", "h1") == True


def test_check_if_kingside_castling_is_possible_02():
    sequence_of_moves = [("g1", "f3"), ("d7", "d6"), ("g2", "g4"), ("g8", "f6")]
    board = Board()
    board.initialize_board()

    for position, next_position in sequence_of_moves:
        board.move_piece_to_new_position(position, next_position)

    assert (
        board.check_if_castling_is_possible("e1", "h1") == False
    )  # Bishop is blocking the way


def test_check_if_kingside_castling_is_possible_03():
    sequence_of_moves = [
        ("g1", "f3"),
        ("d7", "d6"),
        ("g2", "g4"),
        ("g8", "f6"),
        ("f1", "g2"),
        ("b8", "c6"),
        ("g7", "g5"),
        ("e1", "f1"),
        ("d8", "d7"),
    ]
    board = Board()
    board.initialize_board()

    for position, next_position in sequence_of_moves:
        board.move_piece_to_new_position(position, next_position)

    assert board.check_if_castling_is_possible("f1", "h1") == False  # King has moved


def test_check_if_kingside_castling_is_possible_04():
    sequence_of_moves = [
        ("g1", "f3"),
        ("d7", "d6"),
        ("g2", "g4"),
        ("g8", "f6"),
        ("f1", "g2"),
        ("b8", "c6"),
        ("g7", "g5"),
        ("e1", "f1"),
        ("d8", "d7"),
        ("a7", "a5"),
        ("f1", "e1"),
        ("f6", "d5"),
    ]
    board = Board()
    board.initialize_board()

    for position, next_position in sequence_of_moves:
        board.move_piece_to_new_position(position, next_position)

    assert (
        board.check_if_castling_is_possible("e1", "h1") == False
    )  # King has moved already in game


def test_check_if_kingside_castling_is_possible_05():
    sequence_of_moves = [
        ("g1", "f3"),
        ("d7", "d6"),
        ("g2", "g4"),
        ("g8", "f6"),
        ("f1", "g2"),
        ("b8", "c6"),
        ("g7", "g5"),
        ("h1", "g1"),
        ("d8", "d7"),
        ("a7", "a5"),
        ("g1", "h1"),
        ("f6", "d5"),
    ]
    board = Board()
    board.initialize_board()

    for position, next_position in sequence_of_moves:
        board.move_piece_to_new_position(position, next_position)

    assert (
        board.check_if_castling_is_possible("e1", "h1") == False
    )  # Rock has moved already in game


def test_check_if_queenside_castling_is_possible_01():
    sequence_of_moves = [
        ("b1", "c3"),
        ("c3", "c5"),
        ("d2", "d3"),
        ("g8", "f6"),
        ("c1", "e3"),
        ("e7", "e5"),
        ("d1", "d2"),
        ("f8", "d6"),
    ]
    board = Board()
    board.initialize_board()

    for position, next_position in sequence_of_moves:
        board.move_piece_to_new_position(position, next_position)

    assert board.check_if_castling_is_possible("e1", "a1") == True


def test_check_if_queenside_castling_is_possible_02():
    sequence_of_moves = [
        ("b1", "c3"),
        ("c3", "c5"),
        ("d2", "d3"),
        ("g8", "f6"),
        ("c1", "e3"),
        ("e7", "e5"),
    ]
    board = Board()
    board.initialize_board()

    for position, next_position in sequence_of_moves:
        board.move_piece_to_new_position(position, next_position)

    assert (
        board.check_if_castling_is_possible("e1", "a1") == False
    )  # Queen is blocking the way


def test_check_if_queenside_castling_is_possible_03():
    sequence_of_moves = [
        ("b1", "c3"),
        ("c3", "c5"),
        ("d2", "d3"),
        ("g8", "f6"),
        ("c1", "e3"),
        ("e7", "e5"),
        ("d1", "d2"),
        ("f8", "d6"),
        ("e1", "d1"),
        ("d8", "e7"),
    ]
    board = Board()
    board.initialize_board()

    for position, next_position in sequence_of_moves:
        board.move_piece_to_new_position(position, next_position)

    assert board.check_if_castling_is_possible("d1", "a1") == False  # King has moved


def test_check_if_queenside_castling_is_possible_04():
    sequence_of_moves = [
        ("b1", "c3"),
        ("c3", "c5"),
        ("d2", "d3"),
        ("g8", "f6"),
        ("c1", "e3"),
        ("e7", "e5"),
        ("d1", "d2"),
        ("f8", "d6"),
        ("e1", "d1"),
        ("d8", "e7"),
        ("d1", "e1"),
        ("f6", "g4"),
    ]
    board = Board()
    board.initialize_board()

    for position, next_position in sequence_of_moves:
        board.move_piece_to_new_position(position, next_position)

    assert board.check_if_castling_is_possible("e1", "a1") == False  # King has moved


def test_check_if_queenside_castling_is_possible_05():
    sequence_of_moves = [
        ("b1", "c3"),
        ("c3", "c5"),
        ("d2", "d3"),
        ("g8", "f6"),
        ("c1", "e3"),
        ("e7", "e5"),
        ("d1", "d2"),
        ("f8", "d6"),
        ("a1", "b1"),
        ("d8", "e7"),
        ("b1", "a1"),
        ("f6", "g4"),
    ]
    board = Board()
    board.initialize_board()

    for position, next_position in sequence_of_moves:
        board.move_piece_to_new_position(position, next_position)

    assert board.check_if_castling_is_possible("e1", "a1") == False  # Rock has moved


def test_can_promote():
    board = Board()
    board.initialize_board(
        pieces=[
            white_king := King(
                color=ChessColor.WHITE, current_position=name_2_position("c6")
            ),
            white_rock := Rock(
                color=ChessColor.WHITE, current_position=name_2_position("h8")
            ),
            white_pawn := Pawn(
                color=ChessColor.WHITE, current_position=name_2_position("g7")
            ),
            promo_white_pawn := Pawn(
                color=ChessColor.WHITE, current_position=name_2_position("d8")
            ),
            black_king := King(
                color=ChessColor.BLACK, current_position=name_2_position("f4")
            ),
            black_pawn := Pawn(
                color=ChessColor.BLACK, current_position=name_2_position("d2")
            ),
            promo_black_pawn := Pawn(
                color=ChessColor.BLACK, current_position=name_2_position("b1")
            ),
            black_knight := Knight(
                color=ChessColor.BLACK, current_position=name_2_position("f1")
            ),
        ]
    )

    assert board.can_promote(piece=white_pawn) == False
    assert board.can_promote(piece=promo_white_pawn) == True
    assert board.can_promote(piece=white_rock) == False
    assert board.can_promote(piece=black_pawn) == False
    assert board.can_promote(piece=promo_black_pawn) == True
    assert board.can_promote(piece=black_knight) == False


def test_promotion_01():
    board = Board()

    board.initialize_board(
        pieces=[
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
    )

    board.move("d7", "d8", promotion_class=Rock)
    promoted_piece = board.position_map["d8"]
    assert isinstance(promoted_piece, Rock)
    assert white_pawn not in board.pieces
    assert promoted_piece in board.pieces

