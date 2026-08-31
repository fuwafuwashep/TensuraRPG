# ============================================================
# PART 2 ENEMY DATA
# ============================================================

init python:


    part2_enemy_data = {


        # ====================================================
        # TEMPEST SERPENT
        # ====================================================

        "tempest_serpent": {

            "name": "Tempest Serpent",

            "max_hp": 38,

            "run_chance": 0.65,

            # Heat Source Perception is NOT an attack.
            "passive": "Heat Source Perception",

            "armor": 0,

            "moves": [

                {
                    "name": "Bite",
                    "category": "physical",
                    "min_damage": 4,
                    "max_damage": 6,
                },

                {
                    "name": "Tail Whip",
                    "category": "physical",
                    "min_damage": 4,
                    "max_damage": 7,
                },

                {
                    "name": "Poison Breath",
                    "category": "skill",
                    "min_damage": 5,
                    "max_damage": 8,
                },
            ],
        },


        # ====================================================
        # BLACK SPIDER
        # ====================================================

        "black_spider": {

            "name": "Black Spider",

            "max_hp": 34,

            "run_chance": 0.70,

            "passive": None,

            "armor": 0,

            "moves": [

                {
                    "name": "Poisonous Bite",
                    "category": "physical",
                    "min_damage": 4,
                    "max_damage": 6,
                },

                {
                    "name": "Sticky Thread",
                    "category": "skill",
                    "min_damage": 1,
                    "max_damage": 2,
                },

                {
                    "name": "Steel Thread",
                    "category": "skill",
                    "min_damage": 5,
                    "max_damage": 8,
                },
            ],
        },


        # ====================================================
        # GIANT BAT
        # ====================================================

        "giant_bat": {

            "name": "Giant Bat",

            "max_hp": 32,

            "run_chance": 0.75,

            "passive": None,

            "armor": 0,

            "moves": [

                {
                    "name": "Drain",
                    "category": "skill",
                    "min_damage": 4,
                    "max_damage": 6,
                },

                {
                    "name": "Ultrasonic Waves",
                    "category": "skill",
                    "min_damage": 5,
                    "max_damage": 7,
                },
            ],
        },


        # ====================================================
        # EVIL CENTIPEDE
        # ====================================================

        "evil_centipede": {

            "name": "Evil Centipede",

            "max_hp": 42,

            "run_chance": 0.60,

            "passive": None,

            "armor": 0,

            "moves": [

                {
                    "name": "Bite",
                    "category": "physical",
                    "min_damage": 5,
                    "max_damage": 7,
                },

                {
                    "name": "Headbutt",
                    "category": "physical",
                    "min_damage": 5,
                    "max_damage": 8,
                },

                {
                    "name": "Paralyzing Breath",
                    "category": "skill",
                    "min_damage": 4,
                    "max_damage": 7,
                },
            ],
        },


        # ====================================================
        # ARMORSAURUS
        # ====================================================

        "armorsaurus": {

            "name": "Armorsaurus",

            "max_hp": 50,

            "run_chance": 0.55,

            # Body Armor is passive, not a move.
            "passive": "Body Armor",

            # Reduces incoming player damage by 2.
            "armor": 2,

            "moves": [

                {
                    "name": "Bite",
                    "category": "physical",
                    "min_damage": 6,
                    "max_damage": 8,
                },

                {
                    "name": "Headbutt",
                    "category": "physical",
                    "min_damage": 7,
                    "max_damage": 9,
                },
            ],
        },
    }


# ============================================================
# GENERIC PART 2 BATTLE
# ============================================================

label battle_part2_enemy(enemy_key):


    # --------------------------------------------------------
    # LOAD ENEMY DATA
    # --------------------------------------------------------

    $ enemy_data = part2_enemy_data[enemy_key]

    $ enemy_name = enemy_data["name"]

    $ enemy_max_hp = enemy_data["max_hp"]
    $ enemy_hp = enemy_max_hp

    $ enemy_run_chance = enemy_data["run_chance"]

    $ enemy_passive = enemy_data["passive"]

    $ enemy_armor = enemy_data["armor"]


    # --------------------------------------------------------
    # PLAYER
    # --------------------------------------------------------

    $ player_hp = player_max_hp


    # Sticky Thread can temporarily restrict the player.
    $ player_restrained = False


    n "[enemy_name] attacks!"


    if enemy_passive:

        n "Intrinsic Skill: [enemy_passive]."


    # ========================================================
    # BATTLE LOOP
    # ========================================================

    while enemy_hp > 0 and player_hp > 0:


        $ battle_menu_level = "main"
        $ battle_category = None


        window hide


        $ battle_result = renpy.call_screen(
            "battle_command_menu",
            enemy_name=enemy_name,
            enemy_hp=enemy_hp,
            enemy_max_hp=enemy_max_hp
        )


        window show


        # ====================================================
        # RUN
        # ====================================================

        if battle_result[0] == "run":


            $ run_roll = renpy.random.random()


            if run_roll < enemy_run_chance:


                n "You escape from the [enemy_name]."


                return "ran"


            else:


                n "The [enemy_name] blocks your escape!"


        # ====================================================
        # PLAYER MOVE
        # ====================================================

        elif battle_result[0] == "move":


            $ chosen_category = battle_result[1]
            $ chosen_move = battle_result[2]


            # ------------------------------------------------
            # BASIC ATTACK
            # ------------------------------------------------

            if chosen_move == "Basic Attack":


                $ player_damage = renpy.random.randint(5, 8)


                if player_restrained:

                    $ player_damage = max(
                        1,
                        player_damage - 2
                    )

                    $ player_restrained = False


                    n "The Sticky Thread restricts your movement."


                # Armorsaurus Body Armor.
                if enemy_armor > 0:


                    $ original_damage = player_damage


                    $ player_damage = max(
                        1,
                        player_damage - enemy_armor
                    )


                    if player_damage < original_damage:

                        n "Body Armor reduces the damage."


                $ enemy_hp = max(
                    0,
                    enemy_hp - player_damage
                )


                n "You attack the [enemy_name]."

                n "You deal [player_damage] damage!"


            # ------------------------------------------------
            # WATER BLADE
            # ------------------------------------------------

            elif chosen_move == "Water Blade":


                $ player_damage = renpy.random.randint(6, 9)


                if player_restrained:


                    $ player_damage = max(
                        1,
                        player_damage - 2
                    )

                    $ player_restrained = False


                    n "The Sticky Thread restricts your movement."


                if enemy_armor > 0:


                    $ original_damage = player_damage


                    $ player_damage = max(
                        1,
                        player_damage - enemy_armor
                    )


                    if player_damage < original_damage:

                        n "Body Armor reduces the damage."


                $ enemy_hp = max(
                    0,
                    enemy_hp - player_damage
                )


                n "Water gathers into a sharp blade."

                n "The Water Blade strikes the [enemy_name]."

                n "You deal [player_damage] damage!"


            # ------------------------------------------------
            # FUTURE PLAYER MOVES
            # ------------------------------------------------

            else:


                n "[chosen_move] has not been programmed yet."


        # ====================================================
        # ENEMY TURN
        # ====================================================

        if enemy_hp > 0:


            $ enemy_move = renpy.random.choice(
                enemy_data["moves"]
            )


            $ enemy_move_name = enemy_move["name"]


            # ------------------------------------------------
            # STICKY THREAD
            # ------------------------------------------------

            if enemy_move_name == "Sticky Thread":


                $ enemy_damage = renpy.random.randint(
                    enemy_move["min_damage"],
                    enemy_move["max_damage"]
                )


                $ player_hp = max(
                    0,
                    player_hp - enemy_damage
                )


                $ player_restrained = True


                n "The Black Spider uses Sticky Thread!"

                n "The thread wraps around you and restricts your movement."

                n "You take [enemy_damage] damage."


            # ------------------------------------------------
            # DRAIN
            # ------------------------------------------------

            elif enemy_move_name == "Drain":


                $ enemy_damage = renpy.random.randint(
                    enemy_move["min_damage"],
                    enemy_move["max_damage"]
                )


                $ player_hp = max(
                    0,
                    player_hp - enemy_damage
                )


                $ drain_heal = max(
                    1,
                    enemy_damage // 2
                )


                $ enemy_hp = min(
                    enemy_max_hp,
                    enemy_hp + drain_heal
                )


                n "The Giant Bat uses Drain!"

                n "You take [enemy_damage] damage."

                n "The Giant Bat restores [drain_heal] HP."


            # ------------------------------------------------
            # NORMAL ENEMY ATTACK
            # ------------------------------------------------

            else:


                $ enemy_damage = renpy.random.randint(
                    enemy_move["min_damage"],
                    enemy_move["max_damage"]
                )


                $ player_hp = max(
                    0,
                    player_hp - enemy_damage
                )


                n "The [enemy_name] uses [enemy_move_name]!"

                n "You take [enemy_damage] damage."


    # ========================================================
    # RESULT
    # ========================================================

    if enemy_hp <= 0:


        return "won"


    return "lost"