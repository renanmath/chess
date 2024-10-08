from pydantic import NonNegativeInt, PositiveInt
from pydantic.dataclasses import dataclass
from enum import Enum


class ChessColor(Enum):
    WHITE = "white"
    BLACK = "black"


class LetterPosition(Enum):
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5
    F = 6
    G = 7
    H = 8


class NumberPosition(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8


@dataclass
class Position:
    x: LetterPosition
    y: NumberPosition

    @property
    def coordinates(self):
        return (int(self.x.value), int(self.y.value))

    @property
    def color(self):
        x, y = self.coordinates
        if x % 2 == 0:
            if y % 2 == 0:
                return ChessColor.BLACK
            else:
                return ChessColor.WHITE
        else:
            if y % 2 == 0:
                return ChessColor.WHITE
            else:
                return ChessColor.BLACK

    def get_up_position(self):
        i, j = self.coordinates
        return coordinates_2_position((i, j + 1))

    def get_down_position(self):
        i, j = self.coordinates
        return coordinates_2_position((i, j - 1))

    def get_right_position(self):
        i, j = self.coordinates
        return coordinates_2_position((i + 1, j))

    def get_left_position(self):
        i, j = self.coordinates
        return coordinates_2_position((i - 1, j))

    def get_left_position(self):
        i, j = self.coordinates
        return coordinates_2_position((i - 1, j))

    def get_left_up_position(self):
        i, j = self.coordinates
        return coordinates_2_position((i - 1, j + 1))

    def get_left_down_position(self):
        i, j = self.coordinates
        return coordinates_2_position((i - 1, j - 1))

    def get_right_up_position(self):
        i, j = self.coordinates
        return coordinates_2_position((i + 1, j + 1))

    def get_right_down_position(self):
        i, j = self.coordinates
        return coordinates_2_position((i + 1, j - 1))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position):
            return False
        return self.coordinates == other.coordinates

    def __repr__(self) -> str:
        return f"{self.x.name.lower()}{self.y.value}"

    def __hash__(self) -> NonNegativeInt:
        return hash(str(self))


def coordinates_2_position(coordinates: tuple[int, int]) -> Position | None:
    i, j = coordinates
    try:
        return Position(x=LetterPosition(i), y=NumberPosition(j))
    except ValueError:
        return None


def name_2_position(name: str) -> Position:
    x = LetterPosition[name[0].upper()]
    y = NumberPosition(int(name[1]))

    return Position(x, y)


PIECE_SYMBOLS = {
    ChessColor.WHITE: {
        "King": "♔",
        "Queen": "♕",
        "Rock": "♖",
        "Bishop": "♗",
        "Knight": "♘",
        "Pawn": "♙",
    },
    ChessColor.BLACK: {
        "King": "♚",
        "Queen": "♛",
        "Rock": "♜",
        "Bishop": "♚",
        "Knight": "♞",
        "Pawn": "♟",
    },
}


class ChessException(Exception):
    pass
