from abc import ABC, abstractmethod
from .enums import GameIdMessage as GIM
from ..model.custom_dtypes import SavedGames


class Panel(ABC):
    """An interface.
    
    It doesn't share any code and only contains 
    abstract methods.
    """

    @abstractmethod
    def render_game_panel(self,
                          round_stats: dict,
                          game_stats: dict,
                          max_rounds_per_game: int,
                          saved_games_count: int,
                          saved_game_id: str) -> str:
        """Return the ingame input panel."""

    @abstractmethod
    def render_continue_game_input_panel(
            self, round_stats: dict, current_game_winner: str) -> str:
        """Return the continue game input pannel."""

    @abstractmethod
    def render_main_menu_panel_with_saved_game_list(
            self, saved_games: SavedGames) -> str:
        """Return the main menu panel with the injected saved game list."""

    @abstractmethod
    def render_main_menu_panel_with_game_rules(self) -> str:
        """Return the main menu panel with the injected game rules."""

    @abstractmethod
    def render_main_menu_panel(self) -> str:
        """Return the main menu panel."""

    @abstractmethod
    def render_main_menu_panel_with_game_id(self, deleted_game_id: str) -> str:
        """Return the main menu panel with the injected game id."""

    @abstractmethod
    def render_game_id_input_panel(self) -> str:
        """Return the game id input panel."""

    @abstractmethod
    def render_round_amound_input_panel(self) -> str:
        """Return the round amount input panel."""


class MainGamePanel(Panel):
    """A subclass of the 'Panel' class.

    It provides methods to render the game panels.
    """

    __main_menu_base_panel: str

    def __init__(self) -> None:
        self.__main_menu_base_panel = (
            '\nWelcome to the main menu!'
            '\nPick an option (number) and type it below:'
            '\n1) Start a new game'
            '\n2) Load a game (you need to provide the game id)'
            '\n3) Delete a game (you need to provide the game id)'
            '\n4) List all saved games'
            '\n5) Display the game rules'
            '\n6) Quit the game'
            '\nType here: '
        )

    def render_game_panel(self,
                          round_stats: dict,
                          game_stats: dict,
                          max_rounds_per_game: int,
                          saved_games_count: int,
                          saved_game_id: str) -> str:
        base_panel = (
            f'\nGame stats: won {game_stats["games_won"]}, '
            f'lost {game_stats["games_lost"]}'
            f'\nRound: {round_stats["round"]}/{max_rounds_per_game}'
            '\nRound stats:'
            f'\nYour choice: '
            f'[ {round_stats["user_choice"] or "Not set yet!"} ], '
            'PC choice: '
            f'[ {round_stats["computer_choice"] or "Not set yet!"} ]'
            f'\nRounds won: {round_stats["rounds_won"]}, '
            f'Rounds lost: {round_stats["rounds_lost"]}, '
            f'Total draws: {round_stats["total_draws"]}'
            '\nType ->'
            '\n"r"(ock), "p"(aper), "s"(cissors),'
            '\n"q"(uit the game), "qm"(uit to the main menu, '
            'also clears the game stats),'
            '\n"S"(ave the game; you can save at most 5 games), '
            f'the number of currently saved games -> {saved_games_count}/5'
            '\nType here: '
        )
        if not saved_game_id:
            return base_panel
        return message_renderer.inject_game_id_related_dynamic_message(
            base_panel,
            GIM.GAME_SAVED.value,
            saved_game_id
        )

    def render_continue_game_input_panel(
            self, round_stats: dict, current_game_winner: str) -> str:
        return (
            f'\nYour choice: [ {round_stats["user_choice"]} ], '
            f'PC choice: [ {round_stats["computer_choice"]} ]'
            f'\nRounds won: {round_stats["rounds_won"]}, '
            f'Rounds lost: {round_stats["rounds_lost"]}, '
            f'Total draws: {round_stats["total_draws"]}'
            f'\n[ {current_game_winner.upper()} ] has won!'
            '\nWanna play again?'
            '\nIf yes, then type -> "y", else -> "qm"(uit to the main '
            'menu, also clears the game stats) or "q"(uit the game): '
        )

    def render_main_menu_panel_with_saved_game_list(
            self, saved_games: SavedGames) -> str:
        return message_renderer.inject_saved_games_list(
            self.__main_menu_base_panel,
            saved_games
        )

    def render_main_menu_panel_with_game_rules(self) -> str:
        return message_renderer.inject_game_rules(
            self.__main_menu_base_panel
        )

    def render_main_menu_panel(self) -> str:
        return self.__main_menu_base_panel

    def render_main_menu_panel_with_game_id(self, deleted_game_id: str) -> str:
        return message_renderer.inject_game_id_related_dynamic_message(
            self.__main_menu_base_panel,
            GIM.GAME_DELETED.value,
            deleted_game_id
        )

    def render_game_id_input_panel(self) -> str:
        return ('\nEnter the game id here '
                '(type "qm" to go back to the main menu): ')

    def render_round_amound_input_panel(self) -> str:
        return ('\nType the number of rounds (3, 5, 7 or 9) '
                'that you wanna set for one game'
                '\nor type "qm" to go back to the main menu.'
                '\nType here: ')


class Message(ABC):
    """An abstract message class.

    It doesn't share any code and only contains 
    abstract methods.
    """

    @abstractmethod
    def render_generic_error_message(self, invalid_input: str) -> str:
        """Return a generic error message."""

    @abstractmethod
    def render_exit_message(self, game_stats: dict[str, int]) -> str:
        """Return the exit game message."""

    @abstractmethod
    def render_main_menu_exit_message(self) -> str:
        """Return the main menu exit message."""

    @abstractmethod
    def render_invalid_game_id_message(self) -> str:
        """Return the invalid game id message."""

    @abstractmethod
    def render_delete_saved_game_error_message(
            self, error_message: str) -> str:
        """Return the error message for deleting a saved game."""

    @abstractmethod
    def render_load_saved_game_error_message(
            self, error_message: str) -> str:
        """Return the error message for loading a saved game."""

    @abstractmethod
    def inject_saved_games_list(
            self, base_pannel: str,
            saved_games: SavedGames) -> str:
        """Inject a list of saved games if it is not empty."""

    @abstractmethod
    def inject_game_id_related_dynamic_message(
            self, base_pannel: str,
            message: str, game_id: str) -> str:
        """Inject a game id related message into the base panels."""

    @abstractmethod
    def inject_game_rules(self, base_pannel: str) -> str:
        """Inject the game rules into the main menu base panel."""


class GameMessage(Message):
    """A subclass of the 'Message' class.

    It provides methods to render different messages and, when
    necessary, inject them into the game menu panels.
    """

    __game_id_related_dynamic_messages: dict[str, str]
    __game_rules: str

    def __init__(self) -> None:
        self.__game_id_related_dynamic_messages = {
            GIM.GAME_SAVED.value: (
                '\n**The game saved successfully! Here is the game id**: %s\n'
            ),
            GIM.GAME_DELETED.value: (
                '\n**The game with the game id -> %s was deleted!**\n'
            )
        }
        self.__game_rules = (
            '\nFirst, you need to select '
            'the "best of [ your choice ]" amount '
            'of rounds per game.'
            '\nA round counter will be incremented by 1 '
            'when you win or lose in the current round. '
            '\nIf it is a draw, then the round '
            'counter won\'t be incremented.'
            '\nBecause it is the "best of [ your choice ]", '
            'either you or the computer wins when '
            '\na "win condition" is reached. For example, '
            'in a 5-round game, it cound be -> '
            '3/0-2 etc.\n'
        )

    def render_generic_error_message(self, invalid_input: str) -> str:
        return f'\nThis input -> [ {invalid_input} ] is invalid, try again!'

    def render_exit_message(self, game_stats: dict[str, int]) -> str:
        return (
            f'\nYou have finished the game. Here are your final stats: '
            f'\nWon: {game_stats["games_won"]}'
            f'\nLost: {game_stats["games_lost"]}'
        )

    def render_main_menu_exit_message(self) -> str:
        return '\nGood bye!'

    def render_invalid_game_id_message(self) -> str:
        return '\nThis game id in invalid, try again!'

    def render_delete_saved_game_error_message(
            self, error_message: str) -> str:
        return f'\n{error_message}'

    def render_load_saved_game_error_message(
            self, error_message: str) -> str:
        return f'\n{error_message}'

    def inject_saved_games_list(
            self, base_pannel: str,
            saved_games: SavedGames) -> str:
        if not saved_games:
            return '\n**You don\'t have any saved games yet!**\n' + base_pannel
        formatted_games = '\n'.join(
            [f'{idx}) [ {tuple_[0]} ]; The game stats -> '
             f'won: {tuple_[2]} lost: {tuple_[1]}' 
             for idx, tuple_ in enumerate(saved_games, 1)]
        )
        return (
            '\nYour saved game ids:'
            f'\n{formatted_games}\n{base_pannel}'
        )

    def inject_game_id_related_dynamic_message(
            self, base_pannel: str,
            message: str, game_id: str) -> str:
        return (
            self.__game_id_related_dynamic_messages[message] % game_id
        ) + base_pannel

    def inject_game_rules(self, base_pannel: str) -> str:
        return self.__game_rules + base_pannel


panel_renderer = MainGamePanel()
message_renderer = GameMessage()
