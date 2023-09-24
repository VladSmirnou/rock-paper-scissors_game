import re

from abc import ABC, abstractmethod
from typing import Optional, Callable

from ..controller.controller import (
    continue_game_panel_controller,
    game_id_input_panel_controller,
    ingame_panel_controller,
    main_menu_panel_controller,
    get_invalid_user_input_message,
    round_amount_panel_controller
)
from ..controller.constants import (
    QUIT_TO_MAIN_MENU,
    QUIT_GAME,
    SAVE_GAME,
    YES
)
from ..controller.enums import (
    MainMenuPanelChoice
)
from ..controller.regex_patterns import (
    MAX_ROUNDS_PER_GAME,
    ROCK_PAPER_SCISSORS,
    UUID_
)
from .custom_dtypes import PathOptions
from .enums import GamePanel as GP


class ControllerRouter(ABC):
    """An abstract class that provides a common 
    functionality for all of its subclasses.

    Subclasses combine input values that they must
    handle with the corresponding methods of the 
    appropriate controller in a list of tuples.
    """

    @property
    @abstractmethod
    def path_options(self) -> PathOptions:
        """Return path options."""

    def route_user_input(self, user_input: str) -> Optional[str]:
        """Route the user's input to the appropriate method of the controller."""
        for input_option, logic in self.path_options:
            if re.fullmatch(input_option, user_input):
                # I use 'try-except' because I don't wanna
                # add 'if user_input...' in particular
                # methods of the controller classes.
                try:
                    return logic(user_input)
                except TypeError:
                    return logic()
        return get_invalid_user_input_message(user_input)


class MainMenuPanelRouter(ControllerRouter):
    """A subclass of the 'ControllerRouter' class.

    To access the documentation, please refer to the superclass.
    """

    __path_options: PathOptions

    def __init__(self):
        self.__path_options = [
            (
                MainMenuPanelChoice.START_NEW_GAME.value,
                main_menu_panel_controller.start_new_game
            ),
            (
                MainMenuPanelChoice.LOAD_SAVED_GAME.value,
                main_menu_panel_controller.load_saved_game
            ),
            (
                MainMenuPanelChoice.DELETE_SAVED_GAME.value,
                main_menu_panel_controller.delete_saved_game
            ),
            (
                MainMenuPanelChoice.LIST_SAVED_GAMES.value,
                main_menu_panel_controller.list_saved_games
            ),
            (
                MainMenuPanelChoice.DISPLAY_GAME_RULES.value,
                main_menu_panel_controller.display_game_rules
            ),
            (
                MainMenuPanelChoice.QUIT_GAME.value,
                main_menu_panel_controller.quit_game_from_main_menu
            ),
        ]

    @property
    def path_options(self) -> PathOptions:
        return self.__path_options


class GameIdInputPanelRouter(ControllerRouter):
    """A subclass of the 'ControllerRouter' class.

    To access the documentation, please refer to the superclass.
    """

    __path_options: PathOptions

    def __init__(self):
        self.__path_options = [
            (
                QUIT_TO_MAIN_MENU,
                game_id_input_panel_controller
                .quit_to_main_menu_from_game_id_input_panel
            ),
            (
                UUID_,
                game_id_input_panel_controller.process_user_intentions
            ),
        ]

    @property
    def path_options(self) -> PathOptions:
        return self.__path_options


class IngamePanelRouter(ControllerRouter):
    """A subclass of the 'ControllerRouter' class.

    To access the documentation, please refer to the superclass.
    """

    __path_options: PathOptions

    def __init__(self):
        self.__path_options = [
            (
                QUIT_GAME,
                ingame_panel_controller.quit_game
            ),
            (
                SAVE_GAME,
                ingame_panel_controller.save_game
            ),
            (
                QUIT_TO_MAIN_MENU,
                ingame_panel_controller.quit_to_main_menu
            ),
            (
                ROCK_PAPER_SCISSORS,
                ingame_panel_controller.continue_default_game
            ),
        ]

    @property
    def path_options(self) -> PathOptions:
        return self.__path_options


class ContinueGamePanelRoute(ControllerRouter):
    """A subclass of the 'ControllerRouter' class.

    To access the documentation, please refer to the superclass.
    """

    __path_options: PathOptions

    def __init__(self):
        self.__path_options = [
            (
                QUIT_GAME,
                continue_game_panel_controller.quit_game
            ),
            (
                QUIT_TO_MAIN_MENU,
                continue_game_panel_controller.quit_to_main_menu
            ),
            (
                YES,
                continue_game_panel_controller.continue_playing
            ),
        ]

    @property
    def path_options(self) -> PathOptions:
        return self.__path_options


class RoundAmountPanelRouter(ControllerRouter):
    """A subclass of the 'ControllerRouter' class.

    To access the documentation, please refer to the superclass.
    """

    __path_options: PathOptions

    def __init__(self):
        self.__path_options = [
            (
                QUIT_TO_MAIN_MENU,
                round_amount_panel_controller.quit_to_main_menu
            ),
            (
                MAX_ROUNDS_PER_GAME,
                round_amount_panel_controller.start_game
            ),
        ]

    @property
    def path_options(self) -> PathOptions:
        return self.__path_options


class StaticPanelRouter:
    """Provide static game panels.

    This class is not a subclass of the 'ControllerRouter' 
    abstract class because it behaves differently.
    It provides the menu panel according to the user's 
    position in the game.
    It maps (not combines) the menu panel names with the 
    corresponding methods of the appropriate controller.
    """

    __path_options: dict[str, Callable[[], str]]

    def __init__(self):
        self.__path_options = {
                GP.ROUND_AMOUNT_PANEL.value:
                round_amount_panel_controller.get_input_panel
            ,
                GP.INGAME_PANEL.value:
                ingame_panel_controller.get_input_panel
            ,
                GP.CONTINUE_GAME_PANEL.value:
                continue_game_panel_controller.get_input_panel
            ,
                GP.GAME_ID_INPUT_PANEL.value:
                game_id_input_panel_controller.get_input_panel
            ,
                GP.MAIN_MENU_PANEL.value:
                main_menu_panel_controller.get_input_panel
            ,
        }

    def return_default_panel(self, requested_panel: str) -> str:
        """Return the requested game panel."""
        return self.__path_options[requested_panel]()


main_menu_panel_router = MainMenuPanelRouter()
game_id_input_panel_router = GameIdInputPanelRouter()
ingame_panel_router = IngamePanelRouter()
continue_game_panel_router = ContinueGamePanelRoute()
round_amount_panel_router = RoundAmountPanelRouter()
static_panel_router = StaticPanelRouter()
