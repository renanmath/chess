from abc import ABC, abstractmethod
from pydantic.dataclasses import dataclass

from chess.game import Game
from chess.interface import GameInterface
from chess.models import ChessColor, ChessException
from chess.pieces import Piece


@dataclass
class MoveParameters:
    origin: str
    destination: str
    promotion_class: type[Piece] | None = None
    en_passant: bool = False
    enemy_pawn_position: str | None = None
    castling: bool = False
    rock_position: str | None = None


class Engine(ABC):
    def __init__(self, game: Game, player_color: ChessColor) -> None:
        self.game = game
        self.player_color = player_color

    @abstractmethod
    def next_move(self) -> MoveParameters:
        ...


class ManualEngine(Engine):
    def __init__(self, game: Game, player_color: ChessColor):
        super().__init__(game, player_color)
        self.interface = GameInterface(self.game)

    def next_move(self):
        notation = input(f"Type your move in algebraic notation: ")

        (
            origin,
            destination,
            promotion_class,
            en_passant,
            enemy_pawn_position,
            castling,
            rock_position,
        ) = self.interface.get_move_info_from_algebraic_notation(
            notation, self.player_color
        )

        move = MoveParameters(
            origin=origin,
            destination=destination,
            promotion_class=promotion_class,
            en_passant=en_passant,
            enemy_pawn_position=enemy_pawn_position,
            castling=castling,
            rock_position=rock_position,
        )

        return move
