# ============================================================
# BATTLE MENU
# ============================================================


default battle_menu_level = "main"
default battle_category = None


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
# ALLIES
# ============================================================

default battle_allies = []


# ============================================================
# EQUIPPED MOVES
#
# Physical = maximum 3
# Aura     = maximum 5
# Magic    = maximum 5
# Skills   = maximum 5
# ============================================================

default battle_physical_moves = [
    "Basic Attack",
]


default battle_aura_moves = []


# Water Blade is equipped for now.
# It only appears if Water Manipulation has been acquired.

default battle_magic_moves = [
    "Water Blade",
]


default battle_skill_moves = []

# ============================================================
# BATTLE SPRITE POSITIONS
# ============================================================

transform battle_player_sprite_position:

    xanchor 0.5
    yanchor 1.0

    xpos 360
    ypos 960

    zoom 0.75


transform battle_enemy_sprite_position:

    xanchor 0.5
    yanchor 1.0

    xpos 1390
    ypos 650

    zoom 0.70


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
        "images/battle_ui/command_button.svg",
        matrixcolor=TintMatrix(button_color)
    )


    textbutton button_text:

        xcenter px
        ycenter py

        xsize 300
        ysize 90

        background button_image
        hover_background button_image
        insensitive_background button_image

        focus_mask True

        text_size 27

        text_color "#111111"
        text_hover_color "#000000"
        text_insensitive_color "#555555"

        text_xalign 0.5
        text_yalign 0.5

        sensitive enabled

        action button_action


# ============================================================
# TURN ORDER
# ============================================================

screen battle_turn_order(enemy_name):


    frame:

        xalign 0.5
        ypos 20

        background "#D6D6D6E6"

        padding (12, 8)


        hbox:

            spacing 8


            use turn_order_entry("YOU")


            for ally in battle_allies:

                use turn_order_entry(ally)


            use turn_order_entry(enemy_name)



screen turn_order_entry(character_name):


    frame:

        xsize 115
        ysize 58

        background "#EEEEEEF2"

        padding (6, 6)


        text character_name:

            size 18
            color "#202020"

            xalign 0.5
            yalign 0.5


# ============================================================
# PLAYER STATUS
# ============================================================

screen battle_player_status():


    frame:

        xpos 30
        yalign 0.86

        xsize 300

        background "#D6D6D6E6"

        padding (15, 10)


        vbox:

            spacing 5


            text "YOU":

                size 24
                color "#202020"


            text "HP  [player_hp] / [player_max_hp]":

                size 20
                color "#202020"


# ============================================================
# ENEMY STATUS
# ============================================================

screen battle_enemy_status(
    enemy_name,
    enemy_hp,
    enemy_max_hp
):


    frame:

        xalign 0.98
        ypos 105

        xsize 330

        background "#D6D6D6E6"

        padding (15, 10)


        vbox:

            spacing 5


            text enemy_name:

                size 24
                color "#202020"


            text "HP  [enemy_hp] / [enemy_max_hp]":

                size 20
                color "#202020"


# ============================================================
# MAIN BATTLE SCREEN
# ============================================================

screen battle_command_menu(
    enemy_name,
    enemy_hp,
    enemy_max_hp,
    enemy_sprite=None,
    battle_background="images/backgrounds/VeldoracaveBattle.png"
):

    # ========================================================
    # BATTLE BACKGROUND
    # ========================================================

    add battle_background


    # ========================================================
    # PLAYER SPRITE
    # ========================================================

    add "images/characters/yourself/slimebattle.png" at battle_player_sprite_position


    # ========================================================
    # ENEMY SPRITE
    # ========================================================

    if enemy_sprite:

        add enemy_sprite at battle_enemy_sprite_position

    modal True


    use battle_turn_order(enemy_name)

    use battle_player_status()

    use battle_enemy_status(
        enemy_name,
        enemy_hp,
        enemy_max_hp
    )


    # ========================================================
    # COMMAND CLUSTER
    #
    # This entire area is anchored to the BOTTOM RIGHT
    # of the 1920 x 1080 screen.
    # ========================================================

    fixed:

        xsize 950
        ysize 400

        xalign 1.0
        yalign 1.0

        xoffset -15
        yoffset -10


        # ====================================================
        # MAIN MENU
        #
        #
        # STOMACH       FIGHT       ALLIES
        #
        #                 RUN
        #
        # ====================================================

        if battle_menu_level == "main":


            # STOMACH - LEFT

            use battle_command_button(
                "STOMACH",
                160,
                190,
                Show("battle_stomach_menu"),
                battle_color_stomach
            )


            # ALLIES - RIGHT

            use battle_command_button(
                "ALLIES",
                790,
                190,
                Show("battle_allies_menu"),
                battle_color_allies
            )


            # RUN - BOTTOM CENTER

            use battle_command_button(
                "RUN",
                475,
                290,
                Return(("run",)),
                battle_color_run
            )


            # FIGHT - CENTER
            #
            # Drawn last so it appears above the side buttons.

            use battle_command_button(
                "FIGHT",
                475,
                165,
                [
                    SetVariable(
                        "battle_category",
                        None
                    ),

                    SetVariable(
                        "battle_menu_level",
                        "categories"
                    ),
                ],
                battle_color_fight
            )


        # ====================================================
        # FIGHT CATEGORY MENU
        #
        #
        # PHYSICAL                  AURA
        #
        #              FIGHT
        #
        # MAGIC                    SKILLS
        #
        #              CANCEL
        #
        # ====================================================

        elif battle_menu_level == "categories":


            # PHYSICAL - UPPER LEFT

            use battle_command_button(
                "PHYSICAL",
                205,
                135,
                [
                    SetVariable(
                        "battle_category",
                        "physical"
                    ),

                    SetVariable(
                        "battle_menu_level",
                        "moves"
                    ),
                ],
                battle_color_physical
            )


            # AURA - UPPER RIGHT

            use battle_command_button(
                "AURA",
                745,
                135,
                [
                    SetVariable(
                        "battle_category",
                        "aura"
                    ),

                    SetVariable(
                        "battle_menu_level",
                        "moves"
                    ),
                ],
                battle_color_aura
            )


            # MAGIC - LOWER LEFT

            use battle_command_button(
                "MAGIC",
                205,
                250,
                [
                    SetVariable(
                        "battle_category",
                        "magic"
                    ),

                    SetVariable(
                        "battle_menu_level",
                        "moves"
                    ),
                ],
                battle_color_magic
            )


            # SKILLS - LOWER RIGHT

            use battle_command_button(
                "SKILLS",
                745,
                250,
                [
                    SetVariable(
                        "battle_category",
                        "skills"
                    ),

                    SetVariable(
                        "battle_menu_level",
                        "moves"
                    ),
                ],
                battle_color_skills
            )


            # FIGHT - CENTER

            use battle_command_button(
                "FIGHT",
                475,
                192,
                NullAction(),
                battle_color_fight
            )


            # CANCEL - BOTTOM

            use battle_command_button(
                "CANCEL",
                475,
                335,
                [
                    SetVariable(
                        "battle_category",
                        None
                    ),

                    SetVariable(
                        "battle_menu_level",
                        "main"
                    ),
                ],
                battle_color_cancel
            )


        # ====================================================
        # MOVE MENU
        # ====================================================

        elif battle_menu_level == "moves":


            # ------------------------------------------------
            # PHYSICAL
            #
            # Maximum 3 moves.
            # ------------------------------------------------

            if battle_category == "physical":


                $ current_moves = battle_physical_moves[:3]
                $ current_category_name = "PHYSICAL"
                $ current_category_color = battle_color_physical


                # Move 1 - LEFT

                use battle_move_button(
                    current_moves,
                    0,
                    205,
                    145,
                    current_category_color
                )


                # Move 2 - RIGHT

                use battle_move_button(
                    current_moves,
                    1,
                    745,
                    145,
                    current_category_color
                )


                # Move 3 - TOP

                use battle_move_button(
                    current_moves,
                    2,
                    475,
                    60,
                    current_category_color
                )


            # ------------------------------------------------
            # AURA
            #
            # Maximum 5 moves.
            # ------------------------------------------------

            elif battle_category == "aura":


                $ current_moves = battle_aura_moves[:5]
                $ current_category_name = "AURA"
                $ current_category_color = battle_color_aura


                use battle_five_move_layout(
                    current_moves,
                    current_category_color
                )


            # ------------------------------------------------
            # MAGIC
            #
            # Maximum 5 moves.
            # ------------------------------------------------

            elif battle_category == "magic":


                if water_manipulation:

                    $ current_moves = battle_magic_moves[:5]

                else:

                    $ current_moves = []


                $ current_category_name = "MAGIC"
                $ current_category_color = battle_color_magic


                use battle_five_move_layout(
                    current_moves,
                    current_category_color
                )


            # ------------------------------------------------
            # SKILLS
            #
            # Maximum 5 moves.
            # ------------------------------------------------

            elif battle_category == "skills":


                $ current_moves = battle_skill_moves[:5]
                $ current_category_name = "SKILLS"
                $ current_category_color = battle_color_skills


                use battle_five_move_layout(
                    current_moves,
                    current_category_color
                )


            else:


                $ current_moves = []
                $ current_category_name = "FIGHT"
                $ current_category_color = battle_color_fight


            # ------------------------------------------------
            # CURRENT CATEGORY - CENTER
            # ------------------------------------------------

            use battle_command_button(
                current_category_name,
                475,
                192,
                NullAction(),
                current_category_color
            )


            # ------------------------------------------------
            # CANCEL - BOTTOM
            #
            # Goes back to Physical / Aura / Magic / Skills.
            # ------------------------------------------------

            use battle_command_button(
                "CANCEL",
                475,
                335,
                [
                    SetVariable(
                        "battle_category",
                        None
                    ),

                    SetVariable(
                        "battle_menu_level",
                        "categories"
                    ),
                ],
                battle_color_cancel
            )


# ============================================================
# FIVE MOVE LAYOUT
#
# Used for:
# Aura
# Magic
# Skills
#
#
#                 MOVE 5
#
# MOVE 1                       MOVE 2
#
#                 CATEGORY
#
# MOVE 3                       MOVE 4
#
#                 CANCEL
# ============================================================

screen battle_five_move_layout(
    move_list,
    button_color
):


    # UPPER LEFT

    use battle_move_button(
        move_list,
        0,
        205,
        135,
        button_color
    )


    # UPPER RIGHT

    use battle_move_button(
        move_list,
        1,
        745,
        135,
        button_color
    )


    # LOWER LEFT

    use battle_move_button(
        move_list,
        2,
        205,
        250,
        button_color
    )


    # LOWER RIGHT

    use battle_move_button(
        move_list,
        3,
        745,
        250,
        button_color
    )


    # TOP CENTER

    use battle_move_button(
        move_list,
        4,
        475,
        60,
        button_color
    )


# ============================================================
# INDIVIDUAL MOVE BUTTON
# ============================================================

screen battle_move_button(
    move_list,
    slot_number,
    px,
    py,
    button_color
):


    # Only show a button if a move is actually equipped
    # in that position.

    if slot_number < len(move_list):


        use battle_command_button(
            move_list[slot_number],
            px,
            py,
            Return(
                (
                    "move",
                    battle_category,
                    move_list[slot_number]
                )
            ),
            button_color
        )


# ============================================================
# STOMACH
# ============================================================

screen battle_stomach_menu():


    modal True


    add "#00000070"


    frame:

        xalign 0.5
        yalign 0.5

        xsize 800
        ysize 720

        background "#D6D6D6F2"

        padding (30, 30)


        vbox:

            spacing 20


            hbox:

                xfill True


                text "STOMACH":

                    size 36
                    color "#202020"


                textbutton "X":

                    xalign 1.0

                    background None

                    text_size 28
                    text_color "#202020"

                    action Hide(
                        "battle_stomach_menu"
                    )


            viewport:

                xfill True
                ysize 580

                mousewheel True
                draggable True

                scrollbars "vertical"


                vbox:

                    xfill True
                    spacing 10


                    use battle_storage_entry(
                        "Hipokute Herbs",
                        hipokute_herb_clusters
                    )


                    use battle_storage_entry(
                        "Magic Ore",
                        magic_ore_clusters
                    )


# ============================================================
# STOMACH ENTRY
# ============================================================

screen battle_storage_entry(
    item_name,
    amount
):


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

                    action Hide(
                        "battle_allies_menu"
                    )


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