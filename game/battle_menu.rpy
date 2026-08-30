# ============================================================
# BATTLE MENU
# ============================================================

default battle_menu_level = "main"
default battle_category = None

default battle_spin_from = 0.0
default battle_spin_to = 0.0


# ------------------------------------------------------------
# CURRENT EQUIPPED MOVES
#
# Later these will be changed by an outside-battle loadout menu.
# ------------------------------------------------------------

default battle_physical_moves = [
    "Basic Attack",
]

default battle_art_moves = []

default battle_magic_moves = []

default battle_skill_moves = [
    "Water Manipulation",
]


# ============================================================
# WHEEL ANIMATION
# ============================================================

transform battle_wheel_spin:

    subpixel True
    transform_anchor True

    on show:

        alpha 0.0
        rotate battle_spin_from

        easeout 0.25:
            alpha 1.0
            rotate 0.0

    on hide:

        easein 0.20:
            alpha 0.0
            rotate battle_spin_to


# ============================================================
# REUSABLE BUTTON
# ============================================================

screen battle_slot_button(button_text, px, py, button_action, enabled=True):

    textbutton button_text:

        xcenter px
        ycenter py

        xsize 250
        ysize 95

        background None
        hover_background None
        insensitive_background None

        text_size 30

        text_color "#FFFFFF"
        text_hover_color "#99CCFF"
        text_insensitive_color "#606770"

        text_xalign 0.5
        text_yalign 0.5

        sensitive enabled
        action button_action


# ============================================================
# MOVE SLOT
# ============================================================

screen battle_move_slot(slot_number, px, py, move_list):

    if slot_number < len(move_list):

        use battle_slot_button(
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

        use battle_slot_button(
            "EMPTY",
            px,
            py,
            NullAction(),
            False
        )


# ============================================================
# MAIN BATTLE COMMAND SCREEN
# ============================================================

screen battle_command_menu(enemy_name, enemy_hp, enemy_max_hp):

    modal True

    $ shown_enemy_hp = max(0, enemy_hp)
    $ shown_player_hp = max(0, player_hp)


    # --------------------------------------------------------
    # HP DISPLAY
    # --------------------------------------------------------

    frame:

        xalign 0.5
        ypos 35

        padding (30, 18)

        background "#101722E6"

        vbox:

            spacing 8

            text "[enemy_name]  HP: [shown_enemy_hp] / [enemy_max_hp]":
                size 28
                xalign 0.5

            text "Your HP: [shown_player_hp] / [player_max_hp]":
                size 28
                xalign 0.5


    # ========================================================
    # MAIN THREE-POINT MENU
    #
    #                 FIGHT
    #
    #                   O
    #
    #           STORAGE     RUN
    #
    # ========================================================

    showif battle_menu_level == "main":

        fixed:

            at battle_wheel_spin

            xsize 900
            ysize 600

            xcenter 960
            ycenter 690

            add "images/battle_ui/battle_main_wheel.svg"


            # FIGHT - TOP

            use battle_slot_button(
                "FIGHT",
                450,
                155,
                [
                    SetVariable("battle_spin_from", -28.0),
                    SetVariable("battle_spin_to", 28.0),
                    SetVariable("battle_category", None),
                    SetVariable("battle_menu_level", "categories"),
                ]
            )


            # STORAGE - BOTTOM LEFT

            use battle_slot_button(
                "STORAGE",
                300,
                440,
                Show("battle_storage_menu")
            )


            # RUN - BOTTOM RIGHT

            use battle_slot_button(
                "RUN",
                600,
                440,
                Return(("run",))
            )


    # ========================================================
    # FIVE-POINT STAR
    #
    #                 PHYSICAL
    #
    #       BACK        O        ARTS
    #
    #            SKILLS     MAGIC
    #
    # ========================================================

    showif battle_menu_level == "categories" or battle_menu_level == "moves":

        fixed:

            at battle_wheel_spin

            xsize 900
            ysize 600

            xcenter 960
            ycenter 690

            add "images/battle_ui/battle_star_wheel.svg"


            # ------------------------------------------------
            # BACK - ALWAYS LEFT
            # ------------------------------------------------

            if battle_menu_level == "moves":

                use battle_slot_button(
                    "BACK",
                    285,
                    300,
                    [
                        SetVariable("battle_category", None),
                        SetVariable("battle_menu_level", "categories"),
                    ]
                )

            else:

                use battle_slot_button(
                    "BACK",
                    285,
                    300,
                    [
                        SetVariable("battle_spin_from", 28.0),
                        SetVariable("battle_spin_to", -28.0),
                        SetVariable("battle_category", None),
                        SetVariable("battle_menu_level", "main"),
                    ]
                )


            # =================================================
            # CATEGORY MODE
            # =================================================

            if battle_menu_level == "categories":


                # TOP

                use battle_slot_button(
                    "PHYSICAL",
                    450,
                    155,
                    [
                        SetVariable("battle_category", "physical"),
                        SetVariable("battle_menu_level", "moves"),
                    ]
                )


                # RIGHT

                use battle_slot_button(
                    "ARTS",
                    615,
                    300,
                    [
                        SetVariable("battle_category", "arts"),
                        SetVariable("battle_menu_level", "moves"),
                    ]
                )


                # BOTTOM RIGHT

                use battle_slot_button(
                    "MAGIC",
                    600,
                    440,
                    [
                        SetVariable("battle_category", "magic"),
                        SetVariable("battle_menu_level", "moves"),
                    ]
                )


                # BOTTOM LEFT

                use battle_slot_button(
                    "SKILLS",
                    300,
                    440,
                    [
                        SetVariable("battle_category", "skills"),
                        SetVariable("battle_menu_level", "moves"),
                    ]
                )


            # =================================================
            # MOVE MODE
            #
            # STAR DOES NOT MOVE.
            # ONLY THE FOUR LABELS CHANGE.
            # BACK STAYS LEFT.
            # =================================================

            else:

                if battle_category == "physical":

                    $ current_moves = battle_physical_moves


                elif battle_category == "arts":

                    $ current_moves = battle_art_moves


                elif battle_category == "magic":

                    $ current_moves = battle_magic_moves


                elif battle_category == "skills":

                    if water_manipulation:

                        $ current_moves = battle_skill_moves

                    else:

                        $ current_moves = []


                else:

                    $ current_moves = []


                # TOP / MOVE 1

                use battle_move_slot(
                    0,
                    450,
                    155,
                    current_moves
                )


                # RIGHT / MOVE 2

                use battle_move_slot(
                    1,
                    615,
                    300,
                    current_moves
                )


                # BOTTOM RIGHT / MOVE 3

                use battle_move_slot(
                    2,
                    600,
                    440,
                    current_moves
                )


                # BOTTOM LEFT / MOVE 4

                use battle_move_slot(
                    3,
                    300,
                    440,
                    current_moves
                )


# ============================================================
# STORAGE
# ============================================================

screen battle_storage_menu():

    modal True

    frame:

        xalign 0.5
        yalign 0.5

        xsize 520

        padding (40, 35)

        background "#101722F2"

        vbox:

            xalign 0.5
            spacing 20

            text "STORAGE":
                size 36
                xalign 0.5

            text "Magic Ore Clusters: [magic_ore_clusters]":
                size 25
                xalign 0.5

            text "Hipokute Herb Clusters: [hipokute_herb_clusters]":
                size 25
                xalign 0.5

            null height 10

            text "No combat-usable stored items yet.":
                size 22
                xalign 0.5

            null height 10

            textbutton "BACK":

                xalign 0.5

                action Hide("battle_storage_menu")