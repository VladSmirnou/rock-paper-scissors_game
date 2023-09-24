import sys

from typing import Optional, Never

from .descriptors import (
    UserWantsToDelete,
    UserWantsToGoBackToMainMenu,
    UserWantsToLoad,
    UserWantsToListSavedGames,
    UserSetMaxRounds,
    UserWantsToDisplayGameRules
)
from ..model.model import game_cache, dbms, Cache, DBMS
from ..model.custom_dtypes import SavedGames
from ..view.view import message_renderer, panel_renderer, Message, Panel


def quit_game() -> Never:
    """Print game stats,
    close the DB connection and quit the game.
    """
    print(message_renderer.render_exit_message(
        game_cache.game_stats
    ))
    dbms.close_db_connection()
    sys.exit()


def get_invalid_user_input_message(user_input: str) -> str:
    """Return a generic error message."""
    return message_renderer.render_generic_error_message(user_input)


class UserState:
    """Represent the user's state during the game process.

    This class contains a bunch of descriptor objects
    that are shared amongst the game controllers.
    All the property methods of this class set or return
    a state of their corresponding attributes.
    """

    _user_wants_to_delete = UserWantsToDelete()
    _user_wants_to_go_back_to_main_menu = UserWantsToGoBackToMainMenu()
    _user_wants_to_load = UserWantsToLoad()
    _user_wants_to_list_saved_games = UserWantsToListSavedGames()
    _user_wants_to_display_game_rules = UserWantsToDisplayGameRules()
    _user_set_max_rounds = UserSetMaxRounds()

    @property
    def user_wants_to_delete(self) -> bool:
        """See the class docs."""
        return self._user_wants_to_delete

    @property
    def user_wants_to_go_back_to_main_menu(self) -> bool:
        """See the class docs."""
        return self._user_wants_to_go_back_to_main_menu

    @user_wants_to_go_back_to_main_menu.setter
    def user_wants_to_go_back_to_main_menu(self, value: bool) -> None:
        self._user_wants_to_go_back_to_main_menu = value

    @property
    def user_wants_to_load(self) -> bool:
        """See the class docs."""
        return self._user_wants_to_load

    @property
    def user_wants_to_list_saved_games(self) -> bool:
        """See the class docs."""
        return self._user_wants_to_list_saved_games

    @property
    def user_wants_to_display_game_rules(self) -> bool:
        """See the class docs."""
        return self._user_wants_to_display_game_rules

    @property
    def user_set_max_rounds(self) -> bool:
        """See the class docs."""
        return self._user_set_max_rounds

    @user_set_max_rounds.setter
    def user_set_max_rounds(self, value: bool) -> None:
        self._user_set_max_rounds = value


class MainMenuController(UserState):
    """This class handles requests that come
    from the main menu panel.
    """

    __game_cache: Cache
    __dbms: DBMS
    __message_renderer: Message
    __panel_renderer: Panel

    def __init__(
            self, game_cache: Cache, dbms: DBMS,
            message_renderer: Message, panel_renderer: Panel) -> None:
        self.__game_cache = game_cache
        self.__dbms = dbms
        self.__message_renderer = message_renderer
        self.__panel_renderer = panel_renderer

    def get_input_panel(self) -> str:
        """Return the main menu panel."""
        if self._user_wants_to_display_game_rules:
            self._user_wants_to_display_game_rules = False
            return (
                self
                .__panel_renderer
                .render_main_menu_panel_with_game_rules()
            )
        if self._user_wants_to_list_saved_games:
            self._user_wants_to_list_saved_games = False
            saved_games: SavedGames = self.__game_cache.saved_games
            if saved_games == []:
                saved_games = self.__dbms.get_saved_games_data()
            return (
                self
                .__panel_renderer
                .render_main_menu_panel_with_saved_game_list(
                    saved_games
                )
            )
        deleted_game_id: str = self.__game_cache.deleted_game_id
        if deleted_game_id:
            self.__game_cache.clear_deleted_game_id()
            return self.__panel_renderer.render_main_menu_panel_with_game_id(
                deleted_game_id
            )
        return self.__panel_renderer.render_main_menu_panel()

    def list_saved_games(self) -> None:
        """Set the user's decision to list saved games to 'True'."""
        self._user_wants_to_list_saved_games = True

    def delete_saved_game(self) -> None:
        """Set the user's decision to delete a saved game to 'True'."""
        self._user_wants_to_delete = True

    def load_saved_game(self) -> None:
        """Set the user's decision to load a saved game to 'True'."""
        self._user_wants_to_load = True

    def display_game_rules(self) -> None:
        """Set the user's decision to display the game rules to 'True'."""
        self._user_wants_to_display_game_rules = True

    def start_new_game(self) -> None:
        """Start a new game."""
        # If the user wants to start a new game,
        # then I don't have to do anything.
        return

    def quit_game_from_main_menu(self) -> Never:
        """Close the DB connection and quit the game from the main menu."""
        print(self.__message_renderer.render_main_menu_exit_message())
        self.__dbms.close_db_connection()
        sys.exit()


class GameIdInputPanelController(UserState):
    """This class handles requests that come
    from the game id input panel.
    """

    __dbms: DBMS
    __message_renderer: Message
    __panel_renderer: Panel

    def __init__(self, dbms: DBMS,
                 message_renderer: Message,
                 panel_renderer: Panel) -> None:
        self.__dbms = dbms
        self.__message_renderer = message_renderer
        self.__panel_renderer = panel_renderer

    def get_input_panel(self) -> str:
        """Return the game id input panel."""
        return self.__panel_renderer.render_game_id_input_panel()

    def process_user_intentions(self, user_input: str) -> Optional[str]:
        """Load or delete a saved game from the DB according
        to the user's decision.
        """
        if self._user_wants_to_load:
            return self.initialize_load_process(user_input)
        if self._user_wants_to_delete:
            return self.initialize_delete_process(user_input)
        return None

    def quit_to_main_menu_from_game_id_input_panel(self) -> None:
        """Set the user's intent to go back to the main menu."""
        self._user_wants_to_go_back_to_main_menu = True
        # If the user was trying to load or delete a saved game but
        # wasn't able to, then he'll go back to the main menu, 
        # so I need to clear his initial decision here,
        # or I can place it in the 'main.py' file.
        self._user_wants_to_load = False
        self._user_wants_to_delete = False

    def initialize_load_process(self, user_input: str) -> Optional[str]:
        """Start the saved game session restoration process."""
        error_message: Optional[str] = self.__dbms.restore_saved_game_session(
            user_input
        )
        if error_message:
            return (
                self
                .__message_renderer
                .render_load_saved_game_error_message(
                    error_message
                )
            )
        # 'user_set_max_rounds' should be here
        # because when the user has loaded a saved game
        # he will continue to play it,
        # and he doesn't need to set this value.
        self._user_set_max_rounds = True
        self._user_wants_to_load = False
        return None

    def initialize_delete_process(self, user_input: str) -> Optional[str]:
        """Start the saved game deletion process."""
        error_message: Optional[str] = self.__dbms.delete_saved_game(
            user_input
        )
        if error_message:
            return (
                self
                .__message_renderer
                .render_delete_saved_game_error_message(
                    error_message
                )
            )
        self._user_wants_to_delete = False
        self._user_wants_to_go_back_to_main_menu = True
        return None


class IngamePanelController(UserState):
    """This class handles requests that come
    from the game id input panel.
    """

    __game_cache: Cache
    __dbms: DBMS
    __panel_renderer: Panel

    def __init__(
            self, game_cache: Cache, dbms: DBMS,
            panel_renderer: Panel) -> None:
        self.__game_cache = game_cache
        self.__dbms = dbms
        self.__panel_renderer = panel_renderer

    def get_input_panel(self) -> str:
        """Return the ingame panel."""
        saved_game_id: str = self.__game_cache.saved_game_id
        if saved_game_id:
            self.__game_cache.clear_saved_game_id()
        return self.__panel_renderer.render_game_panel(
            self.__game_cache.round_stats,
            self.__game_cache.game_stats,
            self.__game_cache.max_rounds_per_game,
            self.__game_cache.saved_games_count,
            saved_game_id,
        )

    def quit_game(self) -> Never:
        """Quit the game."""
        # This method exists because, maybe,
        # I'd want to add something controller-
        # specific before quitting the game.
        quit_game()

    def save_game(self) -> Optional[str]:
        """Save game results."""
        err: Optional[str] = self.__dbms.save_game_data()
        if err:
            return err
        return None

    def quit_to_main_menu(self) -> None:
        """Quit to the main menu."""
        self._user_set_max_rounds = False
        self._user_wants_to_go_back_to_main_menu = True
        self.__game_cache.clear_game_stats()

    def continue_default_game(self, user_input: str) -> None:
        """Continue a game session."""
        self.get_round_results(user_input)

    def get_round_results(self, user_input: str) -> None:
        """Calculate round results."""
        self.__game_cache.get_round_winner(user_input)
        self.__game_cache.check_shortcut_game_winner()


class ContinueGamePanelController(UserState):
    """This class handles requests that come
    from the continue game panel.
    """

    __panel_renderer: Panel
    __game_cache: Cache

    def __init__(self, game_cache: Cache, panel_renderer: Panel) -> None:
        self.__panel_renderer = panel_renderer
        self.__game_cache = game_cache

    def get_input_panel(self) -> str:
        """Return the continue game input panel."""
        return self.__panel_renderer.render_continue_game_input_panel(
            self.__game_cache.round_stats,
            self.__game_cache.current_game_winner
        )

    def quit_game(self) -> Never:
        """Quit the game.

        See this method purpose in the
        'IngamePanelController' class 'quit game' method.
        """
        quit_game()

    def quit_to_main_menu(self) -> None:
        """Quit to the main menu."""
        self._user_wants_to_go_back_to_main_menu = True
        self.__game_cache.clear_game_stats()

    def continue_playing(self) -> None:
        """Clear round stats.

        Round stats must be cleared
        before the user starts a new game.
        """
        self.__game_cache.clear_round_stats()

    def get_game_results(self) -> None:
        """Calculate game session results."""
        self.__game_cache.get_game_winner()

    def check_if_the_last_round(self) -> bool:
        """Return 'True' if a round is the
        last one in the current game, 'False'
        otherwise.
        """
        return (self.__game_cache.current_round ==
                self.__game_cache.max_rounds_per_game)


class RoundAmountPanelContoller(UserState):
    """This class handles requests that come
    from the round amount panel.
    """

    __game_cache: Cache
    __panel_renderer: Panel

    def __init__(
            self, game_cache: Cache,
            panel_renderer: Panel) -> None:
        self.__game_cache = game_cache
        self.__panel_renderer = panel_renderer

    def get_input_panel(self) -> str:
        """Return the round amount input panel."""
        return self.__panel_renderer.render_round_amound_input_panel()

    def quit_to_main_menu(self) -> None:
        """Quit to the main menu."""
        self._user_wants_to_go_back_to_main_menu = True
        self.__game_cache.clear_game_stats()

    def start_game(self, user_input: str) -> None:
        """Start a new game after the user picked
        the amount of rounds for one game.
        """
        numeric_user_input: int = int(user_input)
        self._user_set_max_rounds = True
        self.__game_cache.max_rounds_per_game = numeric_user_input
        self.__game_cache.set_win_condition(numeric_user_input)


user_state = UserState()

# DI is an interesting thing I ain't gonna lie, but what am I
# supposed to do with this messy object creation?

round_amount_panel_controller = RoundAmountPanelContoller(
    game_cache=game_cache,
    panel_renderer=panel_renderer
)
main_menu_panel_controller = MainMenuController(
    game_cache=game_cache,
    dbms=dbms,
    message_renderer=message_renderer,
    panel_renderer=panel_renderer
)
game_id_input_panel_controller = GameIdInputPanelController(
    dbms=dbms,
    message_renderer=message_renderer,
    panel_renderer=panel_renderer
)
ingame_panel_controller = IngamePanelController(
    game_cache=game_cache,
    dbms=dbms,
    panel_renderer=panel_renderer
)
continue_game_panel_controller = ContinueGamePanelController(
    game_cache=game_cache,
    panel_renderer=panel_renderer
)
