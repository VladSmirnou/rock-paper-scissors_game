import random
import uuid

from abc import ABC, abstractmethod
from typing import Any, Final, Optional

import psycopg2
import psycopg2.extras

from .custom_dtypes import GameId, GamesLost, GamesWon, SavedGames
from .db_config import conn, cur
from .enums import CacheChoice
from .constants import MAX_SAVED_GAMES


class Cache(ABC):

    _CHOICE: Final[list[str]] = [choice.value for choice in CacheChoice]

    @property
    @abstractmethod
    def saved_games(self) -> SavedGames:
        """Return a list of saved games."""

    @saved_games.setter
    @abstractmethod
    def saved_games(self, list_: SavedGames) -> None:
        ...

    @abstractmethod
    def clear_saved_game_id(self) -> None:
        """Reset cached game id."""

    @abstractmethod
    def clear_deleted_game_id(self) -> None:
        """Remove deleted game id from the cache."""

    @abstractmethod
    def clear_round_stats(self) -> None:
        """Reset cached round stats."""

    @abstractmethod
    def clear_game_stats(self) -> None:
        """Reset cached game stats."""

    @staticmethod
    @abstractmethod
    def get_clear_round_stats() -> dict:
        """Return the initial round stats."""

    @staticmethod
    @abstractmethod
    def get_clear_game_stats() -> dict:
        """Return the initial game stats."""

    @property
    @abstractmethod
    def saved_game_id(self) -> str:
        """Return saved game id."""

    @saved_game_id.setter
    @abstractmethod
    def saved_game_id(self, game_id: str) -> None:
        ...

    @property
    @abstractmethod
    def deleted_game_id(self) -> str:
        """Return deleted game id."""

    @deleted_game_id.setter
    @abstractmethod
    def deleted_game_id(self, game_id: str) -> None:
        ...

    @property
    @abstractmethod
    def round_stats(self) -> dict:
        """Return round stats."""

    @property
    @abstractmethod
    def game_stats(self) -> dict:
        """Return session stats."""

    @property
    @abstractmethod
    def current_round(self) -> int:
        """Return a round number."""

    @property
    @abstractmethod
    def current_game_winner(self) -> str:
        """Return the game winner."""

    @current_game_winner.setter
    @abstractmethod
    def current_game_winner(self, game_winner: str) -> None:
        ...

    @property
    @abstractmethod
    def computer_choice(self) -> str:
        """Return a computer's choise."""

    @property
    @abstractmethod
    def max_rounds_per_game(self) -> int:
        """Return a value of the '__max_rounds_per_game' attribute."""

    @max_rounds_per_game.setter
    @abstractmethod
    def max_rounds_per_game(self, number_from_user: int) -> None:
        ...

    @property
    @abstractmethod
    def saved_games_count(self) -> int:
        """Return an amount of saved games."""

    @abstractmethod
    def set_round_stats(self, data: dict) -> None:
        """Cache round stats."""

    @abstractmethod
    def set_game_stats(
            self, data: dict) -> None:
        """Cache game stats."""

    @abstractmethod
    def set_prev_round_choices(self,
                               user_input: str,
                               computer_choice: str) -> None:
        """Cache user and computer 
        choices for the previous round."""

    @abstractmethod
    def check_shortcut_game_winner(self) -> None:
        """Set the 'round' attribute equal to the maximum 
        round amount per one game when a win 
        condition is reached.
        """

    @abstractmethod
    def get_round_winner(self, user_input: str) -> None:
        """Get the round winner."""

    @abstractmethod
    def get_game_winner(self) -> None:
        """Get the game winner."""

    @abstractmethod
    def calculate_win_condition(self, number_from_user):
        """Calculate the win condition for one game."""

    @abstractmethod
    def set_win_condition(self, number_from_user: int) -> None:
        """Cache a win condition for one game."""

    @abstractmethod
    def update_saved_games_count(self) -> None:
        """Update a value of the '__saved_games_count' attribute."""

    @abstractmethod
    def set_saved_games_count(self) -> None:
        """Cache a count of saved games."""


class GameCache(Cache):
    """Store game data while the game is running."""

    __saved_game_id: str
    __deleted_game_id: str
    __current_game_winner: str
    __max_rounds_per_game: int
    __win_condition: Optional[int]
    __saved_games: SavedGames
    __saved_games_count: int
    __round_stats: dict[str, Any]
    __game_stats: dict[str, Any]

    def __init__(self) -> None:
        self.__saved_game_id = ''
        self.__deleted_game_id = ''
        self.__current_game_winner = ''
        self.__saved_games = []
        self.__saved_games_count = 0
        self.__max_rounds_per_game = 0
        self.__win_condition = None
        self.__round_stats = {
            'rounds_won': 0,
            'rounds_lost': 0,
            'total_draws': 0,
            'round': 0,
            'user_choice': '',
            'computer_choice': '',
        }
        self.__game_stats = {
            'games_won': 0,
            'games_lost': 0,
        }

    @property
    def saved_games(self) -> SavedGames:
        return self.__saved_games

    @saved_games.setter
    def saved_games(
            self, list_: SavedGames) -> None:
        self.__saved_games = list_

    def clear_saved_game_id(self) -> None:
        self.__saved_game_id = ''

    def clear_deleted_game_id(self) -> None:
        self.__deleted_game_id = ''

    def clear_round_stats(self) -> None:
        self.__round_stats = self.get_clear_round_stats()

    def clear_game_stats(self) -> None:
        self.__game_stats = self.get_clear_game_stats()
        self.__round_stats = self.get_clear_round_stats()
        self.__current_game_winner = ''

    @staticmethod
    def get_clear_round_stats() -> dict:
        return {
            'rounds_won': 0,
            'rounds_lost': 0, 
            'total_draws': 0,
            'round': 0,
            'user_choice': '',
            'computer_choice': '',
        }

    @staticmethod
    def get_clear_game_stats() -> dict:
        return {
            'games_won': 0,
            'games_lost': 0,
        }

    @property
    def saved_game_id(self) -> str:
        return self.__saved_game_id

    @saved_game_id.setter
    def saved_game_id(self, game_id: str) -> None:
        self.__saved_game_id = game_id

    @property
    def deleted_game_id(self) -> str:
        return self.__deleted_game_id

    @deleted_game_id.setter
    def deleted_game_id(self, game_id: str) -> None:
        self.__deleted_game_id = game_id

    @property
    def round_stats(self) -> dict:
        return self.__round_stats

    @property
    def game_stats(self) -> dict:
        return self.__game_stats

    @property
    def current_round(self) -> int:
        return self.__round_stats['round']

    @property
    def current_game_winner(self) -> str:
        return self.__current_game_winner

    @current_game_winner.setter
    def current_game_winner(self, game_winner: str) -> None:
        self.__current_game_winner = game_winner

    @property
    def computer_choice(self) -> str:
        return random.choice(self._CHOICE)

    @property
    def max_rounds_per_game(self) -> int:
        return self.__max_rounds_per_game

    @max_rounds_per_game.setter
    def max_rounds_per_game(self, number_from_user: int) -> None:
        self.__max_rounds_per_game = number_from_user

    @property
    def saved_games_count(self) -> int:
        return self.__saved_games_count

    def set_round_stats(self, data: dict) -> None:
        self.__round_stats |= data

    def set_game_stats(self, data: dict) -> None:
        self.__game_stats['games_won'] = data['games_won']
        self.__game_stats['games_lost'] = data['games_lost']
        self.max_rounds_per_game  = data['max_rounds_per_game']
        self.set_win_condition(data['max_rounds_per_game'])

    def set_prev_round_choices(self,
                               user_input: str,
                               computer_choice: str) -> None:
        self.__round_stats['user_choice'] = user_input
        self.__round_stats['computer_choice'] = computer_choice

    def check_shortcut_game_winner(self) -> None:
        if self.__win_condition in (self.__round_stats['rounds_won'],
                                    self.__round_stats['rounds_lost']):
            self.__round_stats['round'] = self.__max_rounds_per_game

    def get_round_winner(self, user_input: str) -> None:
        computer_choice: str = self.computer_choice
        self.set_prev_round_choices(user_input, computer_choice)

        choices: tuple = (user_input, computer_choice)
        match choices:
            case choices if user_input == computer_choice:
                self.__round_stats['total_draws'] += 1
            case (
                    (CacheChoice.SCISSORS.value, CacheChoice.ROCK.value) |
                    (CacheChoice.ROCK.value, CacheChoice.PAPER.value) |
                    (CacheChoice.PAPER.value, CacheChoice.SCISSORS.value)
                ):
                self.__round_stats['rounds_lost'] += 1
                self.__round_stats['round'] += 1
            case _:
                self.__round_stats['rounds_won'] += 1
                self.__round_stats['round'] += 1

    def get_game_winner(self) -> None:
        current_game_winner: str = ''
        if self.__round_stats['rounds_won'] == self.__win_condition:
            self.__game_stats['games_won'] += 1
            current_game_winner = 'user'
        else:
            self.__game_stats['games_lost'] += 1
            current_game_winner = 'computer'
        self.current_game_winner = current_game_winner

    def calculate_win_condition(self, number_from_user: int) -> int:
        return number_from_user // 2 + 1

    def set_win_condition(self, number_from_user: int) -> None:
        self.__win_condition = self.calculate_win_condition(number_from_user)

    def update_saved_games_count(self) -> None:
        self.__saved_games_count = len(self.__saved_games)

    def set_saved_games_count(self) -> None:
        self.__saved_games_count = dbms.get_current_saved_games_count()


class DBMS(ABC):
    """An abstract DBMS class."""

    @abstractmethod
    def close_db_connection(self) -> None:
        """Close the database connection when the
        user is exiting the game.
        """

    @abstractmethod
    def save_game_data(self) -> Optional[str]:
        """Save game data into the DB."""

    @abstractmethod
    def restore_saved_game_session(self, game_id: str) -> Optional[str]:
        """Get game data from the DB and 
        send it into the 'IngameCache' class.
        """

    @abstractmethod
    def delete_saved_game(self, game_id: str) -> Optional[str]:
        """Remove a specific saved game from the DB."""

    @abstractmethod
    def get_saved_games_data(self) -> SavedGames:
        """Return game data about saved games."""

    @abstractmethod
    def get_current_saved_games_count(self) -> int:
        "Return a number of saved games."

    @property
    @abstractmethod
    def str_uuid_value(self) -> str:
        """Return a uuid value converted to string."""


class Postgres(DBMS):
    """Provides methods to work with 
    the PostgreSQL DB via psycopg2.
    """

    def close_db_connection(self) -> None:
        cur.close()
        conn.close()

    def get_current_saved_games_count(self) -> int:
        cur.execute('SELECT count(*) FROM game_data')
        return cur.fetchone()[0]

    @property
    def str_uuid_value(self) -> str:
        return str(uuid.uuid4())

    def save_game_data(self) -> Optional[str]:
        if self.get_current_saved_games_count() >= MAX_SAVED_GAMES:
            return '\n**You have reached the max number of saved games!**'

        game_id: GameId = GameId(self.str_uuid_value)
        cur.execute(
            """INSERT INTO game_data VALUES (
                %(game_id)s, 
                %(games_won)s,
                %(games_lost)s, 
                %(max_rounds_per_game)s
            )""",
            {
                'game_id': game_id, 
                **game_cache.game_stats,
                'max_rounds_per_game': game_cache.max_rounds_per_game,
            }
        )
        cur.execute(
            """INSERT INTO round_data VALUES (
                %(game_id)s, 
                %(round)s, 
                %(rounds_lost)s, 
                %(total_draws)s, 
                %(rounds_won)s, 
                %(user_choice)s, 
                %(computer_choice)s
            )""",
            {'game_id': game_id, **game_cache.round_stats}
        )
        conn.commit()

        game_cache.saved_game_id = game_id
        game_cache.saved_games.append(
            (
                game_id,
                GamesLost(game_cache.game_stats['games_lost']),
                GamesWon(game_cache.game_stats['games_won'])
            )
        )
        game_cache.update_saved_games_count()
        return None

    def restore_saved_game_session(self, game_id: str) -> Optional[str]:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                WITH t AS (
                    SELECT 
                        game_id, 
                        games_won, 
                        games_lost,
                        max_rounds_per_game
                    FROM game_data 
                    WHERE game_id = %s
                )
                SELECT 
                    games_won, 
                    games_lost, 
                    max_rounds_per_game, 
                    round, 
                    rounds_lost, 
                    total_draws, 
                    rounds_won, 
                    user_choice, 
                    computer_choice 
                FROM 
                    t 
                JOIN 
                    round_data 
                USING(game_id)
                """, (game_id,))

            loaded_game_data: Optional[dict] = cur.fetchone()
            if not loaded_game_data:
                return f'There is no game with this game id -> {game_id}'

            game_cache.set_game_stats(
                dict(list(loaded_game_data.items())[:3])
            )

            game_cache.set_round_stats(
                dict(list(loaded_game_data.items())[3:])
            )

        return None

    def delete_saved_game(self, game_id: str) -> Optional[str]:
        cur.execute(
            'SELECT game_id FROM game_data WHERE game_id = %s', (game_id,)
        )

        if not cur.fetchone():
            return f'There is no game with this game id -> {game_id}'

        cur.execute(
            'DELETE FROM game_data WHERE game_id = %s', (game_id,)
        )

        conn.commit()

        game_cache.deleted_game_id = game_id
        game_cache.saved_games.remove(
            [tuple_ for tuple_ in game_cache.saved_games
             if tuple_[0] == game_id][0]
        )
        game_cache.update_saved_games_count()
        return None

    def get_saved_games_data(self) -> SavedGames:
        cur.execute('SELECT game_id, games_won, games_lost FROM game_data')
        data: list = cur.fetchall()
        game_cache.saved_games = SavedGames(data)
        return SavedGames(data)


game_cache: Cache = GameCache()
dbms: DBMS = Postgres()

game_cache.set_saved_games_count()
