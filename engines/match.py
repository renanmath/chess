import time
from chess.game import Game
from chess.models import ChessColor, ChessException
from engines.engine import Engine, ManualEngine


def play_match(
    game: Game,
    white_engine: Engine,
    black_engine: Engine,
    display: bool = False,
    delay: int = 1,
):
    engines = [white_engine, black_engine]
    while True:
        if display:
            game.board.display()
            time.sleep(delay)

        engine = engines.pop(0)

        if display:
            print(f"\n{engine.player_color.name.capitalize()} player turn")

        try:
            move_params = engine.next_move()
            game.make_move(
                origin=move_params.origin,
                destination=move_params.destination,
                promotion_class=move_params.promotion_class,
                en_passant=move_params.en_passant,
                enemy_pawn_position=move_params.enemy_pawn_position,
                castling=move_params.castling,
                rock_position=move_params.rock_position,
            )
            engines.append(engine)
            if game.winning_player is not None:
                if display:
                    print(
                        f"Player {engine.player_color.name.capitalize()} win the match"
                    )
                break
        except ChessException as error:
            engines.insert(0, engine)
            if display:
                print(f"Error: {error}")

    return game


if __name__ == "__main__":
    game = Game()
    play_match(
        game=game,
        white_engine=ManualEngine(game=game, player_color=ChessColor.WHITE),
        black_engine=ManualEngine(game=game, player_color=ChessColor.BLACK),
        display=True,
        delay=0
    )
