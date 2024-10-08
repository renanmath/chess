from enum import Enum
from abc import ABC, abstractmethod

from chess.models import (
    PIECE_SYMBOLS,
    ChessColor,
    LetterPosition,
    NumberPosition,
    Position,
)


class Piece(ABC):
    def __init__(self, color: ChessColor, current_position: Position) -> None:
        self.color = color
        self.current_position = current_position
        self.num_movements: int = 0

    @abstractmethod
    def get_possible_positions_to_move(self) -> list[Position]:
        ...

    def move(self, next_position: Position):
        self.current_position = next_position
        self.num_movements += 1

    @property
    def symbol(self):
        return PIECE_SYMBOLS[self.color][self.__class__.__name__]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} at {self.current_position}"


class Pawn(Piece):
    def __init__(self, color: ChessColor, current_position: Position) -> None:
        super().__init__(color, current_position)

    def get_possible_positions_to_move(self) -> list[Position]:
        if self.color == ChessColor.WHITE:
            possible_positions = [
                self.current_position.get_up_position(),
                self.current_position.get_left_up_position(),
                self.current_position.get_right_up_position(),
            ]
        else:
            possible_positions = [
                self.current_position.get_down_position(),
                self.current_position.get_left_down_position(),
                self.current_position.get_right_down_position(),
            ]

        if self.num_movements == 0:
            try:
                if self.color == ChessColor.WHITE:
                    possible_positions.append(
                        self.current_position.get_up_position().get_up_position()
                    )
                else:
                    possible_positions.append(
                        self.current_position.get_down_position().get_down_position()
                    )
            except AttributeError:
                pass

        return [p for p in possible_positions if p is not None]


class Knight(Piece):
    def __init__(self, color: ChessColor, current_position: Position) -> None:
        super().__init__(color, current_position)

    def get_possible_positions_to_move(self) -> list[Position]:
        possible_positions: list[Position] = list()

        try:
            possible_positions.append(
                self.current_position.get_right_up_position().get_up_position()
            )
        except AttributeError:
            pass

        try:
            possible_positions.append(
                self.current_position.get_right_up_position().get_right_position()
            )
        except AttributeError:
            pass

        try:
            possible_positions.append(
                self.current_position.get_right_down_position().get_down_position()
            )
        except AttributeError:
            pass

        try:
            possible_positions.append(
                self.current_position.get_right_down_position().get_right_position()
            )
        except AttributeError:
            pass

        try:
            possible_positions.append(
                self.current_position.get_left_up_position().get_up_position()
            )
        except AttributeError:
            pass

        try:
            possible_positions.append(
                self.current_position.get_left_up_position().get_left_position()
            )
        except AttributeError:
            pass

        try:
            possible_positions.append(
                self.current_position.get_left_down_position().get_down_position()
            )
        except AttributeError:
            pass

        try:
            possible_positions.append(
                self.current_position.get_left_down_position().get_left_position()
            )
        except AttributeError:
            pass

        possible_positions = [pos for pos in possible_positions if pos is not None]
        return possible_positions


class Bishop(Piece):
    def __init__(self, color: ChessColor, current_position: Position) -> None:
        super().__init__(color, current_position)

    def get_possible_positions_to_move(self) -> list[Position]:
        return list(get_first_diagonal(self.current_position)) + list(
            get_second_diagonal(self.current_position)
        )


class Rock(Piece):
    def __init__(self, color: ChessColor, current_position: Position) -> None:
        super().__init__(color, current_position)

    def get_possible_positions_to_move(self) -> list[Position]:
        return list(get_column(self.current_position)) + list(
            get_row(self.current_position)
        )


class Queen(Piece):
    def __init__(self, color: ChessColor, current_position: Position) -> None:
        super().__init__(color, current_position)

    def get_possible_positions_to_move(self) -> list[Position]:
        return (
            list(get_column(self.current_position))
            + list(get_row(self.current_position))
            + list(get_first_diagonal(self.current_position))
            + list(get_second_diagonal(self.current_position))
        )


class King(Piece):
    def __init__(self, color: ChessColor, current_position: Position) -> None:
        super().__init__(color, current_position)

    def get_possible_positions_to_move(self) -> list[Position]:
        possible_positions = [
            self.current_position.get_up_position(),
            self.current_position.get_down_position(),
            self.current_position.get_left_position(),
            self.current_position.get_right_position(),
            self.current_position.get_right_up_position(),
            self.current_position.get_right_down_position(),
            self.current_position.get_left_up_position(),
            self.current_position.get_left_down_position(),
        ]

        possible_positions = [pos for pos in possible_positions if pos is not None]
        return possible_positions


def get_column(current_position: Position):
    position = current_position
    while True:
        position = position.get_up_position()
        if position is not None:
            yield position
        else:
            break

    position = current_position
    while True:
        position = position.get_down_position()
        if position is not None:
            yield position
        else:
            break


def get_row(current_position: Position):
    position = current_position
    while True:
        position = position.get_left_position()
        if position is not None:
            yield position
        else:
            break

    position = current_position
    while True:
        position = position.get_right_position()
        if position is not None:
            yield position
        else:
            break


def get_first_diagonal(current_position: Position):
    position = current_position
    while True:
        position = position.get_left_up_position()
        if position is not None:
            yield position
        else:
            break

    position = current_position
    while True:
        position = position.get_right_down_position()
        if position is not None:
            yield position
        else:
            break


def get_second_diagonal(current_position: Position):
    position = current_position
    while True:
        position = position.get_left_down_position()
        if position is not None:
            yield position
        else:
            break

    position = current_position
    while True:
        position = position.get_right_up_position()
        if position is not None:
            yield position
        else:
            break
