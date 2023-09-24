from enum import Enum


class GamePanel(Enum):
    """Enums for the 'MainRouter' class."""
    MAIN_MENU_PANEL = 'main_menu_panel'
    GAME_ID_INPUT_PANEL = 'game_id_input_panel'
    INGAME_PANEL = 'ingame_panel'
    CONTINUE_GAME_PANEL = 'continue_game_panel'
    ROUND_AMOUNT_PANEL = 'round_amount_panel'
