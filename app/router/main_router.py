from typing import Optional

from .controller_routers import (ControllerRouter, continue_game_panel_router,
                                 game_id_input_panel_router,
                                 ingame_panel_router, main_menu_panel_router,
                                 round_amount_panel_router,
                                 static_panel_router)
from .enums import GamePanel as GP


class MainRouter:
    """A main router.

    It maps game panel names with the appropriate 
    controller objects and provides methods
    to route the user's input to those objects.
    """

    __controller_routers: dict[str, ControllerRouter]

    def __init__(self):
        self.__controller_routers = {
            GP.MAIN_MENU_PANEL.value: main_menu_panel_router,
            GP.GAME_ID_INPUT_PANEL.value: game_id_input_panel_router,
            GP.INGAME_PANEL.value: ingame_panel_router,
            GP.CONTINUE_GAME_PANEL.value: continue_game_panel_router,
            GP.ROUND_AMOUNT_PANEL.value: round_amount_panel_router,
        }

    def route_user_input(self, user_input: str, action: str) -> Optional[str]:
        """Route the user's input to the appropriate controller router."""
        return self.__controller_routers[action].route_user_input(user_input)

    # I can combine this function with the function above and remove
    # the static controller, but I think that it is better to separate them.
    def route_static_panel(self, requested_panel: str) -> str:
        """Return the menu panel according to the user's request."""
        return static_panel_router.return_default_panel(requested_panel)


main_router_obj = MainRouter()
