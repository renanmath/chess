import pytest

from chess.models import ChessColor, LetterPosition, NumberPosition, Position
from chess.pieces import Bishop, King, Knight, Pawn, Queen, Rock


def test_get_positions_of_pieces():
    list_of_arguments = [
        (Pawn, (6, 2), [(5, 3), (6, 3), (7, 3), (6, 4)]),
        (Knight, (2, 3), [(3, 5), (3, 1), (1, 1), (1, 5), (4, 2), (4, 4)]),
        (
            Bishop,
            (4, 3),
            [
                (3, 4),
                (2, 5),
                (1, 6),
                (5, 2),
                (6, 1),
                (3, 2),
                (2, 1),
                (5, 4),
                (6, 5),
                (7, 6),
                (8, 7),
            ],
        ),
        (
            Rock,
            (5, 7),
            [
                (1, 7),
                (2, 7),
                (3, 7),
                (4, 7),
                (6, 7),
                (7, 7),
                (8, 7),
                (5, 1),
                (5, 2),
                (5, 3),
                (5, 4),
                (5, 5),
                (5, 6),
                (5, 8),
            ],
        ),
        (
            Queen,
            (7, 4),
            [
                (7, 1),
                (7, 2),
                (7, 3),
                (7, 5),
                (7, 6),
                (7, 7),
                (7, 8),
                (1, 4),
                (2, 4),
                (3, 4),
                (4, 4),
                (5, 4),
                (6, 4),
                (8, 4),
                (3, 8),
                (4, 7),
                (5, 6),
                (6, 5),
                (8, 3),
                (4, 1),
                (5, 2),
                (6, 3),
                (8, 5),
            ],
        ),
        (King, (8, 2), [(8, 3), (7, 3), (7, 2), (7, 1), (8, 1)]),
    ]

    for piece_class, (i, j), expected_coordinates in list_of_arguments:
        position = Position(x=LetterPosition(i), y=NumberPosition(j))
        piece = piece_class(color=ChessColor.WHITE, current_position=position)
        possible_positions_to_move = piece.get_possible_positions_to_move()
        for p in possible_positions_to_move:
            assert p is not None

        coordinates = [p.coordinates for p in possible_positions_to_move]
        assert len(coordinates) == len(expected_coordinates)

        for expected in expected_coordinates:
            assert expected in coordinates
