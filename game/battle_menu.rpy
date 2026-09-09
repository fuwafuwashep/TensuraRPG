# ============================================================
# BATTLE MENU
# ============================================================


default battle_menu_level = "main"
default battle_category = None
default battle_player_name = "RIMURU"


# ============================================================
# BUTTON COLORS
# ============================================================

define battle_color_fight = "#F3AAAA"
define battle_color_stomach = "#A9D6F5"
define battle_color_allies = "#B8E4B5"
define battle_color_run = "#F4E5A5"

define battle_color_cancel = "#A95F5F"

define battle_color_physical = "#D9D9D9"
define battle_color_aura = "#9B9B9B"
define battle_color_magic = "#D7C1EE"
define battle_color_skills = "#A184C4"


# ============================================================
# STATUS COLORS
# ============================================================

define battle_hp_color = "#45D884"
define battle_mp_color = "#55AEE8"
define battle_status_text_color = "#F3F3F3"
define battle_status_label_color = "#494949"


# ============================================================
# BATTLE UI ASSETS
# ============================================================

define battle_ui_user_status = "images/battle_ui/userstatus.png"
define battle_ui_enemy_status = "images/battle_ui/enemystatus.png"
define battle_ui_first_status = "images/battle_ui/firststatus.png"
define battle_ui_other_status = "images/battle_ui/otherstatus.png"
define battle_ui_button = "images/battle_ui/button.png"
define battle_ui_status_fill = "images/battle_ui/status_fill.svg"


# ============================================================
# ALLIES
# ============================================================

default battle_allies = []

# ============================================================
# Slide Assets
# ============================================================

default battle_turn_queue = []
default battle_turn_cycle = []
default battle_turn_cycle_index = 0

default battle_turn_order_shifting = False
default battle_turn_old_queue = []

define battle_turn_x_positions = [
    -22,
    -67,
    -112,
    -157,
    -202,
]

define battle_turn_y_positions = [
    -10,
    60,
    120,
    180,
    240,
]

# ============================================================
# BATTLE SPRITE POSITIONS
# ============================================================

transform battle_player_sprite_position:

    xanchor 0.5
    yanchor 1.0

    xpos 485
    ypos 770

    zoom 2.5


transform battle_enemy_sprite_position:

    xanchor 0.5
    yanchor 1.0

    xpos 1390
    ypos 650

    zoom 0.70


# ============================================================
# GENERIC COLORED METER
# ============================================================

screen battle_status_meter(
    current_value,
    maximum_value,
    meter_x,
    meter_y,
    meter_width,
    meter_height,
    meter_color
):

    $ safe_maximum = max(1, maximum_value)
    $ safe_current = max(0, min(current_value, safe_maximum))
    $ fill_width = int(float(safe_current) / float(safe_maximum) * meter_width)

    if fill_width > 0:
        $ meter_fill = Frame(
            Transform(
            battle_ui_status_fill,
            matrixcolor=TintMatrix(meter_color)
        ),
        9,
        0,
        9,
        0
        )
        
        add meter_fill:
            xpos meter_x
            ypos meter_y
            xsize fill_width
            ysize meter_height


# ============================================================
# GENERIC POINTED BUTTON
# ============================================================

screen battle_command_button(
    button_text,
    px,
    py,
    button_action,
    button_color,
    enabled=True
):

    $ button_image = Transform(
        "images/battle_ui/button.png",
        matrixcolor=TintMatrix(button_color)
    )

    $ disabled_button_image = Transform(
        "images/battle_ui/button.png",
        matrixcolor=TintMatrix(button_color),
        alpha=0.42
    )

    fixed:

        xcenter px
        ycenter py

        xsize 450
        ysize 150

        imagebutton:

            idle button_image
            hover button_image
            insensitive disabled_button_image

            focus_mask True
            sensitive enabled
            action button_action

        text button_text:

            xalign 0.5
            yalign 0.5

            xsize 260
            text_align 0.5

            size 27
            color "#171717"

# ============================================================
# TURN ORDER QUEUE LOGIC
# ============================================================

init python:

    import renpy.store as store

    def setup_battle_turn_queue(enemy_name):

        if enemy_goes_first():
            cycle = (
                [enemy_name]
                + list(store.battle_allies)
                + [store.battle_player_name]
            )

        else:
            cycle = (
                [store.battle_player_name]
                + list(store.battle_allies)
                + [enemy_name]
            )

        store.battle_turn_cycle = cycle
        store.battle_turn_cycle_index = 0

        store.battle_turn_queue = [
            cycle[i % len(cycle)]
            for i in range(5)
        ]

        store.battle_turn_old_queue = []
        store.battle_turn_order_shifting = False


    def prepare_battle_turn_shift():

        if not store.battle_turn_cycle:
            return

        store.battle_turn_old_queue = list(
            store.battle_turn_queue
        )

        store.battle_turn_cycle_index = (
            store.battle_turn_cycle_index + 1
        ) % len(store.battle_turn_cycle)

        start = store.battle_turn_cycle_index

        store.battle_turn_queue = [
            store.battle_turn_cycle[
                (start + i) % len(store.battle_turn_cycle)
            ]
            for i in range(5)
        ]

        store.battle_turn_order_shifting = True

transform turn_order_first_exit:

    xoffset 0
    alpha 1.0

    linear 0.30 xoffset -500 alpha 0.0


transform turn_order_move_up(dx, dy):

    xoffset dx
    yoffset dy

    linear 0.30 xoffset 0 yoffset 0


transform turn_order_new_appear:

    alpha 0.0
    xoffset 35
    yoffset 15

    linear 0.30 alpha 1.0 xoffset 0 yoffset 0

# ============================================================
# TURN ORDER
# ============================================================
screen battle_turn_card(character_name, first=False):

    if first:

        fixed:

            xsize 450
            ysize 150

            add battle_ui_first_status

            text str(character_name):

                xcenter 285
                ycenter 75

                xsize 245

                text_align 0.5

                size 25
                bold True

                color "#F4F4F4"

                outlines [
                    (2, "#000000AA", 0, 0)
                ]

    else:

        fixed:

            xsize 350
            ysize 100

            add battle_ui_other_status

            text str(character_name):

                xcenter 185
                ycenter 50

                xsize 270

                text_align 0.5

                size 22
                bold True

                color "#F4F4F4"

                outlines [
                    (2, "#000000AA", 0, 0)
                ]

screen battle_turn_order(enemy_name):

    fixed:

        xpos 0
        ypos 0

        xsize 450
        ysize 430


        if not battle_turn_order_shifting:

            for i, character_name in enumerate(battle_turn_queue):

                $ slot_x = battle_turn_x_positions[i]
                $ slot_y = battle_turn_y_positions[i]

                fixed:

                    xpos slot_x
                    ypos slot_y

                    if i == 0:

                        use battle_turn_card(
                            character_name,
                            True
                        )

                    else:

                        use battle_turn_card(
                            character_name,
                            False
                        )


        else:

            fixed:

                xpos battle_turn_x_positions[0]
                ypos battle_turn_y_positions[0]

                at turn_order_first_exit

                use battle_turn_card(
                    battle_turn_old_queue[0],
                    True
                )


            for old_index in range(1, 5):

                $ new_index = old_index - 1

                $ old_x = battle_turn_x_positions[old_index]
                $ old_y = battle_turn_y_positions[old_index]

                $ new_x = battle_turn_x_positions[new_index]
                $ new_y = battle_turn_y_positions[new_index]

                $ move_dx = old_x - new_x
                $ move_dy = old_y - new_y

                fixed:

                    xpos new_x
                    ypos new_y

                    at turn_order_move_up(
                        move_dx,
                        move_dy
                    )

                    if new_index == 0:

                        use battle_turn_card(
                            battle_turn_old_queue[old_index],
                            True
                        )

                    else:

                        use battle_turn_card(
                            battle_turn_old_queue[old_index],
                            False
                        )


            fixed:

                xpos battle_turn_x_positions[4]
                ypos battle_turn_y_positions[4]

                at turn_order_new_appear

                use battle_turn_card(
                    battle_turn_queue[4],
                    False
                )


# ============================================================
# PLAYER STATUS
# ============================================================

screen battle_player_status():

    fixed:

        xpos 0
        ypos 875

        xsize 600
        ysize 200

        add battle_ui_user_status

        text battle_player_name:
            xpos 165
            ypos 34
            size 29
            bold True
            color battle_status_text_color
            outlines [(2, "#000000AA", 0, 0)]

        text battle_status_text("player"):
            xpos 355
            ypos 43
            xsize 220
            text_align 1.0
            size 15
            color "#D8D8D8"
            outlines [(1, "#00000099", 0, 0)]

        text "HP":
            xpos 169
            ypos 82
            size 20
            bold True
            color battle_status_label_color

        use battle_status_meter(
            player_hp,
            player_max_hp,
            205,
            85,
            267,
            18,
            battle_hp_color
        )

        text "[player_hp]/[player_max_hp]":
            xpos 478
            ypos 82
            xsize 112
            text_align 0.5
            size 19
            bold True
            color battle_status_text_color
            outlines [(2, "#000000AA", 0, 0)]

        text "MP":
            xpos 164
            ypos 121
            size 20
            bold True
            color battle_status_label_color

        use battle_status_meter(
            player_mp,
            player_max_mp,
            201,
            123,
            267,
            18,
            battle_mp_color
        )

        text "[player_mp]/[player_max_mp]":
            xpos 478
            ypos 120
            xsize 112
            text_align 0.5
            size 19
            bold True
            color battle_status_text_color
            outlines [(2, "#000000AA", 0, 0)]


# ============================================================
# ENEMY STATUS
# ============================================================

screen battle_enemy_status(
    enemy_name,
    enemy_hp,
    enemy_max_hp,
    enemy_mp=100,
    enemy_max_mp=100
):

    fixed:

        xpos 1320
        ypos 0

        xsize 600
        ysize 200

        add battle_ui_enemy_status

        text enemy_name:
            xpos 118
            ypos 34
            xsize 300
            size 29
            bold True
            color battle_status_text_color
            outlines [(2, "#000000AA", 0, 0)]

        text battle_status_text("enemy"):
            xpos 118
            ypos 61
            xsize 275
            size 15
            color "#D8D8D8"
            outlines [(1, "#00000099", 0, 0)]

        use battle_status_meter(
            enemy_hp,
            enemy_max_hp,
            126,
            83,
            279,
            18,
            battle_hp_color
        )

        text "HP":
            xpos 414
            ypos 82
            size 20
            bold True
            color battle_status_label_color

        use battle_status_meter(
            enemy_mp,
            enemy_max_mp,
            126,
            121,
            280,
            18,
            battle_mp_color
        )

        text "MP":
            xpos 414
            ypos 121
            size 20
            bold True
            color battle_status_label_color


# ============================================================
# MAIN BATTLE SCREEN
# ============================================================

screen battle_command_menu(
    enemy_name,
    enemy_hp,
    enemy_max_hp,
    enemy_sprite=None,
    battle_background="images/backgrounds/VeldoracaveBattle.png",
    predator_allowed=True,
    can_run=True
):

    modal True

    # battle_stage stays visible throughout command selection and narration.

    # ========================================================
    # BOTTOM-RIGHT COMMAND CLUSTER
    # ========================================================

    fixed:

        xsize 820
        ysize 390

        xalign 1.0
        yalign 1.0

        xoffset -15
        yoffset -5


        # ====================================================
        # MAIN
        # ====================================================

        if battle_menu_level == "main":

            use battle_command_button(
                "ITEMS",
                150,
                200,
                Show("battle_stomach_menu"),
                battle_color_stomach
            )

            use battle_command_button(
                "ALLIES",
                650,
                200,
                Show("battle_allies_menu"),
                battle_color_allies,
                thought_communication
            )

            use battle_command_button(
                "RUN",
                400,
                250,
                Return(("run",)),
                battle_color_run,
                can_run
            )

            use battle_command_button(
                "FIGHT",
                400,
                150,
                [
                    SetVariable("battle_category", None),
                    SetVariable("battle_menu_level", "categories"),
                ],
                battle_color_fight
            )


        # ====================================================
        # FIGHT CATEGORIES
        # ====================================================

        elif battle_menu_level == "categories":

            use battle_command_button(
                "PHYSICAL",
                150,
                100,
                [
                    SetVariable("battle_category", "physical"),
                    SetVariable("battle_menu_level", "moves"),
                ],
                battle_color_physical
            )

            use battle_command_button(
                "AURA",
                650,
                100,
                [
                    SetVariable("battle_category", "aura"),
                    SetVariable("battle_menu_level", "moves"),
                ],
                battle_color_aura
            )

            use battle_command_button(
                "MAGIC",
                150,
                200,
                [
                    SetVariable("battle_category", "magic"),
                    SetVariable("battle_menu_level", "moves"),
                ],
                battle_color_magic
            )

            use battle_command_button(
                "SKILLS",
                650,
                200,
                [
                    SetVariable("battle_category", "skills"),
                    SetVariable("battle_menu_level", "moves"),
                ],
                battle_color_skills
            )

            use battle_command_button(
                "FIGHT",
                400,
                150,
                NullAction(),
                battle_color_fight
            )

            use battle_command_button(
                "CANCEL",
                400,
                250,
                [
                    SetVariable("battle_category", None),
                    SetVariable("battle_menu_level", "main"),
                ],
                battle_color_cancel
            )


        # ====================================================
        # EQUIPPED MOVES
        # ====================================================

        elif battle_menu_level == "moves":

            if battle_category == "physical":

                $ current_moves = get_equipped_moves("physical", predator_allowed)[:3]
                $ current_category_name = "PHYSICAL"
                $ current_category_color = battle_color_physical

                use battle_move_button(current_moves, 0, 150, 100, current_category_color, enemy_hp, predator_allowed)
                use battle_move_button(current_moves, 1, 650, 100, current_category_color, enemy_hp, predator_allowed)
                use battle_move_button(current_moves, 2, 400, 50, current_category_color, enemy_hp, predator_allowed)


            elif battle_category == "aura":

                $ current_moves = get_equipped_moves("aura", predator_allowed)[:5]
                $ current_category_name = "AURA"
                $ current_category_color = battle_color_aura

                use battle_five_move_layout(current_moves, current_category_color, enemy_hp, predator_allowed)


            elif battle_category == "magic":

                $ current_moves = get_equipped_moves("magic", predator_allowed)[:5]
                $ current_category_name = "MAGIC"
                $ current_category_color = battle_color_magic

                use battle_five_move_layout(current_moves, current_category_color, enemy_hp, predator_allowed)


            else:

                $ current_moves = get_equipped_moves("skills", predator_allowed)[:5]
                $ current_category_name = "SKILLS"
                $ current_category_color = battle_color_skills

                use battle_five_move_layout(current_moves, current_category_color, enemy_hp, predator_allowed)


            use battle_command_button(
                current_category_name,
                400,
                150,
                NullAction(),
                current_category_color
            )

            use battle_command_button(
                "CANCEL",
                400,
                250,
                [
                    SetVariable("battle_category", None),
                    SetVariable("battle_menu_level", "categories"),
                ],
                battle_color_cancel
            )


# ============================================================
# FIVE MOVE LAYOUT
# ============================================================

screen battle_five_move_layout(
    move_list,
    button_color,
    enemy_hp,
    predator_allowed
):

    use battle_move_button(move_list, 0, 150, 100, button_color, enemy_hp, predator_allowed)
    use battle_move_button(move_list, 1, 650, 100, button_color, enemy_hp, predator_allowed)
    use battle_move_button(move_list, 2, 150, 200, button_color, enemy_hp, predator_allowed)
    use battle_move_button(move_list, 3, 650, 200, button_color, enemy_hp, predator_allowed)
    use battle_move_button(move_list, 4, 400, 50, button_color, enemy_hp, predator_allowed)


# ============================================================
# MOVE BUTTON
# ============================================================

screen battle_move_button(
    move_list,
    slot_number,
    px,
    py,
    button_color,
    enemy_hp,
    predator_allowed
):

    if slot_number < len(move_list):

        $ move_name = move_list[slot_number]
        $ enabled = move_context_available(
            move_name,
            predator_allowed,
            enemy_hp,
            player_hp,
            player_max_hp
        )

        use battle_command_button(
            move_name + "\n" + str(MOVE_DATA[move_name].get("mp_cost", 0)) + " MP",
            px,
            py,
            Return(("move", battle_category, move_name)),
            button_color,
            enabled
        )


# ============================================================
# STOMACH
# ============================================================

screen battle_stomach_menu():
    modal True
    zorder 200
    key "game_menu" action Hide("battle_stomach_menu")
    use rpg_panel("Battle items • Using an item takes a turn", Hide("battle_stomach_menu")):
        use rpg_inventory_contents(battle=True)


screen battle_storage_entry(item_name, amount):

    frame:

        xfill True
        yminimum 75

        background "#EEEEEE"
        padding (18, 12)

        hbox:

            xfill True

            frame:

                xsize 48
                ysize 48
                background "#B8B8B8"

                text "?":
                    size 24
                    color "#202020"
                    xalign 0.5
                    yalign 0.5

            null width 15

            text item_name:
                size 25
                color "#202020"
                yalign 0.5

            text "x[amount]":
                size 25
                color "#202020"
                xalign 1.0
                yalign 0.5


# ============================================================
# ALLIES
# ============================================================

screen battle_allies_menu():

    zorder 200
    key "game_menu" action Hide("battle_allies_menu")

    modal True

    add "#00000070"

    frame:

        xalign 0.5
        yalign 0.5

        xsize 650
        background "#D6D6D6F2"
        padding (30, 30)

        vbox:

            spacing 15

            hbox:

                xfill True

                text "ALLIES":
                    size 36
                    color "#202020"

                textbutton "X":
                    xalign 1.0
                    background None
                    text_size 28
                    text_color "#202020"
                    action Hide("battle_allies_menu")

            if not thought_communication:

                text "Thought Communication is required to fight with allies.":
                    size 24
                    color "#555555"

            else:

                for slot in range(3):

                    frame:

                        xfill True
                        ysize 90
                        background "#EEEEEE"
                        padding (18, 15)

                        if slot < len(battle_allies):

                            text battle_allies[slot]:
                                size 27
                                color "#202020"
                                yalign 0.5

                        else:

                            text "EMPTY ALLY SLOT":
                                size 24
                                color "#888888"
                                yalign 0.5

# ============================================================
# ADVANCE TURN ORDER
# ============================================================

label advance_battle_turn_order:

    $ prepare_battle_turn_shift()

    $ renpy.restart_interaction()

    $ renpy.pause(0.30, hard=True)

    $ battle_turn_order_shifting = False
    $ battle_turn_old_queue = []

    $ renpy.restart_interaction()

    return

# ============================================================
# PERSISTENT BATTLE PRESENTATION
# ============================================================

screen battle_stage():

    add enemy_background

    add "images/characters/yourself/slimebattle.png" at battle_player_sprite_position

    if enemy_sprite:
        add enemy_sprite at battle_enemy_sprite_position
    else:
        frame:
            xpos 1120
            ypos 280
            xysize (510, 280)
            background "#14282DDD"

            vbox:
                align (0.5, 0.5)
                spacing 15

                text enemy_name:
                    size 36
                    color "#EDF6F4"
                    xalign 0.5

                text "SPRITE PLACEHOLDER":
                    size 20
                    color "#A8BEC5"
                    xalign 0.5

    use battle_turn_order(enemy_name)
    use battle_player_status()
    use battle_enemy_status(enemy_name, enemy_hp, enemy_max_hp)
