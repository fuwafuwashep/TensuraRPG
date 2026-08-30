# ============================================================
# BATTLE MENU
# ============================================================


default battle_menu_level = "main"
default battle_category = None


# ============================================================
# ALLIES
#
# Maximum of three.
# Later put ally names in this list when they join battle.
# ============================================================

default battle_allies = []


# ============================================================
# PHYSICAL MOVES
# ============================================================

default battle_physical_moves = [
    "Basic Attack",
]


# ============================================================
# ARTS
# ============================================================

default battle_art_moves = []


# ============================================================
# SKILLS
# ============================================================

default battle_skill_moves = []


# ============================================================
# GENERIC COMMAND BUTTON
# ============================================================

screen battle_command_button(
    button_text,
    px,
    py,
    button_action,
    enabled=True
):


    textbutton button_text:

        xcenter px
        ycenter py

        xsize 300
        ysize 90

        background "images/battle_ui/command_button.svg"
        hover_background "images/battle_ui/command_button.svg"
        insensitive_background "images/battle_ui/command_button.svg"

        text_size 27

        text_color "#242424"
        text_hover_color "#000000"
        text_insensitive_color "#888888"

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


            # Player currently first.

            use turn_order_entry("YOU")


            # Allies are inserted after the player for now.
            # Later battle speed will determine the real order.

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
# HP PANELS
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



screen battle_enemy_status(enemy_name, enemy_hp, enemy_max_hp):


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
# BATTLE SCREEN
# ============================================================

screen battle_command_menu(
    enemy_name,
    enemy_hp,
    enemy_max_hp
):


    modal True


    use battle_turn_order(enemy_name)

    use battle_player_status()

    use battle_enemy_status(
        enemy_name,
        enemy_hp,
        enemy_max_hp
    )


    # ========================================================
    # BOTTOM COMMAND AREA
    # ========================================================

    fixed:

        xsize 1100
        ysize 370

        xcenter 960
        yalign 1.0

        yoffset -10


        # ====================================================
        # MAIN
        #
        # STORAGE     FIGHT     ALLIES
        #
        #              RUN
        # ====================================================

        if battle_menu_level == "main":


            use battle_command_button(
                "STORAGE",
                225,
                180,
                Show("battle_storage_menu")
            )


            use battle_command_button(
                "FIGHT",
                550,
                180,
                [
                    SetVariable(
                        "battle_category",
                        None
                    ),
                    SetVariable(
                        "battle_menu_level",
                        "categories"
                    ),
                ]
            )


            use battle_command_button(
                "ALLIES",
                875,
                180,
                Show("battle_allies_menu")
            )


            use battle_command_button(
                "RUN",
                550,
                285,
                Return(("run",))
            )



        # ====================================================
        # CATEGORIES
        #
        # PHYSICAL              ARTS
        #
        #              BACK
        #
        # SKILLS                MAGIC
        # ====================================================

        elif battle_menu_level == "categories":


            use battle_command_button(
                "PHYSICAL",
                320,
                125,
                [
                    SetVariable(
                        "battle_category",
                        "physical"
                    ),
                    SetVariable(
                        "battle_menu_level",
                        "moves"
                    ),
                ]
            )


            use battle_command_button(
                "ARTS",
                780,
                125,
                [
                    SetVariable(
                        "battle_category",
                        "arts"
                    ),
                    SetVariable(
                        "battle_menu_level",
                        "moves"
                    ),
                ]
            )


            use battle_command_button(
                "SKILLS",
                320,
                260,
                [
                    SetVariable(
                        "battle_category",
                        "skills"
                    ),
                    SetVariable(
                        "battle_menu_level",
                        "moves"
                    ),
                ]
            )


            use battle_command_button(
                "MAGIC",
                780,
                260,
                [
                    SetVariable(
                        "battle_category",
                        "magic"
                    ),
                    SetVariable(
                        "battle_menu_level",
                        "moves"
                    ),
                ]
            )


            use battle_command_button(
                "BACK",
                550,
                192,
                [
                    SetVariable(
                        "battle_category",
                        None
                    ),
                    SetVariable(
                        "battle_menu_level",
                        "main"
                    ),
                ]
            )



        # ====================================================
        # MOVE SELECTION
        # ====================================================

        elif battle_menu_level == "moves":


            # ------------------------------------------------
            # DETERMINE AVAILABLE MOVES
            # ------------------------------------------------

            if battle_category == "physical":

                $ current_moves = battle_physical_moves


            elif battle_category == "arts":

                $ current_moves = battle_art_moves


            elif battle_category == "skills":

                $ current_moves = battle_skill_moves


            elif battle_category == "magic":

                # Water Manipulation unlocks Spirit Water Magic.

                if water_manipulation:

                    $ current_moves = [
                        "Water Blade",
                    ]

                else:

                    $ current_moves = []


            else:

                $ current_moves = []



            # ------------------------------------------------
            # FOUR MOVE POSITIONS
            # ------------------------------------------------

            use battle_move_button(
                current_moves,
                0,
                320,
                125
            )


            use battle_move_button(
                current_moves,
                1,
                780,
                125
            )


            use battle_move_button(
                current_moves,
                2,
                320,
                260
            )


            use battle_move_button(
                current_moves,
                3,
                780,
                260
            )


            use battle_command_button(
                "BACK",
                550,
                192,
                [
                    SetVariable(
                        "battle_category",
                        None
                    ),
                    SetVariable(
                        "battle_menu_level",
                        "categories"
                    ),
                ]
            )



# ============================================================
# MOVE BUTTON
# ============================================================

screen battle_move_button(
    move_list,
    slot_number,
    px,
    py
):


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
            )
        )


    else:


        use battle_command_button(
            "EMPTY",
            px,
            py,
            NullAction(),
            False
        )



# ============================================================
# STORAGE
# ============================================================

screen battle_storage_menu():

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


                text "STORAGE":

                    size 36
                    color "#202020"


                textbutton "X":

                    xalign 1.0

                    background None

                    text_size 28
                    text_color "#202020"

                    action Hide(
                        "battle_storage_menu"
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