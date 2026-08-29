# ============================================================
# BATTLE MENU
# ============================================================


# ------------------------------------------------------------
# MENU STATE
# ------------------------------------------------------------

default battle_menu_level = "main"
default battle_category = None

# These control which direction the wheel spins.
default battle_spin_from = 0.0
default battle_spin_to = 0.0


# ------------------------------------------------------------
# EQUIPPED MOVES
# ------------------------------------------------------------

# These are placeholders for now.
# Later, the player will organize these outside of battle.

default battle_physical_moves = [
    "Bite",
    "Tail Strike",
    "Wing Strike",
]

default battle_art_moves = [
    "Aura Slash",
    "Mana Bullet",
    "Parry",
    "Instant Movement",
]

default battle_magic_moves = [
    "Fireball",
    "Ice Wall",
    "Heal",
    "Wind Cutter",
]

default battle_skill_moves = [
    "Camouflage",
    "Surface Grip",
    "Manifestation",
    "Dragon Form",
]


# ------------------------------------------------------------
# WHEEL ANIMATION
# ------------------------------------------------------------

transform battle_wheel_spin:

    transform_anchor True
    anchor (0.5, 0.5)

    on show:

        alpha 0.0
        rotate battle_spin_from

        easeout 0.25:
            alpha 1.0
            rotate 0.0

    on hide:

        easein 0.25:
            alpha 0.0
            rotate battle_spin_to


# ------------------------------------------------------------
# REUSABLE POINT BUTTON
# ------------------------------------------------------------

screen battle_point_button(button_text, px, py, button_action, enabled=True):

    textbutton button_text:

        xcenter px
        ycenter py

        xsize 240
        ysize 100

        background None
        hover_background None
        insensitive_background None

        text_size 30

        text_color "#FFFFFF"
        text_hover_color "#86D9FF"
        text_insensitive_color "#59616D"

        text_align 0.5
        text_xalign 0.5
        text_yalign 0.5

        sensitive enabled

        action button_action


# ============================================================
# ACTUAL BATTLE COMMAND SCREEN
# ============================================================

screen battle_command_menu():

    modal True


    # ========================================================
    # MAIN MENU
    #
    #       STORAGE
    #
    #             O ---- FIGHT
    #
    #          RUN
    #
    # ========================================================

    showif battle_menu_level == "main":

        fixed:

            at battle_wheel_spin

            xsize 900
            ysize 900

            xalign 0.5
            yalign 0.5

            add "images/battle_ui/battle_main_wheel.svg"


            # FIGHT
            use battle_point_button(
                "FIGHT",
                700,
                450,
                [
                    SetVariable("battle_spin_from", -36.0),
                    SetVariable("battle_spin_to", 36.0),
                    SetVariable("battle_category", None),
                    SetVariable("battle_menu_level", "categories"),
                ]
            )


            # STORAGE
            use battle_point_button(
                "STORAGE",
                300,
                205,
                Return(("command", "storage"))
            )


            # RUN
            use battle_point_button(
                "RUN",
                300,
                695,
                Return(("command", "run"))
            )



    # ========================================================
    # FIVE-POINT STAR
    #
    # Physical      Arts
    #
    # Back       O
    #
    # Skills        Magic
    #
    # ========================================================

    showif battle_menu_level == "categories" or battle_menu_level == "moves":

        fixed:

            at battle_wheel_spin

            xsize 900
            ysize 900

            xalign 0.5
            yalign 0.5

            add "images/battle_ui/battle_star_wheel.svg"


            # ------------------------------------------------
            # BACK
            #
            # This NEVER changes.
            # It is always the LEFT point of the star.
            # ------------------------------------------------

            use battle_point_button(
                "BACK",
                180,
                450,
                (
                    [
                        SetVariable("battle_category", None),
                        SetVariable("battle_menu_level", "categories"),
                    ]

                    if battle_menu_level == "moves"

                    else

                    [
                        SetVariable("battle_spin_from", 36.0),
                        SetVariable("battle_spin_to", -36.0),
                        SetVariable("battle_category", None),
                        SetVariable("battle_menu_level", "main"),
                    ]
                )
            )


            # =================================================
            # CATEGORY MODE
            # =================================================

            if battle_menu_level == "categories":


                # UPPER LEFT
                use battle_point_button(
                    "PHYSICAL",
                    355,
                    215,
                    [
                        SetVariable("battle_category", "physical"),
                        SetVariable("battle_menu_level", "moves"),
                    ]
                )


                # UPPER RIGHT
                use battle_point_button(
                    "ARTS",
                    635,
                    215,
                    [
                        SetVariable("battle_category", "arts"),
                        SetVariable("battle_menu_level", "moves"),
                    ]
                )


                # LOWER RIGHT
                use battle_point_button(
                    "MAGIC",
                    635,
                    685,
                    [
                        SetVariable("battle_category", "magic"),
                        SetVariable("battle_menu_level", "moves"),
                    ]
                )


                # LOWER LEFT
                use battle_point_button(
                    "SKILLS",
                    355,
                    685,
                    [
                        SetVariable("battle_category", "skills"),
                        SetVariable("battle_menu_level", "moves"),
                    ]
                )



            # =================================================
            # MOVE MODE
            #
            # Same star.
            # No spinning.
            # Category names are simply replaced by moves.
            # BACK stays where it is.
            # =================================================

            else:


                # Figure out which four moves should be displayed.

                if battle_category == "physical":

                    $ current_moves = battle_physical_moves


                elif battle_category == "arts":

                    $ current_moves = battle_art_moves


                elif battle_category == "magic":

                    $ current_moves = battle_magic_moves


                elif battle_category == "skills":

                    $ current_moves = battle_skill_moves


                else:

                    $ current_moves = []



                # ------------------------------------------------
                # SLOT 1 - UPPER LEFT
                # ------------------------------------------------

                if len(current_moves) >= 1:

                    use battle_point_button(
                        current_moves[0],
                        355,
                        215,
                        Return(
                            (
                                "move",
                                battle_category,
                                current_moves[0]
                            )
                        )
                    )

                else:

                    use battle_point_button(
                        "EMPTY",
                        355,
                        215,
                        NullAction(),
                        False
                    )


                # ------------------------------------------------
                # SLOT 2 - UPPER RIGHT
                # ------------------------------------------------

                if len(current_moves) >= 2:

                    use battle_point_button(
                        current_moves[1],
                        635,
                        215,
                        Return(
                            (
                                "move",
                                battle_category,
                                current_moves[1]
                            )
                        )
                    )

                else:

                    use battle_point_button(
                        "EMPTY",
                        635,
                        215,
                        NullAction(),
                        False
                    )


                # ------------------------------------------------
                # SLOT 3 - LOWER RIGHT
                # ------------------------------------------------

                if len(current_moves) >= 3:

                    use battle_point_button(
                        current_moves[2],
                        635,
                        685,
                        Return(
                            (
                                "move",
                                battle_category,
                                current_moves[2]
                            )
                        )
                    )

                else:

                    use battle_point_button(
                        "EMPTY",
                        635,
                        685,
                        NullAction(),
                        False
                    )


                # ------------------------------------------------
                # SLOT 4 - LOWER LEFT
                # ------------------------------------------------

                if len(current_moves) >= 4:

                    use battle_point_button(
                        current_moves[3],
                        355,
                        685,
                        Return(
                            (
                                "move",
                                battle_category,
                                current_moves[3]
                            )
                        )
                    )

                else:

                    use battle_point_button(
                        "EMPTY",
                        355,
                        685,
                        NullAction(),
                        False
                    )



# ============================================================
# TEST LABEL
# ============================================================

label test_battle_menu:

    # Always begin on the normal three-button wheel.

    $ battle_menu_level = "main"
    $ battle_category = None
    $ battle_spin_from = 0.0
    $ battle_spin_to = 0.0


    $ battle_result = renpy.call_screen("battle_command_menu")


    # --------------------------------------------------------
    # TEMPORARY TEST RESULTS
    # --------------------------------------------------------

    if battle_result[0] == "move":

        $ chosen_category = battle_result[1]
        $ chosen_move = battle_result[2]

        "You selected [chosen_move]."

        "Category: [chosen_category]."


    elif battle_result[1] == "storage":

        "You selected Storage."


    elif battle_result[1] == "run":

        "You selected Run."


    return