from typing import final


@final
class UserWantsToLoad:
    """Shares a state of the '_user_wants_to_load' 
    attribute amongst the game controllers.
    """

    __user_wants_to_load: bool

    def __init__(self):
        self.__user_wants_to_load = False

    def __get__(self, instance, owner=None) -> bool:
        return self.__user_wants_to_load

    def __set__(self, instance, value: bool) -> None:
        self.__user_wants_to_load = value


@final
class UserWantsToDelete:
    """Shares a state of the '_user_wants_to_delete' 
    attribute amongst the game controllers.
    """

    __user_wants_to_delete: bool

    def __init__(self):
        self.__user_wants_to_delete = False

    def __get__(self, instance, owner=None) -> bool:
        return self.__user_wants_to_delete

    def __set__(self, instance, value: bool) -> None:
        self.__user_wants_to_delete = value


@final
class UserWantsToGoBackToMainMenu:
    """Shares a state of the 
    '_user_wants_to_go_back_to_main_menu' attribute
    amongst the game controllers.
    """

    __user_wants_to_go_back_to_main_menu: bool

    def __init__(self):
        self.__user_wants_to_go_back_to_main_menu = False

    def __get__(self, instance, owner=None) -> bool:
        return self.__user_wants_to_go_back_to_main_menu

    def __set__(self, instance, value: bool) -> None:
        self.__user_wants_to_go_back_to_main_menu = value


@final
class UserWantsToListSavedGames:
    """Shares a state of the 
    '_user_wants_to_list_saved_games' attribute
    amongst the game controllers.
    """

    __user_wants_to_list_saved_games: bool

    def __init__(self):
        self.__user_wants_to_list_saved_games = False

    def __get__(self, instance, owner=None) -> bool:
        return self.__user_wants_to_list_saved_games

    def __set__(self, instance, value: bool) -> None:
        self.__user_wants_to_list_saved_games = value


@final
class UserSetMaxRounds:
    """Shares a state of the 
    '_user_set_max_rounds' attribute amongst 
    the game controllers.
    """

    __user_set_max_rounds: bool

    def __init__(self):
        self.__user_set_max_rounds = False

    def __get__(self, instance, owner=None) -> bool:
        return self.__user_set_max_rounds

    def __set__(self, instance, value: bool) -> None:
        self.__user_set_max_rounds = value


@final
class UserWantsToDisplayGameRules:
    """Shares a state of the 
    '_user_wants_to_display_game_rules'
    attribute amongst the game controllers.
    """

    __user_wants_to_display_game_rules: bool

    def __init__(self):
        self.__user_wants_to_display_game_rules = False

    def __get__(self, instance, owner=None) -> bool:
        return self.__user_wants_to_display_game_rules

    def __set__(self, instance, value: bool) -> None:
        self.__user_wants_to_display_game_rules = value
