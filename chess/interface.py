from chess.game import Game
from chess.models import ChessColor, ChessException, name_2_position
from chess.pieces import Bishop, King, Knight, Pawn, Queen, Rock

PIECES_CHARS = {"p": Pawn, "B": Bishop, "N": Knight, "R": Rock, "Q": Queen, "K": King}
CHAR_INDEXES = {c: index + 1 for index, c in enumerate("abcdefgh")}


class GameInterface:
    def __init__(self, game: Game) -> None:
        self.game = game

    def get_castling_info_from_algebraic_notation(
        self, alg_notation: str, player_color: ChessColor
    ):
        if len(alg_notation) > 3:
            # Queen side castling
            return (
                ("e1", "c1", None, False, None, True, "a1")
                if player_color == ChessColor.WHITE
                else ("e8", "c8", None, False, None, True, "a8")
            )
        else:
            # King side castling
            return (
                ("e1", "g1", None, False, None, True, "h1")
                if player_color == ChessColor.WHITE
                else ("e8", "g8", None, False, None, True, "h8")
            )

    def get_en_passant_info_from_algebraic_notation(
        self, alg_notation: str, player_color: ChessColor
    ):
        destination_position = name_2_position(alg_notation.split("x")[1][:2])
        possible_origins = [
            str(destination_position.get_left_up_position()),
            str(destination_position.get_right_up_position()),
            str(destination_position.get_left_down_position()),
            str(destination_position.get_right_down_position()),
        ]
        possible_pieces = [
            self.game.board.position_map.get(p, None) for p in possible_origins
        ]
        possible_pieces = [
            piece
            for piece in possible_pieces
            if piece is not None
            and isinstance(piece, Pawn)
            and piece.color == player_color
        ]
        enemy_pawn_position = (
            destination_position.get_down_position()
            if player_color == ChessColor.WHITE
            else destination_position.get_up_position()
        )
        if not possible_pieces:
            raise ChessException("En passant move is not valid")

        elif len(possible_pieces) > 1:
            prefix = alg_notation.split("x")[0]
            if prefix[0] == "p":
                prefix = prefix[1:]
            if len(prefix) == 2:
                return (
                    prefix,
                    str(destination_position),
                    None,
                    True,
                    str(enemy_pawn_position),
                    False,
                    None,
                )
            elif len(prefix) == 1:
                try:
                    y = int(prefix)
                    piece = next(
                        (
                            pc
                            for pc in possible_pieces
                            if pc.current_position.coordinates[1] == y
                        ),
                        None,
                    )
                    if piece is None:
                        raise ChessException("En passant move is not valid")
                    return (
                        str(piece.current_position),
                        str(destination_position),
                        None,
                        True,
                        str(enemy_pawn_position),
                        False,
                        None,
                    )
                except ValueError:
                    x = CHAR_INDEXES[prefix]
                    piece = next(
                        (
                            pc
                            for pc in possible_pieces
                            if pc.current_position.coordinates[0] == x
                        ),
                        None,
                    )
                    if piece is None:
                        raise ChessException("En passant move is not valid")
                    return (
                        str(piece.current_position),
                        str(destination_position),
                        None,
                        True,
                        str(enemy_pawn_position),
                        False,
                        None,
                    )
            else:
                raise ChessException("Invalid algebraic notation")

        else:
            return (
                str(possible_pieces[0].current_position),
                str(destination_position),
                None,
                True,
                str(enemy_pawn_position),
                False,
                None,
            )

    def get_origin_and_destination_info_from_algebraic_notation(
        self, alg_notation: str, player_color: ChessColor
    ):
        if alg_notation[0] != "p" and alg_notation[0] not in PIECES_CHARS:
            alg_notation = "p" + alg_notation

        if "=" in alg_notation:
            # Pawn promotion
            char = alg_notation.split("=")[1][0]
            promotion_class = PIECES_CHARS[char]
            alg_notation = alg_notation.split("=")[0]
        else:
            promotion_class = None

        if "x" in alg_notation:
            destination = alg_notation.split("x")[1][-2:]
        else:
            destination = alg_notation[-2:]

        piece_char = alg_notation[0]
        piece_class = PIECES_CHARS[piece_char]
        destination_position = name_2_position(destination)
        possible_pieces = [
            pc
            for pc in self.game.board.pieces
            if pc.color == player_color
            and isinstance(pc, piece_class)
            and destination_position in pc.get_possible_positions_to_move()
        ]
        if not possible_pieces:
            raise ChessException(f"No piece can move to {destination}")
        elif len(possible_pieces) > 1:
            count_list = [i for i, c in enumerate(alg_notation) if c in "12345678"]
            num_count = len(count_list)
            if num_count == 1:
                col = alg_notation[1]
                x = CHAR_INDEXES[col]
                piece = next(
                    (
                        pc
                        for pc in possible_pieces
                        if pc.current_position.coordinates[0] == x
                    ),
                    None,
                )
                if piece is None:
                    raise ChessException("Position Invalid")
                return (
                    str(piece.current_position),
                    destination,
                    promotion_class,
                    False,
                    None,
                    False,
                    None,
                )

            elif num_count == 2:
                row = int(alg_notation[count_list[0]])
                col = alg_notation[count_list[0] - 1]
                if col in "abcdefgh":
                    origin = f"{col}{row}"
                    return (
                        origin,
                        destination,
                        promotion_class,
                        False,
                        None,
                        False,
                        None,
                    )
                else:
                    piece = next(
                        (
                            pc
                            for pc in possible_pieces
                            if pc.current_position.coordinates[1] == row
                        ),
                        None,
                    )
                    if piece is None:
                        raise ChessException("Invalid position of piece to move")

                    return (
                        str(piece.current_position),
                        destination,
                        promotion_class,
                        False,
                        None,
                        False,
                        None,
                    )

        else:
            piece = possible_pieces[0]
            return (
                str(piece.current_position),
                destination,
                promotion_class,
                False,
                None,
                False,
                None,
            )

    def get_move_info_from_algebraic_notation(
        self, alg_notation: str, player_color: ChessColor
    ):
        """
        origin,
        destination,
        promotion_class,
        en_passant,
        enemy_pawn_position,
        castling,
        rock_position,
        """
        # Special Moves
        # Castling
        if alg_notation.upper() in ["0-0", "0-0-0", "O-O", "O-O-O"]:
            return self.get_castling_info_from_algebraic_notation(
                alg_notation, player_color
            )
        elif "e.p" in alg_notation and "x" in alg_notation:
            # En passant capture
            return self.get_en_passant_info_from_algebraic_notation(
                alg_notation, player_color
            )
        else:
            # General case
            return self.get_origin_and_destination_info_from_algebraic_notation(
                alg_notation, player_color
            )

    def play(self):
        turns = [ChessColor.WHITE, ChessColor.BLACK]
        print("\n\nStarting New Chess Match\n")

        while True:
            self.game.board.display()
            turn = turns.pop(0)
            turns.append(turn)

            print(f"\n{turn.value.capitalize()} player turn")
            notation = input(f"Type your move in algebraic notation: ")
            if notation == "end":
                break

            try:
                (
                    origin,
                    destination,
                    promotion_class,
                    en_passant,
                    enemy_pawn_position,
                    castling,
                    rock_position,
                ) = self.get_move_info_from_algebraic_notation(notation, turn)

                self.game.make_move(
                    origin=origin,
                    destination=destination,
                    promotion_class=promotion_class,
                    en_passant=en_passant,
                    enemy_pawn_position=enemy_pawn_position,
                    castling=castling,
                    rock_position=rock_position,
                )
                # self.game.board.display()
            except ChessException as error:
                print(error)
                print("Try again")
                turns.insert(0, turn)


if __name__ == "__main__":
    game = Game()
    interface = GameInterface(game)
    interface.play()
