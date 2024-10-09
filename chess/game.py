from chess.board import Board
from chess.models import (
    ChessColor,
    ChessException,
    coordinates_2_position,
    name_2_position,
)
from chess.pieces import King, Knight, Piece, Queen
from chess.utils import sign_or_null

opponent_color = {
    ChessColor.WHITE: ChessColor.BLACK,
    ChessColor.BLACK: ChessColor.WHITE,
}


class Game:
    def __init__(self, pieces: list[Piece] | None = None) -> None:
        self.board = Board()
        self.board.initialize_board(pieces=pieces)
        self.kings_position: dict[ChessColor, str] = dict()
        self.threatening_pieces: dict[ChessColor, list[Piece]] = {
            c: [] for c in ChessColor
        }
        self.winning_player: ChessColor | None = None

        for piece in self.board.pieces:
            if isinstance(piece, King):
                self.kings_position[piece.color] = str(piece.current_position)

        if len(self.kings_position) < 2:
            raise ChessException("One must have two kings at the board")

    def verify_if_path_is_not_blocked_by_another_piece(
        self, origin: str, destination: str
    ):
        if origin == destination:
            return True

        destination_position = name_2_position(destination)

        for next_position in self.get_straight_path_from_origin_to_destination(
            origin, destination
        ):
            if next_position == destination_position:
                return True
            piece = self.board.position_map.get(str(next_position), None)
            if piece is not None:
                return False

    def get_straight_path_from_origin_to_destination(
        self, origin: str, destination: str
    ):
        origin_position = name_2_position(origin)
        destination_position = name_2_position(destination)
        a, b = origin_position.coordinates
        c, d = destination_position.coordinates
        x, y = (c - a, d - b)
        vector = (sign_or_null(x), sign_or_null(y))

        while True:
            next_position = coordinates_2_position((a + vector[0], b + vector[1]))
            if next_position is None:
                break
            yield next_position
            a, b = next_position.coordinates

    def verify_if_piece_can_move_to_location(
        self, position: str, destination: str
    ) -> bool:
        piece = self.board.position_map.get(position, None)
        destination_position = name_2_position(destination)
        if piece is None:
            raise ChessException(f"There is not a piece at location {position}")

        other_piece = self.board.position_map.get(destination, None)
        if other_piece is not None and other_piece.color == piece.color:
            # Cannot move to location of piece of same color
            return False

        if destination_position not in list(piece.get_possible_positions_to_move()):
            return False

        if isinstance(piece, Pawn):
            pawn_position = piece.current_position
            if other_piece is None and destination_position in [
                pawn_position.get_left_down_position(),
                pawn_position.get_left_up_position(),
                pawn_position.get_right_down_position(),
                pawn_position.get_right_up_position(),
            ]:
                return False

        if not isinstance(piece, Knight):
            return self.verify_if_path_is_not_blocked_by_another_piece(
                position, destination
            )
        else:
            # Knight can jump over other pieces
            return True

    def verify_if_king_is_in_check(
        self, king_color: ChessColor, board: Board | None = None
    ):
        if board is not None:
            aux_game = Game(pieces=board.pieces)
            return aux_game.verify_if_king_is_in_check(king_color=king_color)

        king_position = self.kings_position[king_color]
        threatening_pieces = list()
        for piece in self.board.pieces:
            if piece.color == king_color:
                continue
            if self.verify_if_piece_can_move_to_location(
                position=str(piece.current_position), destination=king_position
            ):
                threatening_pieces.append(piece)

        self.threatening_pieces[king_color] = threatening_pieces
        return len(threatening_pieces) > 0

    def verify_check_mate(self, king_color: ChessColor):
        king_position = self.kings_position[king_color]
        king = self.board.position_map[king_position]

        if not self.verify_if_king_is_in_check(king_color=king.color):
            return False

        # Check if king can save himself by moving to safe position
        for position in king.get_possible_positions_to_move():
            if not self.verify_if_piece_can_move_to_location(
                position=king_position, destination=str(position)
            ):
                continue
            new_board = self.board.copy()
            new_board.move(king_position, str(position))
            if not self.verify_if_king_is_in_check(
                king_color=king.color, board=new_board
            ):
                return False

        # Check if any piece can capture threatening piece
        if len(self.threatening_pieces[king_color]) > 1:
            # Impossible escape from a double check by capture more then one piece in single move
            return True

        threatening_piece = self.threatening_pieces[king_color][0]
        enemy_pieces = (p for p in self.board.pieces if p.color == king_color)
        for enemy_piece in enemy_pieces:
            try:
                self.validate_move(
                    origin=str(enemy_piece.current_position),
                    destination=str(threatening_piece.current_position),
                )
                return False
            except ChessException:
                continue

        # Check if any piece can block the way of threatening piece
        enemy_pieces = (p for p in self.board.pieces if p.color == king_color)
        for enemy_piece in enemy_pieces:
            positions_in_path = self.get_straight_path_from_origin_to_destination(
                str(threatening_piece.current_position), king_position
            )
            for pos in positions_in_path:
                try:
                    self.validate_move(str(enemy_piece.current_position), str(pos))
                    return False
                except ChessException:
                    continue
        return True

    def validate_move(
        self,
        origin: str,
        destination: str,
        en_passant: bool = False,
        enemy_pawn_position: str | None = None,
        castling: bool = False,
        rock_position: str | None = None,
    ):
        if en_passant:
            if not self.board.check_if_en_passant_is_possible(
                pawn_position=origin, enemy_pawn_position=enemy_pawn_position
            ):
                raise ChessColor("En passant move is not valid")

        if castling:
            if not self.board.check_if_castling_is_possible(
                king_position=origin, rock_position=rock_position
            ):
                raise ChessException("Castling move is not valid")

        if not self.verify_if_piece_can_move_to_location(origin, destination):
            raise ChessException(f"This move is not allowed")

        piece = self.board.position_map[origin]
        new_board = self.board.copy()
        new_board.move(original_position=origin, destination_position=destination)
        if self.verify_if_king_is_in_check(king_color=piece.color, board=new_board):
            raise ChessException(
                f"This move would put the {piece.color.value.lower()} king in check"
            )

    def make_move(
        self,
        origin: str,
        destination: str,
        promotion_class: type[Piece] = Queen,
        en_passant: bool = False,
        enemy_pawn_position: str | None = None,
        castling: bool = False,
        rock_position: str | None = None,
    ):
        self.validate_move(
            origin,
            destination,
            en_passant,
            enemy_pawn_position,
            castling,
            rock_position,
        )
        piece, _ = self.board.move(
            original_position=origin,
            destination_position=destination,
            promotion_class=promotion_class,
        )

        if isinstance(piece, King):
            self.kings_position[piece.color] = str(piece.current_position)

        if self.verify_check_mate(king_color=opponent_color[piece.color]):
            self.winning_player = piece.color

        return piece
