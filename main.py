from app.controller import controller as contr
from app.router import main_router as mr
from app.router.enums import GamePanel as GP

# ---------------------------------------------------------------
# The game flow is ->
# 1) If you want to bypass a phase (while loop) you should return
# something that evaluates to 'False'.
# 2) If you return something that is 'True' (in the case of this game
# it will be an error message) then it indicates that an error 
# has occurend on the 'game server' side, and this phase is not finished yet.
# ---------------------------------------------------------------

while True:

    while (error:= mr.main_router_obj.route_user_input(
        user_input=input(
            mr.main_router_obj.route_static_panel(GP.MAIN_MENU_PANEL.value)
        ),
        action=GP.MAIN_MENU_PANEL.value  # This is like the 'action' attribute of an HTML form.
    )):
        print(error)

    if (contr.user_state.user_wants_to_display_game_rules
            or contr.user_state.user_wants_to_list_saved_games):
        continue

    if (contr.user_state.user_wants_to_load
            or contr.user_state.user_wants_to_delete):
        while (error:= mr.main_router_obj.route_user_input(
            user_input=input(
                mr.main_router_obj.route_static_panel(
                    GP.GAME_ID_INPUT_PANEL.value
                )
            ),
            action=GP.GAME_ID_INPUT_PANEL.value
        )):
            print(error)

        if contr.user_state.user_wants_to_go_back_to_main_menu:
            contr.user_state.user_wants_to_go_back_to_main_menu = False
            continue

    def inner_game_loop() -> None:
        """Because there is no labeled loop concept in Python
        I need to put this logic into the function body.

        # Writing those stupid dockstrings is so annoying I swear to god.
        """
        while True:

            if not contr.user_state.user_set_max_rounds:
                while (error:= mr.main_router_obj.route_user_input(
                    user_input=input(
                        mr.main_router_obj.route_static_panel(
                            GP.ROUND_AMOUNT_PANEL.value
                        )
                    ),
                    action=GP.ROUND_AMOUNT_PANEL.value
                )):
                    print(error)
                if contr.user_state.user_wants_to_go_back_to_main_menu:
                    contr.user_state.user_set_max_rounds = False
                    contr.user_state.user_wants_to_go_back_to_main_menu = False
                    return

            while (error:= mr.main_router_obj.route_user_input(
                user_input=input(
                    mr.main_router_obj.route_static_panel(
                        GP.INGAME_PANEL.value
                    )
                ),
                action=GP.INGAME_PANEL.value
            )):
                print(error)
            if contr.user_state.user_wants_to_go_back_to_main_menu:
                contr.user_state.user_wants_to_go_back_to_main_menu = False
                return

            if contr.continue_game_panel_controller.check_if_the_last_round():
                contr.user_state.user_set_max_rounds = False
                contr.continue_game_panel_controller.get_game_results()
                while (error:= mr.main_router_obj.route_user_input(
                    user_input=input(
                        mr.main_router_obj.route_static_panel(
                            GP.CONTINUE_GAME_PANEL.value
                        )
                    ),
                    action=GP.CONTINUE_GAME_PANEL.value,
                )):
                    print(error)
                if contr.user_state.user_wants_to_go_back_to_main_menu:
                    contr.user_state.user_wants_to_go_back_to_main_menu = False
                    return

    inner_game_loop()
