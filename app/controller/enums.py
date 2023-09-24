from enum import Enum


class MainMenuPanelChoice(Enum):
    """Enums for the 'MainMenuController' class."""
    START_NEW_GAME = '1'
    LOAD_SAVED_GAME = '2'
    DELETE_SAVED_GAME = '3'
    LIST_SAVED_GAMES = '4'
    DISPLAY_GAME_RULES = '5'
    QUIT_GAME = '6'
