# ============================================================
# BATTLE SYSTEM
# ============================================================


# ============================================================
# THUNDER FROG
# ============================================================

label battle_thunder_frog:

    $ player_hp = player_max_hp

    $ frog_max_hp = 24
    $ frog_hp = frog_max_hp

    # 70% chance to successfully escape.
    # Different enemies can have different chances later.
    $ frog_run_chance = 0.70


    n "The Thunder Frog attacks!"


    while frog_hp > 0 and player_hp > 0:


        # Every new turn begins at the three-point menu.

        $ battle_menu_level = "main"
        $ battle_category = None
        $ battle_spin_from = 0.0
        $ battle_spin_to = 0.0


        window hide


        $ battle_result = renpy.call_screen(
            "battle_command_menu",
            enemy_name="Thunder Frog",
            enemy_hp=frog_hp,
            enemy_max_hp=frog_max_hp
        )


        window show


        # ====================================================
        # RUN
        # ====================================================

        if battle_result[0] == "run":

            $ run_roll = renpy.random.random()

            if run_roll < frog_run_chance:

                n "You escape from the Thunder Frog."

                return "ran"

            else:

                n "The Thunder Frog cuts off your escape!"


        # ====================================================
        # MOVE
        # ====================================================

            elif battle_result[0] == "move":

            $ chosen_category = battle_result[1]
            $ chosen_move = battle_result[2]


            # ------------------------------------------------
            # BASIC ATTACK
            # ------------------------------------------------

            if chosen_move == "Basic Attack":

                $ player_damage = renpy.random.randint(5, 8)

                $ frog_hp = max(
                    0,
                    frog_hp - player_damage
                )

                n "You strike the Thunder Frog."

                n "You deal [player_damage] damage!"


            # ------------------------------------------------
            # WATER BLADE
            # ------------------------------------------------

            elif chosen_move == "Water Blade":

                $ player_damage = renpy.random.randint(6, 9)

                $ frog_hp = max(
                    0,
                    frog_hp - player_damage
                )

                n "Water gathers and forms into a sharp blade."

                n "The Water Blade strikes the Thunder Frog."

                n "You deal [player_damage] damage!"


            # ------------------------------------------------
            # TEMPORARY FALLBACK
            # ------------------------------------------------

            else:

                n "[chosen_move] has not been programmed yet."


        # ====================================================
        # ENEMY TURN
        # ====================================================

        if frog_hp > 0:

            $ frog_damage = renpy.random.randint(2, 4)


            # Electricity Resistance helps against this frog.

            if electricity_resistance:

                $ frog_damage = max(
                    1,
                    frog_damage - 1
                )


            $ player_hp = max(
                0,
                player_hp - frog_damage
            )


            n "The Thunder Frog attacks!"

            n "You take [frog_damage] damage."


    # ========================================================
    # RESULT
    # ========================================================

    if frog_hp <= 0:

        return "won"

    return "lost"