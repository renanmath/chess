from copy import deepcopy
from chess.models import (
    ChessColor,
    Position,
    coordinates_2_position,
    name_2_position,
)
from chess.pieces import Bishop, King, Knight, Pawn, Piece, Queen, Rock


class Board:
    def __init__(self) -> None:
        self.pieces: list[Piece] = list()
        self.position_map: dict[str, Piece] = dict()
        self.captured_pieces = {color: list() for color in ChessColor}

    def initialize_board(self, pieces: list[Piece] | None = None):

        if pieces:
            self.pieces = pieces
        else:
            self.set_initial_position_of_pieces()

        for piece in self.pieces:
            self.position_map[str(piece.current_position)] = piece

    def set_initial_position_of_pieces(self):
        self.pieces = list()
        self.pieces.extend(
            [
                Pawn(
                    color=ChessColor.WHITE,
                    current_position=coordinates_2_position((i, 2)),
                )
                for i in range(1, 9)
            ]
        )
        self.pieces.extend(
            [
                Rock(
                    color=ChessColor.WHITE,
                    current_position=coordinates_2_position((1, 1)),
                ),
                Knight(
                    color=ChessColor.WHITE,
                    current_position=coordinates_2_position((2, 1)),
                ),
                Bishop(
                    color=ChessColor.WHITE,
                    current_position=coordinates_2_position((3, 1)),
                ),
                Queen(
                    color=ChessColor.WHITE,
                    current_position=coordinates_2_position((4, 1)),
                ),
                King(
                    color=ChessColor.WHITE,
                    current_position=coordinates_2_position((5, 1)),
                ),
                Bishop(
                    color=ChessColor.WHITE,
                    current_position=coordinates_2_position((6, 1)),
                ),
                Knight(
                    color=ChessColor.WHITE,
                    current_position=coordinates_2_position((7, 1)),
                ),
                Rock(
                    color=ChessColor.WHITE,
                    current_position=coordinates_2_position((8, 1)),
                ),
            ]
        )

        self.pieces.extend(
            [
                Pawn(
                    color=ChessColor.BLACK,
                    current_position=coordinates_2_position((i, 7)),
                )
                for i in range(1, 9)
            ]
        )
        self.pieces.extend(
            [
                Rock(
                    color=ChessColor.BLACK,
                    current_position=coordinates_2_position((1, 8)),
                ),
                Knight(
                    color=ChessColor.BLACK,
                    current_position=coordinates_2_position((2, 8)),
                ),
                Bishop(
                    color=ChessColor.BLACK,
                    current_position=coordinates_2_position((3, 8)),
                ),
                Queen(
                    color=ChessColor.BLACK,
                    current_position=coordinates_2_position((4, 8)),
                ),
                King(
                    color=ChessColor.BLACK,
                    current_position=coordinates_2_position((5, 8)),
                ),
                Bishop(
                    color=ChessColor.BLACK,
                    current_position=coordinates_2_position((6, 8)),
                ),
                Knight(
                    color=ChessColor.BLACK,
                    current_position=coordinates_2_position((7, 8)),
                ),
                Rock(
                    color=ChessColor.BLACK,
                    current_position=coordinates_2_position((8, 8)),
                ),
            ]
        )

    def display(self):
        space = " | "
        for r in range(8, 0, -1):
            print(f"{r}  | ", end="")
            for c in "abcdefgh":
                piece = self.position_map.get(f"{c}{r}", None)
                if piece is None:
                    print(" ", end=space)
                else:
                    print(piece.symbol, end=space)

            print("\n")

        print("     a   b   c   d   e   f   g   h")

    def move_piece_to_new_position(self, piece_position: str, new_position: str):
        # This method do not check if move is valid
        # This verification must be made before move

        old_piece_at_location = self.position_map.get(new_position, None)
        piece = self.position_map[piece_position]
        piece.move(name_2_position(new_position))
        self.position_map[new_position] = piece
        del self.position_map[piece_position]

        return piece, old_piece_at_location

    def check_if_castling_is_possible(
        self, king_position: str, rock_position: str
    ) -> bool:

        king = self.position_map.get(king_position, None)
        if king is None or not isinstance(king, King):
            return False

        rock = self.position_map.get(rock_position, None)
        if rock is None or not isinstance(rock, Rock):
            return False

        if king.color != rock.color:
            return False

        if king.num_movements > 0 or rock.num_movements > 0:
            return False

        if king.color == ChessColor.WHITE:
            if king_position != "e1":
                return False
            elif rock_position not in ["a1", "h1"]:
                return False
            else:
                sequence = {"a1": ["b1", "c1", "d1"], "h1": ["g1", "f1"]}

                for pos in sequence[rock_position]:
                    piece = self.position_map.get(pos, None)
                    if piece is not None:
                        return False

        if king.color == ChessColor.BLACK:
            if king_position != "e8":
                return False
            elif rock_position not in ["a8", "h8"]:
                return False
            else:
                sequence = {"a8": ["b8", "c8", "d8"], "h8": ["g8", "f8"]}

                for pos in sequence[rock_position]:
                    piece = self.position_map.get(pos, None)
                    if piece is not None:
                        return False

        return True

    def check_if_en_passant_is_possible(
        self, pawn_position: str, enemy_pawn_position: str
    ) -> bool:

        pawn = self.position_map.get(pawn_position, None)
        if pawn is None or not isinstance(pawn, Pawn):
            return False

        enemy_pawn = self.position_map.get(enemy_pawn_position, None)
        if enemy_pawn is None or not isinstance(enemy_pawn, Pawn):
            return False

        if pawn.color == enemy_pawn.color:
            return False

        if pawn.color == ChessColor.WHITE and pawn.current_position.coordinates[1] != 5:
            return False
        if pawn.color == ChessColor.BLACK and pawn.current_position.coordinates[1] != 4:
            return False

        if enemy_pawn.num_movements != 1:
            return False

        return (
            abs(
                pawn.current_position.coordinates[0]
                - enemy_pawn.current_position.coordinates[0]
            )
            == 1
        )

    def capture_piece(self, position: str, position_to_capture: str):
        piece, captured_piece = self.move_piece_to_new_position(
            position, position_to_capture
        )
        self.pieces.remove(captured_piece)
        self.captured_pieces[captured_piece.color].append(captured_piece)

        return piece, captured_piece

    def promote_piece(self, position_of_piece: str, class_to_promote: type[Piece]):
        original_piece = self.position_map[position_of_piece]
        promoted_piece = class_to_promote(
            color=original_piece.color, current_position=original_piece.current_position
        )
        self.position_map[position_of_piece] = promoted_piece
        self.pieces.remove(original_piece)
        self.pieces.append(promoted_piece)

    def move(
        self,
        original_position: str,
        destination_position: str,
        promotion_class: type[Piece] = Queen,
    ):

        piece_at_destination = self.position_map.get(destination_position, None)
        if piece_at_destination is not None:
            piece, captured_piece = self.capture_piece(
                original_position, destination_position
            )
        else:
            piece, captured_piece = self.move_piece_to_new_position(
                original_position, destination_position
            )

        if self.can_promote(piece) and promotion_class is not None:
            self.promote_piece(destination_position, class_to_promote=promotion_class)

        return piece, captured_piece

    def can_promote(self, piece: Piece):
        if not isinstance(piece, Pawn):
            return False
        column = piece.current_position.coordinates[1]
        return (column, piece.color) in [(8, ChessColor.WHITE), (1, ChessColor.BLACK)]

    def copy(self):
        board_copy = Board()
        board_copy.initialize_board(pieces=deepcopy(self.pieces))
        return board_copy
