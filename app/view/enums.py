from enum import Enum


class GameIdMessage(Enum):
    """Enums for the classes that are 
    in the 'view.view.py' module.
    """
    GAME_SAVED = 'game_saved'
    GAME_DELETED = 'game_deleted'
