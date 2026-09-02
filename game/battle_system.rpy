# ============================================================
# GLOBAL BATTLE SYSTEM
# ============================================================

# The exact HP values for the newer monsters are placeholder
# balancing values. The move damage/accuracy/effect values are
# based on the design currently written for the game.


default last_battle_predated = False
default last_predation_efficiency = 0.0


# ============================================================
# ENEMY DATA
# ============================================================

init python:

    import renpy.store as store

    ENEMY_DATA = {

        # ====================================================
        # VELDORA'S CAVE
        # ====================================================

        "thunder_frog": {
            "name": "Thunder Frog",
            "max_hp": 180,
            "run_chance": 0.70,
            "sprite": "images/enemies/electricfrog.png",
            "background": "images/backgrounds/VeldoracaveBattle.png",
            "perception": False,
            "physical_resistance": False,
            "grants": [],
            "moves": [
                {"name": "Electric Strike", "type": "electric", "min": 22, "max": 30, "accuracy": 0.95},
            ],
        },

        "tempest_serpent": {
            "name": "Tempest Serpent",
            "max_hp": 300,
            "run_chance": 0.65,
            "sprite": None,
            "background": "images/backgrounds/VeldoracaveBattle.png",
            "perception": True,
            "physical_resistance": False,
            "grants": ["heat_source_perception", "poison_breath"],
            "moves": [
                {"name": "Bite", "type": "physical", "min": 30, "max": 40, "accuracy": 0.95},
                {"name": "Tail Whip", "type": "physical", "min": 28, "max": 42, "accuracy": 0.90},
                {"name": "Poisonous Breath", "type": "poison", "min": 55, "max": 55, "accuracy": 1.00, "poison_chance": 0.30},
            ],
        },

        "black_spider": {
            "name": "Black Spider",
            "max_hp": 280,
            "run_chance": 0.70,
            "sprite": None,
            "background": "images/backgrounds/VeldoracaveBattle.png",
            "perception": False,
            "physical_resistance": False,
            "grants": ["sticky_thread", "steel_thread"],
            "moves": [
                {"name": "Poisonous Bite", "type": "physical", "min": 32, "max": 42, "accuracy": 0.95},
                {"name": "Sticky Thread", "type": "skill", "min": 0, "max": 0, "accuracy": 1.00, "restrain": True},
                {"name": "Steel Thread", "type": "skill", "min": 38, "max": 50, "accuracy": 0.95},
            ],
        },

        "giant_bat": {
            "name": "Giant Bat",
            "max_hp": 260,
            "run_chance": 0.75,
            "sprite": None,
            "background": "images/backgrounds/VeldoracaveBattle.png",
            "perception": False,
            "physical_resistance": False,
            "grants": ["ultra_sound_waves"],
            "moves": [
                {"name": "Drain", "type": "skill", "min": 35, "max": 45, "accuracy": 0.95, "drain": True},
                {"name": "Ultra Sound Waves", "type": "skill", "min": 24, "max": 34, "accuracy": 1.00},
            ],
        },

        "evil_centipede": {
            "name": "Evil Centipede",
            "max_hp": 340,
            "run_chance": 0.60,
            "sprite": None,
            "background": "images/backgrounds/VeldoracaveBattle.png",
            "perception": False,
            "physical_resistance": False,
            "grants": ["paralyzing_breath"],
            "moves": [
                {"name": "Bite", "type": "physical", "min": 36, "max": 46, "accuracy": 0.95},
                {"name": "Headbutt", "type": "physical", "min": 38, "max": 50, "accuracy": 0.90},
                {"name": "Paralysis Breath", "type": "paralysis", "min": 30, "max": 30, "accuracy": 1.00, "paralysis_chance": 0.30},
            ],
        },

        "armorsaurus": {
            "name": "Armorsaurus",
            "max_hp": 420,
            "run_chance": 0.55,
            "sprite": None,
            "background": "images/backgrounds/VeldoracaveBattle.png",
            "perception": False,
            "physical_resistance": True,
            "grants": ["body_armor"],
            "moves": [
                {"name": "Bite", "type": "physical", "min": 40, "max": 52, "accuracy": 0.95},
                {"name": "Headbutt", "type": "physical", "min": 44, "max": 58, "accuracy": 0.90},
            ],
        },


        # ====================================================
        # WEST JURA
        # ====================================================

        "horn_rabbit": {
            "name": "Horn Rabbit",
            "max_hp": 170,
            "run_chance": 0.80,
            "sprite": None,
            "background": "west_jura_battle",
            "perception": False,
            "physical_resistance": False,
            "grants": ["danger_sense"],
            "moves": [
                {"name": "Horn Charge", "type": "physical", "min": 24, "max": 34, "accuracy": 0.95},
            ],
        },

        "giant_bear": {
            "name": "Giant Bear",
            "max_hp": 400,
            "run_chance": 0.60,
            "sprite": None,
            "background": "west_jura_battle",
            "perception": False,
            "physical_resistance": False,
            "grants": ["keen_smell"],
            "moves": [
                {"name": "Claw", "type": "physical", "min": 42, "max": 56, "accuracy": 0.95},
                {"name": "Bite", "type": "physical", "min": 38, "max": 52, "accuracy": 0.95},
            ],
        },

        "barghest": {
            "name": "Barghest",
            "max_hp": 360,
            "run_chance": 0.60,
            "sprite": None,
            "background": "west_jura_battle",
            "perception": False,
            "physical_resistance": False,
            "grants": ["fire_breath"],
            "moves": [
                {"name": "Bite", "type": "physical", "min": 34, "max": 46, "accuracy": 0.95},
                {"name": "Fire Breath", "type": "heat", "min": 55, "max": 55, "accuracy": 1.00, "burn_chance": 0.30},
            ],
        },

        "knight_spider": {
            "name": "Knight Spider",
            "max_hp": 450,
            "run_chance": 0.55,
            "sprite": None,
            "background": "west_jura_battle",
            "perception": False,
            "physical_resistance": True,
            "grants": [],
            "moves": [
                {"name": "Bite", "type": "physical", "min": 38, "max": 50, "accuracy": 0.95},
                {"name": "Steel Thread", "type": "skill", "min": 50, "max": 50, "accuracy": 0.95},
            ],
        },

        "blood_boar": {
            "name": "Blood Boar",
            "max_hp": 380,
            "run_chance": 0.60,
            "sprite": None,
            "background": "west_jura_battle",
            "perception": False,
            "physical_resistance": True,
            "grants": ["steel_pelt"],
            "moves": [
                {"name": "Tusk Charge", "type": "physical", "min": 42, "max": 56, "accuracy": 0.92},
            ],
        },

        "blade_tiger": {
            "name": "Blade Tiger",
            "max_hp": 480,
            "run_chance": 0.50,
            "sprite": None,
            "background": "west_jura_battle",
            "perception": False,
            "physical_resistance": False,
            "grants": ["voice_canon"],
            "moves": [
                {"name": "Claw", "type": "physical", "min": 44, "max": 58, "accuracy": 0.95},
                {"name": "Voice Canon", "type": "skill", "min": 120, "max": 120, "accuracy": 1.00},
            ],
        },

        "direwolf_leader": {
            "name": "Direwolf Leader",
            "max_hp": 520,
            "run_chance": 0.00,
            "sprite": None,
            "background": "west_jura_battle",
            "perception": False,
            "physical_resistance": False,
            "grants": [],
            "moves": [
                {"name": "Bite", "type": "physical", "min": 48, "max": 62, "accuracy": 0.95},
                {"name": "Claw", "type": "physical", "min": 44, "max": 58, "accuracy": 0.95},
            ],
        },
    }


    def grant_enemy_skills(enemy_key):

        gained = []

        for skill_key in ENEMY_DATA[enemy_key].get("grants", []):

            if grant_skill(skill_key):
                gained.append(SKILL_NAMES.get(skill_key, skill_key))

        return gained


    def physical_damage_multiplier():

        if store.steel_strength:
            return 3.0

        if store.strengthen:
            return 2.0

        return 1.0


    def reduce_player_damage_for_resistance(damage, attack_type):

        # Physical resistance does not stack between Body Armor
        # and Steel Pelt. Either one gives the same resistance.
        if attack_type == "physical":

            if store.body_armor or store.steel_pelt:
                return max(1, int(damage * 0.50))

        if attack_type == "electric":

            if getattr(store, "electricity_resistance", False):
                return max(1, int(damage * 0.50))

        if attack_type == "heat":

            if getattr(store, "heat_resistance", False):
                return max(1, int(damage * 0.50))

        if attack_type == "cold":

            if getattr(store, "cold_resistance", False):
                return max(1, int(damage * 0.50))

        return damage


# ============================================================
# OLD LABEL COMPATIBILITY
# ============================================================

label battle_thunder_frog:

    call battle_enemy("thunder_frog")

    return _return


label battle_part2_enemy(enemy_key):

    call battle_enemy(enemy_key)

    return _return


# ============================================================
# GENERIC SINGLE-ENEMY BATTLE
# ============================================================

label battle_enemy(enemy_key, predator_allowed=True):

    $ sync_skill_moves()

    $ enemy_data = ENEMY_DATA[enemy_key]
    $ enemy_name = enemy_data["name"]
    $ enemy_max_hp = enemy_data["max_hp"]
    $ enemy_hp = enemy_max_hp
    $ enemy_run_chance = enemy_data["run_chance"]
    $ enemy_sprite = enemy_data["sprite"]
    $ enemy_background = enemy_data["background"]
    $ enemy_has_perception = enemy_data["perception"]
    $ enemy_physical_resistance = enemy_data["physical_resistance"]

    $ player_hp = player_max_hp

    $ last_battle_predated = False
    $ last_predation_efficiency = 0.0

    # Player-applied effects.
    $ enemy_poisoned = False
    $ enemy_burned = False
    $ enemy_steel_web = False
    $ enemy_skip_turn = False
    $ enemy_speed_reduced = False
    $ enemy_damage_reduction_turns = 0
    $ misty_field_active = False

    # Enemy-applied effects.
    $ player_poisoned = False
    $ player_burned = False
    $ player_skip_turn = False
    $ player_restrained = False

    n "[enemy_name] attacks!"


    while enemy_hp > 0 and player_hp > 0:

        $ battle_menu_level = "main"
        $ battle_category = None


        # ====================================================
        # DAMAGE-OVER-TIME ON PLAYER
        # ====================================================

        if player_poisoned:

            $ status_damage = max(1, int(player_max_hp * 0.05))
            $ player_hp = max(0, player_hp - status_damage)

            n "Poison deals [status_damage] damage to you."

        if player_burned and player_hp > 0:

            $ status_damage = max(1, int(player_max_hp * 0.05))
            $ player_hp = max(0, player_hp - status_damage)

            n "Burn deals [status_damage] damage to you."

        if player_hp <= 0:
            break


        # ====================================================
        # PLAYER TURN
        # ====================================================

        if player_skip_turn:

            $ player_skip_turn = False

            n "Paralysis prevents you from moving this turn!"

        else:

            window hide

            $ battle_result = renpy.call_screen(
                "battle_command_menu",
                enemy_name=enemy_name,
                enemy_hp=enemy_hp,
                enemy_max_hp=enemy_max_hp,
                enemy_sprite=enemy_sprite,
                battle_background=enemy_background,
                predator_allowed=predator_allowed
            )

            window show


            # ================================================
            # RUN
            # ================================================

            if battle_result[0] == "run":

                $ run_roll = renpy.random.random()

                if run_roll < enemy_run_chance:

                    n "You escape from the [enemy_name]."

                    return "ran"

                else:

                    n "The [enemy_name] blocks your escape!"


            # ================================================
            # PLAYER MOVE
            # ================================================

            elif battle_result[0] == "move":

                $ chosen_category = battle_result[1]
                $ chosen_move = battle_result[2]
                $ move_data = MOVE_DATA[chosen_move]
                $ move_hit = renpy.random.random() <= move_data["accuracy"]

                $ consume_move_use(chosen_move)


                # --------------------------------------------
                # PREDATE
                # --------------------------------------------

                if chosen_move == "Predate":

                    if enemy_hp < 100 and predator_allowed:

                        $ enemy_hp = 0
                        $ last_battle_predated = True
                        $ last_predation_efficiency = 1.0
                        $ gained_skills = grant_enemy_skills(enemy_key)

                        n "Predator consumes the [enemy_name]."

                        n "You absorb 100% of its remaining magicules."

                        if gained_skills:

                            $ gained_text = ", ".join(gained_skills)
                            n "Acquired: [gained_text]."

                    else:

                        n "Predate cannot consume this enemy yet."


                # --------------------------------------------
                # BASIC ATTACK
                # --------------------------------------------

                elif chosen_move == "Basic Attack":

                    if move_hit:

                        $ player_damage = renpy.random.randint(35, 45)
                        $ player_damage = int(player_damage * physical_damage_multiplier())

                        if player_restrained:

                            $ player_damage = max(1, int(player_damage * 0.75))
                            $ player_restrained = False

                            n "The thread restricts your movement."

                        if enemy_physical_resistance:
                            $ player_damage = max(1, int(player_damage * 0.50))

                        $ enemy_hp = max(0, enemy_hp - player_damage)

                        n "You deal [player_damage] physical damage!"

                    else:

                        n "Your attack misses!"


                # --------------------------------------------
                # WATER BLADE
                # --------------------------------------------

                elif chosen_move == "Water Blade":

                    if move_hit:

                        $ player_damage = 70
                        $ enemy_hp = max(0, enemy_hp - player_damage)

                        n "Water forms into a sharp blade."
                        n "You deal [player_damage] damage!"

                    else:

                        n "Water Blade misses!"


                # --------------------------------------------
                # MISTY FIELD
                # --------------------------------------------

                elif chosen_move == "Misty Field":

                    if enemy_has_perception:

                        n "The [enemy_name]'s perception skill lets it see through the mist."

                    else:

                        $ misty_field_active = True

                        n "Misty Field fills the battlefield."
                        n "The enemy's accuracy is lowered by 30%."


                # --------------------------------------------
                # POISONOUS BREATH
                # --------------------------------------------

                elif chosen_move == "Poisonous Breath":

                    if move_hit:

                        $ player_damage = 55
                        $ enemy_hp = max(0, enemy_hp - player_damage)

                        n "Poisonous Breath deals [player_damage] damage!"

                        if renpy.random.random() < 0.30:

                            $ enemy_poisoned = True
                            n "The [enemy_name] is poisoned!"


                # --------------------------------------------
                # STICKY WEB
                # --------------------------------------------

                elif chosen_move == "Sticky Web":

                    $ enemy_speed_reduced = True

                    n "Sticky Web covers the enemy's movement area."
                    n "The [enemy_name]'s speed is lowered."


                # --------------------------------------------
                # STICKY SHOT
                # --------------------------------------------

                elif chosen_move == "Sticky Shot":

                    $ enemy_skip_turn = True

                    n "Sticky Shot entraps the [enemy_name] for one turn!"


                # --------------------------------------------
                # STEEL WEB
                # --------------------------------------------

                elif chosen_move == "Steel Web":

                    $ enemy_steel_web = True

                    n "Steel Web surrounds the [enemy_name]."
                    n "It will take 5% damage each turn."


                # --------------------------------------------
                # THREADED SLASH
                # --------------------------------------------

                elif chosen_move == "Threaded Slash":

                    if move_hit:

                        $ player_damage = 50
                        $ enemy_hp = max(0, enemy_hp - player_damage)

                        n "Threaded Slash deals [player_damage] damage!"

                    else:

                        n "Threaded Slash misses!"


                # --------------------------------------------
                # STEEL BIND
                # --------------------------------------------

                elif chosen_move == "Steel Bind":

                    $ enemy_skip_turn = True

                    n "Steel Bind traps the [enemy_name] for one turn!"


                # --------------------------------------------
                # PARALYSIS BREATH
                # --------------------------------------------

                elif chosen_move == "Paralysis Breath":

                    if move_hit:

                        $ player_damage = 30
                        $ enemy_hp = max(0, enemy_hp - player_damage)

                        n "Paralysis Breath deals [player_damage] damage!"

                        if renpy.random.random() < 0.30:

                            $ enemy_skip_turn = True
                            n "The [enemy_name] is paralyzed!"


                # --------------------------------------------
                # FIRE BREATH
                # --------------------------------------------

                elif chosen_move == "Fire Breath":

                    if move_hit:

                        $ player_damage = 55
                        $ enemy_hp = max(0, enemy_hp - player_damage)

                        n "Fire Breath deals [player_damage] damage!"

                        if renpy.random.random() < 0.30:

                            $ enemy_burned = True
                            n "The [enemy_name] is burned!"


                # --------------------------------------------
                # VOICE CANON
                # --------------------------------------------

                elif chosen_move == "Voice Canon":

                    if player_hp > player_max_hp * 0.50:

                        $ player_damage = 120
                        $ enemy_hp = max(0, enemy_hp - player_damage)

                        n "Voice Canon deals [player_damage] damage!"

                    else:

                        n "You need to be above 50% HP to use Voice Canon."


                # --------------------------------------------
                # INTIMIDATION
                # --------------------------------------------

                elif chosen_move == "Intimidation":

                    $ enemy_damage_reduction_turns = 3

                    n "Coercion crushes the enemy's fighting spirit."
                    n "Its damage is reduced by 25% for 3 turns."


                # --------------------------------------------
                # BLACK LIGHTNING
                # --------------------------------------------

                elif chosen_move == "Black Bolt":

                    $ player_damage = 160
                    $ enemy_hp = max(0, enemy_hp - player_damage)

                    n "Black Bolt deals [player_damage] damage!"


                elif chosen_move == "Black Discharge":

                    $ player_damage = 160
                    $ enemy_hp = max(0, enemy_hp - player_damage)

                    n "Black Discharge deals [player_damage] damage!"


                else:

                    n "[chosen_move] has not been programmed yet."


        # ====================================================
        # ENEMY DEFEATED BY PLAYER TURN
        # ====================================================

        if enemy_hp <= 0:
            break


        # ====================================================
        # DAMAGE-OVER-TIME ON ENEMY
        # ====================================================

        if enemy_poisoned:

            $ status_damage = max(1, int(enemy_max_hp * 0.05))
            $ enemy_hp = max(0, enemy_hp - status_damage)

            n "Poison deals [status_damage] damage to the [enemy_name]."

        if enemy_burned and enemy_hp > 0:

            $ status_damage = max(1, int(enemy_max_hp * 0.05))
            $ enemy_hp = max(0, enemy_hp - status_damage)

            n "Burn deals [status_damage] damage to the [enemy_name]."

        if enemy_steel_web and enemy_hp > 0:

            $ status_damage = max(1, int(enemy_max_hp * 0.05))
            $ enemy_hp = max(0, enemy_hp - status_damage)

            n "Steel Web deals [status_damage] damage to the [enemy_name]."

        if enemy_hp <= 0:
            break


        # ====================================================
        # ENEMY TURN
        # ====================================================

        if enemy_skip_turn:

            $ enemy_skip_turn = False

            n "The [enemy_name] cannot move this turn!"

        else:

            $ enemy_move = renpy.random.choice(enemy_data["moves"])
            $ enemy_move_name = enemy_move["name"]
            $ enemy_accuracy = enemy_move["accuracy"]

            if misty_field_active and not enemy_has_perception:
                $ enemy_accuracy = max(0.0, enemy_accuracy - 0.30)

            if renpy.random.random() <= enemy_accuracy:

                $ enemy_damage = renpy.random.randint(enemy_move["min"], enemy_move["max"])

                if enemy_damage_reduction_turns > 0:
                    $ enemy_damage = max(0, int(enemy_damage * 0.75))

                $ enemy_damage = reduce_player_damage_for_resistance(
                    enemy_damage,
                    enemy_move["type"]
                )

                $ player_hp = max(0, player_hp - enemy_damage)

                n "The [enemy_name] uses [enemy_move_name]!"

                if enemy_damage > 0:
                    n "You take [enemy_damage] damage."

                if enemy_move.get("restrain", False):

                    $ player_restrained = True
                    n "The thread restricts your movement."

                if enemy_move.get("drain", False) and enemy_damage > 0:

                    $ drain_heal = max(1, int(enemy_damage * 0.50))
                    $ enemy_hp = min(enemy_max_hp, enemy_hp + drain_heal)

                    n "The [enemy_name] restores [drain_heal] HP."

                if enemy_move.get("poison_chance", 0.0) > 0.0:

                    if renpy.random.random() < enemy_move["poison_chance"]:

                        $ player_poisoned = True
                        n "You are poisoned!"

                if enemy_move.get("burn_chance", 0.0) > 0.0:

                    if renpy.random.random() < enemy_move["burn_chance"]:

                        $ player_burned = True
                        n "You are burned!"

                if enemy_move.get("paralysis_chance", 0.0) > 0.0:

                    $ paralysis_roll = enemy_move["paralysis_chance"]

                    if getattr(store, "paralysis_resistance", False):
                        $ paralysis_roll *= 0.50

                    if renpy.random.random() < paralysis_roll:
                        $ player_skip_turn = True
                        n "You are paralyzed!"

            else:

                n "The [enemy_name]'s [enemy_move_name] misses!"


        if enemy_damage_reduction_turns > 0:
            $ enemy_damage_reduction_turns -= 1


    # ========================================================
    # RESULT
    # ========================================================

    if enemy_hp <= 0:

        # If Predate was not used in combat, Predator absorbs the
        # defeated monster at 80% effectiveness. Direwolf Leader
        # story fights can disable Predator entirely.
        if predator and predator_allowed and not last_battle_predated:

            $ last_battle_predated = True
            $ last_predation_efficiency = 0.80
            $ gained_skills = grant_enemy_skills(enemy_key)

            n "Predator absorbs the defeated [enemy_name]."
            n "You absorb 80% of its remaining magicules."

            if gained_skills:

                $ gained_text = ", ".join(gained_skills)
                n "Acquired: [gained_text]."

        return "won"

    return "lost"
